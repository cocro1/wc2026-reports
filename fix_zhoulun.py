"""
批量重写 6/25 报告中的 "末轮" 错误用法。

核心问题：6/25 是 MD3 小组赛末轮，所有报告里：
- "末轮" 指向"未来第 4 场" 是错的（没有第 4 场）
- "末轮" 用作"为未来准备" 也是错的（本场就是末轮，本场结束小组赛就结束）
- "本场+末轮=X 分" 算分也错了（本场打完就是最终积分）

改写策略（精准 replace_all）：
1. 末轮对XX队 / 末轮vsXX → 本场 vs XX（如果是本场对手，删除整句）
2. 末轮停赛 → 累黄停赛 / 本场停赛
3. 末轮压力 / 末轮影响 → 收官战压力 / 收官战影响
4. 末轮留力 → 收官战留力
5. 末轮对XX战 / 末轮决战 → 收官战
6. (本场+末轮) 算分 → (本场) 算分（但保留 "(本场赢+平)=X 分" 这种小组合写法）
7. "末轮为..." → "本场为..."
8. "本场是末轮" → "本场是收官战（MD3）"
9. 表格表头"末轮" → "出线形势"或"本场后积分"
10. "末轮+首轮" 表格列名 → 删除末轮列

保留用法：
- "末轮" 单独使用且指"小组赛末轮（MD3）"即本场 → 保留或改为"小组赛收官战"
"""
import re
import os
from pathlib import Path

BASE = Path(r'C:\Users\cocro\WorkBuddy\wc2026-reports\reports')
FILES = [
    'report-2026-06-25-switzerland-canada.html',
    'report-2026-06-25-bosnia-qatar.html',
    'report-2026-06-25-morocco-haiti.html',
    'report-2026-06-25-scotland-brazil.html',
    'report-2026-06-25-czech-mexico.html',
    'report-2026-06-25-south-africa-south-korea.html',
]

# 报告里还可能在 MD 笔记 (Obsidian) 也有同样问题
OB_FILES = [
    r'D:\我的坚果云\OB笔记\自媒体\fwc2026\content\predictions\2026-06-25-switzerland-canada-prediction.md',
    r'D:\我的坚果云\OB笔记\自媒体\fwc2026\content\predictions\2026-06-25-bosnia-qatar-prediction.md',
    r'D:\我的坚果云\OB笔记\自媒体\fwc2026\content\predictions\2026-06-25-morocco-haiti-prediction.md',
    r'D:\我的坚果云\OB笔记\自媒体\fwc2026\content\predictions\2026-06-25-scotland-brazil-prediction.md',
    r'D:\我的坚果云\OB笔记\自媒体\fwc2026\content\predictions\2026-06-25-czech-mexico-prediction.md',
    r'D:\我的坚果云\OB笔记\自媒体\fwc2026\content\predictions\2026-06-25-south-africa-south-korea-prediction.md',
]

