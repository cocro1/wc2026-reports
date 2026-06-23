# 步骤 3：网站发布

> 执行时机：每日 19:00（北京时间）
> 工作目录：`C:\Users\cocro\WorkBuddy\wc2026-reports`
> 职责：构建数据文件 → CloudStudio 部署 → GitHub 推送

---

## 任务描述

运行构建脚本、部署到 CloudStudio 和 GitHub Pages，确保网站更新到最新状态。

## 执行清单（新 AI 按此顺序操作）

### 第 1 步：构建数据文件

```bash
cd C:\Users\cocro\WorkBuddy\wc2026-reports
python build_site.py
```

**`build_site.py` 做了什么**（5 个子步骤）：

| 子步骤 | 输入 | 输出 | 说明 |
|--------|------|------|------|
| parse_reports() | `reports/report-*.html` | `match_data.json` | 从 HTML 解析预测数据（比赛日期、预测比分、备选比分、胜率、置信度） |
| convert_articles() | `content/{mystic,research,dixon-coles-monte-carlo}/*.md` | `articles/*.html` + `articles_index.json` | 将 MD 文章转为 HTML 页面（teal 主题） |
| calc_hit_rates() | `match_results.json` + `review-*.html` + `over25_data.json` | `hit_rates.json` | 对比预测 vs 实际赛果，计算三项命中率（预测比分 / 推演比分 / 大球概率） |
| extract_over25() | `articles/simulation/*.html` | `over25_data.json` | 从 Dixon-Coles 推演文章提取 >2.5球概率 |
| 输出 | — | 终端简报 | 报告数/文章数/三项命中率 |

**验证**：
```bash
python -c "
import json
data = json.load(open('match_data.json','r',encoding='utf-8'))
print(f'比赛数: {len(data)}')
print(f'最新日期: {max(m[\"date\"] for m in data)}')
# 检查 prediction 字段是否含球队名
for m in data:
    if m.get('prediction') and not any(t in m['prediction'] for t in ['vs','队']):
        print(f'⚠️ 纯数字比分: {m[\"title\"][:40]} -> {m[\"prediction\"]}')
"
```

⚠️ **必须检查**：`match_data.json` 的 `prediction` 字段是否全部包含完整球队名（铁律6）。

### 第 2 步：构建推演比分数据

```bash
python build_simulation_data.py
```

**`build_simulation_data.py` 做了什么**：
- 读取 `D:\我的坚果云\OB笔记\自媒体\fwc2026\content\dixon-coles-monte-carlo\*.md`
- 解析每个比赛的"推荐精准比分"节
- 提取 Top 2 比分 → `simulation_scores.json`（key 为中文队名）

**常见问题**：
- 英文队名未翻译 → 在脚本中 `EN_TO_ZH_TEAM` 字典中添加新球队
- 推荐精准比分格式不匹配 → 确认为 `**X-X**` 格式（不含球队名后缀）

**验证**：
```bash
python -c "
import json
sim = json.load(open('simulation_scores.json','r',encoding='utf-8'))
sch = json.load(open('schedule.json','r',encoding='utf-8'))
for s in sch:
    k = f'{s[\"team_a\"]} vs {s[\"team_b\"]}'
    if s['date'] == '2026-06-24':  # 替换为当天日期
        print(f'{k}: {\"✅\" if k in sim else \"❌ 缺失\"} -> {sim.get(k,\"\")}')
"
```

### 第 3 步：部署到 CloudStudio

使用 `workbuddy_cloudstudio_deploy` 工具：
- 目录：`C:\Users\cocro\WorkBuddy\wc2026-reports`
- 入口文件：`index.html`
- 目标 URL：https://4ba4efb5528941e79173f029176fe567.app.codebuddy.work

**如果部署失败**：重试一次；仍失败则标注原因。

**验证**：用 WebFetch 访问 CloudStudio URL，确认：
- 页面加载成功
- 最新日期的比赛卡片存在
- 备选比分和推演比分显示正常

### 第 4 步：推送到 GitHub Pages

```bash
cd C:\Users\cocro\WorkBuddy\wc2026-reports
git add -A
git commit -m "网站更新: YYYY-MM-DD（build_site + 新报告）"
git -c credential.helper= push origin main
```

- 远程仓库：https://github.com/cocro1/wc2026-reports
- GitHub Pages 在推送后 1-2 分钟自动构建

