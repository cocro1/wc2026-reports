#!/usr/bin/env python3
"""Generate June 20, 2026 World Cup predictions - 4 matches (Groups E & F, MD2)"""

import json, os, datetime

BASE = r"C:\Users\cocro\WorkBuddy\wc2026-reports"
OBSIDIAN = r"D:\我的坚果云\OB笔记\自媒体\fwc2026"
REPORT_DATE = "2026-06-20"
DATA_UPDATE_TIME = "2026-06-20 00:00"

# =========== MATCH DATA ===========
matches = [
    {
        "id": "germany-ivory-coast",
        "teamA": "德国",
        "teamB": "科特迪瓦",
        "teamA_en": "germany",
        "teamB_en": "ivory-coast",
        "group": "E",
        "stage": "小组赛第2轮",
        "kickoff": "2026年6月20日 16:00 ET / 06月21日 04:00 北京时间",
        "venue": "BMO球场，多伦多，加拿大",
        "group_situation": "德国首轮7-1大胜库拉索，积3分+6净胜球领跑；科特迪瓦首轮1-0绝杀厄瓜多尔，积3分+1净胜球排名第二。本场胜者将锁定出线主动权。",
        "md1_a": "德国 7-1 库拉索（6月14日，休斯顿）",
        "md1_b": "科特迪瓦 1-0 厄瓜多尔（6月14日，费城）",
    },
    {
        "id": "ecuador-curacao",
        "teamA": "厄瓜多尔",
        "teamB": "库拉索",
        "teamA_en": "ecuador",
        "teamB_en": "curacao",
        "group": "E",
        "stage": "小组赛第2轮",
        "kickoff": "2026年6月20日 20:00 ET / 06月21日 08:00 北京时间",
        "venue": "箭头体育场，堪萨斯城，美国",
        "group_situation": "厄瓜多尔首轮0-1惜败科特迪瓦，0分-1净胜球排名第三；库拉索首轮1-7惨败德国，0分-6净胜球垫底。本场对双方均为生死战，输球方基本出局。",
        "md1_a": "厄瓜多尔 0-1 科特迪瓦（6月14日，费城）",
        "md1_b": "库拉索 1-7 德国（6月14日，休斯顿）",
    },
    {
        "id": "netherlands-sweden",
        "teamA": "荷兰",
        "teamB": "瑞典",
        "teamA_en": "netherlands",
        "teamB_en": "sweden",
        "group": "F",
        "stage": "小组赛第2轮",
        "kickoff": "2026年6月20日 13:00 ET / 06月21日 01:00 北京时间",
        "venue": "NRG体育场，休斯顿，美国",
        "group_situation": "瑞典首轮5-1横扫突尼斯，积3分+4净胜球领跑；荷兰首轮2-2战平日本，积1分净胜球0排名第二。本场是小组头名之争的关键战役。",
        "md1_a": "荷兰 2-2 日本（6月14日，阿灵顿）",
        "md1_b": "瑞典 5-1 突尼斯（6月14日，蒙特雷）",
    },
    {
        "id": "tunisia-japan",
        "teamA": "突尼斯",
        "teamB": "日本",
        "teamA_en": "tunisia",
        "teamB_en": "japan",
        "group": "F",
        "stage": "小组赛第2轮",
        "kickoff": "2026年6月20日 22:00 CT / 06月21日 11:00 北京时间",
        "venue": "BBVA体育场，蒙特雷，墨西哥",
        "group_situation": "日本首轮2-2逼平荷兰，积1分净胜球0排名第三；突尼斯首轮1-5惨败瑞典，0分-4净胜球垫底。突尼斯若再败将提前出局，日本取胜则掌握出线主动权。",
        "md1_a": "突尼斯 1-5 瑞典（6月14日，蒙特雷）",
        "md1_b": "日本 2-2 荷兰（6月14日，阿灵顿）",
    },
]