def fix_text(txt: str, file_label: str = '') -> tuple[str, dict]:
    """对一段文本做精准 末轮 修复，返回 (新文本, 改动计数)"""
    changes = {}

    # ====== 优先级最高：完整短语先替换 ======
    rules = [
        # --- 1. 整句"末轮对XX队" / "末轮vsXX" 表达未来比赛 ---
        # 模式: "末轮对<球队>" / "末轮对<球队>战" / "末轮<球队>" 等
        (r'末轮对([^，。；,;\s（）)]+)', r'本场（小组赛收官战 MD3）对\1'),
        (r'末轮vs\s*([^，。；,;\s（）)]+)', r'本场（收官战 MD3）vs \1'),
        (r'对末轮', r'对收官战'),  # 反向："对末轮X" → "对收官战X"

        # --- 2. 算分公式：本场+末轮=X → 修正 ---
        # 模式: "3分(本场赢)+ 3分(末轮)" 这种"X分(本场)+ Y分(末轮)" 双项算分公式 → 改为"X分(本场赢, MD3收官)= Z分"
        # 简单粗暴：找 "本场)+数字分(末轮)" 整个算分小节
        # 例: "3分(本场赢)+ 0分(末轮)= 6分=小组第二(稳出线)"
        #   → "3分(本场赢, MD3收官)= 6分=小组第二(稳出线)"

        # --- 3. 末轮停赛 ---
        (r'末轮停赛', '累黄停赛（小组赛已收官，无下场影响）'),
        (r'末轮被禁赛', '累黄停赛（小组赛已收官，无下场影响）'),
        (r'避免末轮停赛', '避免累黄再吃黄'),
        (r'避免末轮累黄', '避免累黄再吃黄'),
        (r'保护核心避免末轮累黄', '保护核心避免累黄再吃黄'),
        (r'末轮累黄停赛', '累黄再吃黄停赛'),

        # --- 4. 末轮留力 / 末轮压力 / 末轮策略 ---
        (r'为末轮[^，。,;]{0,8}留力', '收官战留力（本场即收官战，留力意义减弱）'),
        (r'末轮留力', '收官战留力'),
        (r'末轮压力', '收官战压力'),
        (r'末轮形势', '收官战形势'),
        (r'末轮结果', '本场结果'),
        (r'末轮+[^，。,;]{0,8}结果', '本场结果'),

        # --- 5. "末轮对X决战" / "末轮决战" / "末轮之战" ---
        (r'末轮[^，。,;]{0,4}决战', '收官战决战'),
        (r'末轮[^，。,;]{0,4}之战', '收官战'),
        (r'末轮[^，。,;]{0,4}对话', '收官战对话'),

        # --- 6. "末轮为X" / "末轮X场" / "末轮胜/平/负" ---
        (r'末轮为([^，。,;]{0,15})练兵', r'本场\1练兵'),
        (r'末轮为([^，。,;]{0,15})准备', r'本场\1准备'),
        (r'末轮胜', '本场胜'),  # 在算分语境里
        (r'末轮平', '本场平'),
        (r'末轮负', '本场负'),
        (r'末轮vs', '收官战 vs'),

        # --- 7. "末轮+首轮" 表格列名 → "出线形势"
        (r'<th>末轮</th>', r'<th>本场后出线形势</th>'),

        # --- 8. "本场是末轮" 保留为"本场是收官战（MD3）"
        (r'本场是末轮', '本场是小组赛收官战（MD3）'),
        (r'本场为末轮', '本场为小组赛收官战（MD3）'),
        (r'本场即末轮', '本场即小组赛收官战（MD3）'),
        (r'末轮(?!对|vs|对|留|压|战|形|结|停|累|被|为)', '收官战'),  # 单独使用的"末轮"
    ]

    for pattern, repl in rules:
        new_txt, n = re.subn(pattern, repl, txt)
        if n > 0:
            changes[pattern] = n
            txt = new_txt

    # ====== 第二轮：算分公式清理 ======
    # 模式: "3分(本场赢)+ 0分(末轮)= 6分" → "3分(本场赢, MD3收官)= 6分"
    # 这种"X分(本场赢/平/负)+ Y分(末轮胜/平/负)= Z分"全部改为"X分(本场) = Z分"

    # 通用模式: "(本场赢) + 0-3分(末轮) = X-Y分" 全部重写
    # 用正则找 "数字分(本场X)+ 数字-数字分(末轮)=" 这种双项算分 → 单项算分
    def simplify_score(m):
        return m.group(1) + '分（本场收官，MD3 结束）=' + m.group(3)
    txt = re.sub(
        r'(\d+)分\((本场[赢平负]+)\)\+\s*[\d-]+分\(末轮[赢平负]?[赢平负]?[赢平负]?\)=' + r'(\d+-?\d*分)',
        simplify_score, txt
    )
    # 也处理: "3分(本场赢)+ 1分(末轮)= 8分" → "3分(本场赢, MD3收官)= 8分"
    txt = re.sub(
        r'(\d+)分\((本场[赢平负]+)\)\+\s*\d+分\(末轮\)=' + r'(\d+分)',
        lambda m: f'{m.group(1)}分({m.group(2)}, MD3 收官)={m.group(3)}', txt
    )
    # 处理: "3分(本场)+ 0-3分(末轮)= 3-6分" → "3分(本场, MD3收官)= 3-6分"
    txt = re.sub(
        r'(\d+)分\((本场)\)\+\s*[\d-]+分\(末轮\)=' + r'(\d+-?\d*分)',
        lambda m: f'{m.group(1)}分({m.group(2)}, MD3 收官)={m.group(3)}', txt
    )

    # 简单粗暴：把"本场)+数字分(末轮)=" 后面所有
    # 模式: "+ X分(末轮胜X队)" → 删除
    txt = re.sub(r'\+\s*\d+分\(末轮胜[一-龥]+\)', '', txt)
    txt = re.sub(r'\+\s*\d+分\(末轮胜[一-龥]+[一-龥]?\)', '', txt)
    txt = re.sub(r'\+\s*\d+分\(末轮\)', '', txt)
    # 模式: "X分(末轮胜X队)= Y分" 中保留 Y分，去掉算分过程
    txt = re.sub(r'\d+分\(末轮胜[一-龥]+\)=', '', txt)
    txt = re.sub(r'\d+分\(末轮\)=', '', txt)

    return txt, changes

def main():
    total_files = 0
    total_changes = 0
    for fname in FILES:
        path = BASE / fname
        if not path.exists():
            print(f'  ⚠️ {fname} 不存在')
            continue
        with open(path, 'r', encoding='utf-8') as f:
            txt = f.read()
        new_txt, changes = fix_text(txt, fname)
        if changes:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_txt)
            total_files += 1
            total_changes += sum(changes.values())
            print(f'✅ {fname}: {sum(changes.values())} 处改动')
            for k, v in list(changes.items())[:5]:
                print(f'     {k!r} → {v} 次')
        else:
            print(f'  {fname}: 无改动')
    print()
    print(f'=== HTML 总计: {total_files} 份文件, {total_changes} 处改动 ===')

    # 处理 OB 笔记
    print('\n=== 处理 OB 笔记 ===')
    for path in OB_FILES:
        if not os.path.exists(path):
            print(f'  ⚠️ {os.path.basename(path)} 不存在')
            continue
        with open(path, 'r', encoding='utf-8') as f:
            txt = f.read()
        new_txt, changes = fix_text(txt, os.path.basename(path))
        if changes:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_txt)
            total_changes += sum(changes.values())
            print(f'✅ {os.path.basename(path)}: {sum(changes.values())} 处改动')

    print(f'\n=== 总改动: {total_changes} 处 ===')

if __name__ == '__main__':
    main()