**如果 git push 失败（远程有新提交）**：
```bash
git pull --rebase origin main
git push origin main
```

### 第 5 步：输出发布简报

```markdown
## 发布简报 — YYYY-MM-DD

### 数据构建
- match_data.json 比赛数：N 场
- 最新日期：YYYY-MM-DD

### 命中率（6月23日起）
- 预测比分命中率：X% (X/N)
- 推演比分命中率：X% (X/N)
- **大球概率命中率：X% (X/N)**
  - 逻辑：over25概率>50%预测大球，实际总进球>2为大球，方向一致=命中

### 部署状态
- CloudStudio：[链接] ✅ 已部署 / ❌ 失败
- GitHub Pages：[链接] ✅ 已推送 / ❌ 失败

### 本次变更
- 新增报告：N 份（列出文件名）
- 修复项：（如有）
```

---

## index.html 渲染机制说明

了解这个机制有助于排查首页显示问题。

### 数据加载顺序

```
1. index.html 加载
2. fetch schedule.json → 按日期分组 → 渲染日期条
3. fetch match_data.json → 与 schedule 匹配合并
4. fetch simulation_scores.json → 查找推演比分
5. fetch over25_data.json → 查找 >2.5球概率
6. fetch hit_rates.json → 显示三项命中率（预测/推演/大球概率）
7. fetch articles/articles_index.json → 动态渲染「推演」「玄学」「专题」tab
```

### 卡片渲染关键函数

| 函数 | 用途 | 输入 | 输出 |
|------|------|------|------|
| `normName(n)` | 标准化队名 | "巴拿马" | "巴拿马" |
| `sameTeam(a,b)` | 判断两名称是否同一队 | "巴拿马", "Panama" | true/false |
| `formatPredScore(pred, a, b)` | 预测比分 → 卡片左:右格式 | "克罗地亚 3-0 巴拿马", "巴拿马", "克罗地亚" | "0 : 3" |
| `formatAltScore(alt, pred, a, b)` | 备选比分 → 卡片左:右格式 | "2-0", "克罗地亚 3-0 巴拿马", "巴拿马", "克罗地亚" | "0 : 2" |
| `findPrediction(a, b)` | 查找匹配的预测数据 | "巴拿马", "克罗地亚" | match_data 条目 |

### 比分方向处理算法

```
formatPredScore("克罗地亚 3-0 巴拿马", team_a="巴拿马", team_b="克罗地亚"):
  1. 解析: predTeam1="克罗地亚", score1=3, score2=0, predTeam2="巴拿马"
  2. sameTeam("克罗地亚", "巴拿马") = false
  3. sameTeam("克罗地亚", "克罗地亚") = true → predTeam1=team_b(right)
  4. 交换: return "0 : 3"  ← 正确！

formatAltScore("2-0", "克罗地亚 3-0 巴拿马", team_a="巴拿马", team_b="克罗地亚"):
  1. 解析: a1=2, a2=0
  2. 从主预测推断: predTeam1="克罗地亚" = team_b
  3. 交换: return "0 : 2"  ← 备选跟随主预测方向
```

### 匹配合并逻辑

```
index.html 合并逻辑:
1. schedule.json: {team_a: "巴拿马", team_b: "克罗地亚", date: "2026-06-24", ...}
2. match_data.json: {title: "巴拿马 vs 克罗地亚 预测报告", prediction: "克罗地亚 3-0 巴拿马", ...}
3. findPrediction("巴拿马", "克罗地亚") → 通过 normName 模糊匹配 → 找到
4. formatPredScore(...) → "0 : 3"
5. formatAltScore(...) → "0 : 2"
6. 渲染卡片: 巴拿马 0 : 3 克罗地亚
```

---

## 常见故障排查

| 问题 | 原因 | 修复 |
|------|------|------|
| 首页某场比赛不显示 | match_data.json 中 title 与 schedule.json 队名不匹配 | 检查队名别名/简称是否在 normName() 中有处理 |
| 备选比分不显示 | alt_score 为空 | 见步骤1 — 段落格式缺失 |
| 推演比分"暂无数据" | simulation_scores.json key 不匹配 | 运行 build_simulation_data.py，检查 EN_TO_ZH_TEAM |
| 比分方向颠倒 | prediction 纯数字无队名 | 回到报告修正 ← 这是铁律6 |
| build_site.py 报错 | 新报告 HTML 格式不规范 | 检查 HTML 是否闭合、是否使用标准 class 名 |