# =========== CSS STYLE ===========
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system,"PingFang SC","Microsoft YaHei",sans-serif; background:#f5f7fa; color:#1a1a2e; line-height:1.8; }
.header { background:#0033A0; color:white; padding:32px 24px 28px; text-align:center; border-bottom:4px solid #002070; }
.header h1 { font-size:24px; font-weight:700; letter-spacing:2px; }
.header p { font-size:14px; opacity:0.85; margin-top:8px; }
.container { max-width:960px; margin:0 auto; padding:24px 16px 48px; }
.match-card { background:white; border-radius:10px; box-shadow:0 2px 12px rgba(0,0,0,0.06); margin-bottom:28px; padding:32px; border-left:4px solid #0033A0; }
.match-title { font-size:20px; font-weight:700; color:#0033A0; margin-bottom:6px; }
.match-meta { font-size:13px; color:#666; margin-bottom:20px; line-height:1.6; }
.match-meta strong { color:#0033A0; }
.h2 { font-size:17px; font-weight:700; color:#0033A0; border-bottom:2px solid #e0e8f5; padding-bottom:6px; margin:24px 0 12px; }
.h3 { font-size:15px; font-weight:700; color:#1a1a2e; margin:16px 0 8px; }
p { margin-bottom:10px; font-size:14px; }
table { width:100%; border-collapse:collapse; margin:12px 0; font-size:13px; }
th { background:#0033A0; color:white; padding:8px 10px; text-align:left; font-weight:600; }
td { padding:7px 10px; border-bottom:1px solid #e8e8e8; }
tr:nth-child(even) td { background:#f8fafd; }
.tag { display:inline-block; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600; }
.tag-red { background:#fde8e8; color:#c62828; }
.tag-green { background:#e8f5e9; color:#2e7d32; }
.tag-blue { background:#e3f2fd; color:#0033A0; }
.tag-orange { background:#fff3e0; color:#e65100; }
.tag-yellow { background:#fffde7; color:#f9a825; }
.prob-section { background:#f0f4ff; border-radius:8px; padding:20px; margin:16px 0; }
.prob-bar { display:flex; border-radius:8px; overflow:hidden; height:36px; margin:10px 0; font-size:12px; font-weight:600; text-align:center; line-height:36px; }
.prob-a { background:#0033A0; color:white; }
.prob-d { background:#85B7EB; color:#1a1a2e; }
.prob-b { background:#c5d5f0; color:#1a1a2e; }
.verdict { background:#f0f8f0; border-left:4px solid #2e7d32; padding:16px 20px; margin:16px 0; border-radius:4px; font-size:14px; }
.verdict strong { color:#2e7d32; }
.warning { background:#fff8e1; border-left:4px solid #f9a825; padding:12px 16px; margin:12px 0; border-radius:4px; font-size:13px; }
.footer { text-align:center; font-size:11px; color:#aaa; padding:24px; border-top:1px solid #eee; margin-top:32px; }
a { color:#0033A0; }
.standings-table td:first-child { font-weight:700; }
.coach-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:12px 0; }
.coach-card { background:#f8fafd; border-radius:8px; padding:16px; border:1px solid #e0e8f5; }
.coach-card h4 { color:#0033A0; margin-bottom:8px; }
.coach-dim { display:flex; justify-content:space-between; padding:3px 0; font-size:13px; }
.coach-dim span:last-child { font-weight:700; color:#0033A0; }
@media (max-width:700px) { .coach-grid { grid-template-columns:1fr; } .match-card { padding:20px 16px; } }
"""

def gen_match_html(m):
    """Generate HTML for one match"""
    lines = [f'<div class="match-card" id="{m["id"]}">']
    
    # Match info
    lines.append(f'<div class="match-title">{m["teamA"]} vs {m["teamB"]}</div>')
    lines.append(f'<div class="match-meta">')
    lines.append(f'<strong>{m["group"]}组 {m["stage"]}</strong><br>')
    lines.append(f'⏰ {m["kickoff"]}<br>')
    lines.append(f'📍 {m["venue"]}<br>')
    lines.append(f'📊 数据更新时间：{DATA_UPDATE_TIME}')
    lines.append(f'</div>')
    
    # Group situation
    lines.append(f'<div class="h2">同组形势</div>')
    lines.append(f'<p>{m["group_situation"]}</p>')
    lines.append(f'<p><strong>首轮战果：</strong>{m["md1_a"]} | {m["md1_b"]}</p>')
    
    # V3/V4 detailed analysis placeholder
    lines.append(f'<div class="h2">近期状态（对手强度校准后）</div>')
    lines.append(f'<p><strong>{m["teamA"]}：</strong></p>')
    lines.append(f'<p><strong>{m["teamB"]}：</strong></p>')
    
    # The full report content will be injected
    lines.append(f'<div id="content-{m["id"]}"></div>')
    
    lines.append(f'</div>')
    return "\n".join(lines)

def gen_index_entry(m):
    """Generate JS entry for index.html"""
    return f'''    date: "{REPORT_DATE}",
    file: "reports/report-{REPORT_DATE}-{m['teamA_en']}-{m['teamB_en']}.html",
    title: "{m['teamA']} vs {m['teamB']}",
    group: "{m['group']}组 小组赛",
    prediction: "详见报告",
    confidence: "中",
    actual: false'''

# =========== Markdown generator ===========
def gen_md(m):
    """Generate markdown report for one match"""
    md = f"""# {m['teamA']} vs {m['teamB']} — {m['group']}组 {m['stage']} 预测报告

> 数据更新时间：{DATA_UPDATE_TIME}

## 【比赛信息】
- **对阵**：{m['teamA']} vs {m['teamB']}
- **赛事**：{m['group']}组 {m['stage']}
- **时间**：{m['kickoff']}
- **地点**：{m['venue']}
- **同组形势**：{m['group_situation']}
- **首轮赛果**：{m['md1_a']} | {m['md1_b']}

"""
    return md

# We'll fill in the detailed content for each match manually 
# since the V4 framework requires deep qualitative analysis

print("Template files generated.")
print(f"Base directory: {BASE}")
print(f"Obsidian directory: {OBSIDIAN}")
