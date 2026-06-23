# 2026世界杯预测 — 自动化流水线操作手册

> 本文档是流水线的总入口。如果你是一个新 AI，请从本文档开始阅读。

## 目录

1. [流水线概览](#流水线概览)
2. [七条铁律（最高优先级）](#七条铁律最高优先级)
3. [文件结构全景图](#文件结构全景图)
4. [数据流转图](#数据流转图)
5. [各步骤入口](#各步骤入口)
6. [故障排查指南](#故障排查指南)

---

## 流水线概览

```
写文稿 (17:30)  →  校对文稿 (18:30)  →  网站发布 (19:30)
     │                    │                    │
 生成 HTML + MD      数据校验 + 内容优化    构建 + 部署 + 推送
 不更新 index         不部署                 双平台 (CloudStudio + GitHub)
```

每个步骤是独立任务，由定时调度触发。但你也可以手动执行任意步骤。

### 当前部署

| 平台 | URL |
|------|-----|
| CloudStudio | https://4ba4efb5528941e79173f029176fe567.app.codebuddy.work |
| GitHub Pages | https://cocro1.github.io/wc2026-reports/ |
| GitHub 仓库 | https://github.com/cocro1/wc2026-reports |

---

## 七条铁律（最高优先级）

**这些规则在所有步骤中都必须遵守，违规则会导致严重错误。**

### 铁律1：所有时间以北京时间为准（GMT+8）
信息源如用 UTC/EST/EDT 等时区，必须换算为北京时间后写入。
输出格式：`⏰ 当地时间 时区 (城市当地时间) / 北京时间`

### 铁律2：赛程/对阵/比分必须与 FIFA 官方交叉核对
`schedule.json` 不是绝对权威。如与 FIFA 官网 (fifawc-2026.com) / ESPN 不一致，以 FIFA 官方为准。

### 铁律3：文件命名日期以北京时间为准（不可协商）
文件名中的 `YYYY-MM-DD` 必须与北京时间日期一致。
例：比赛在北京时间 6 月 23 日凌晨开赛 → 文件名日期为 `2026-06-23`，而非美东时间的 `6月22日`。

### 铁律4：时区标注必须精确
北美跨 4 个时区：ET(UTC-4) / CT(UTC-5) / MT(UTC-6) / PT(UTC-7)，不可统一标注为 EDT。
墨西哥不使用夏令时：Guadalajara/Mexico City/Monterrey 全年 CST(UTC-6)。

### 铁律5：小组归属正确性
2026 世界杯有 12 个小组 (A-L)，每组 4 队，共 48 队。

### 铁律6：预测比分必须带完整球队名
预测比分文本必须是"克罗地亚 3-0 巴拿马"格式，**严禁"3-0"纯数字**。
原因：首页卡片通过球队名匹配比分方向，纯数字无法判断左右归属。

### 铁律7：预测/备选比分概率逻辑一致
概率最高的比分 → 最可能/主预测，次高的 → 备选 1/备选比分。
禁止把概率低的放主预测、概率高的放备选。

---

## 文件结构全景图

```
wc2026-reports/
├── index.html              ← 网站首页（JS 渲染卡片）
├── schedule.json           ← 73 场小组赛赛程（北京时间，需与 FIFA 交叉核对）
├── match_data.json         ← 预测数据（build_site.py 从 reports/ 生成）
├── simulation_scores.json  ← Dixon-Coles 推演比分（build_simulation_data.py 生成）
├── match_results.json      ← 实际赛果（手动维护）
├── odds.json               ← 实时赔率（fetch_odds.py 抓取）
├── hit_rates.json          ← 命中率统计（build_site.py 计算）
│
├── build_site.py           ← 核心构建脚本（解析报告 + 转文章 + 算命中率）
├── build_simulation_data.py ← 解析 Dixon-Coles MD → simulation_scores.json
│
├── reports/                ← 预测报告 + 复盘报告
│   ├── report-YYYY-MM-DD-teamA-teamB.html  ← 预测报告
│   └── review-YYYY-MM-DD-teamA-teamB.html  ← 复盘报告
│
├── articles/               ← 专题文章（由 build_site.py 从 MD 转换）
│   ├── mystic/             ← 玄学预测
│   ├── simulation/         ← 蒙特卡洛推演
│   ├── research/           ← 专题研究
│   └── articles_index.json
│
├── .workbuddy/
│   ├── pipeline/           ← 📍 本文档所在目录
│   ├── proofreads/         ← 校对报告输出
│   ├── references/         ← 参考数据（场馆时区等）
│   └── memory/             ← 项目记忆
│
└── D:\我的坚果云\OB笔记\自媒体\fwc2026\content\
    ├── predictions/        ← MD 预测笔记（写文稿输出）
    └── dixon-coles-monte-carlo/  ← Dixon-Coles 推演 MD（build_simulation_data.py 输入）
```

---

## 数据流转图

```
                          ┌─────────────────────┐
                          │  FIFA 官方赛程        │
                          │  ESPN / WhoScored    │
                          │  LiveScores.com      │
                          └─────────┬───────────┘
                                    │ 写文稿 读取
                                    ▼
┌──────────────┐      ┌─────────────────────────┐
│ schedule.json │◄────│  写文稿 (STEP 1)         │
│ (赛程基准)     │      │  生成:                   │
└──────┬───────┘      │  • reports/report-*.html │
       │              │  • content/predictions/  │
       │              │    *-prediction.md       │
       │              └───────────┬─────────────┘
       │                          │ 校对 读取+修改
       │                          ▼
       │              ┌─────────────────────────┐
       │              │  校对文稿 (STEP 2)        │
       │              │  校验: 数据/格式/违禁词    │
       │              │  输出: proofreads/*.md    │
       │              └───────────┬─────────────┘
       │                          │ 发布 读取
       ▼                          ▼
┌─────────────────────────────────────────────────┐
│              网站发布 (STEP 3)                    │
│                                                  │
│  build_site.py ──► match_data.json               │
│       │                  + hit_rates.json         │
│       │                                           │
│  build_simulation_data.py ──► simulation_scores   │
│       │                  .json                    │
│       ▼                                           │
│  CloudStudio 部署 ──► app.codebuddy.work          │
│  git push ──► GitHub Pages                        │
└─────────────────────────────────────────────────┘
       │
       ▼
┌────────────────┐
│  index.html    │
│  (首页渲染)     │
│  加载:          │
│  • schedule.json│
│  • match_data   │
│  • simulation   │
│  • odds.json    │
│  渲染:          │
│  • 预测卡片      │
│  • 备选比分      │
│  • 推演比分      │
│  • 赔率          │
│  • 命中率        │
└────────────────┘
```

---

## 各步骤入口

| 步骤 | 文档 | 调度时间 |
|------|------|---------|
| 写文稿 | [PIPELINE-STEP1-WRITE.md](PIPELINE-STEP1-WRITE.md) | 每日 17:30 |
| 校对文稿 | [PIPELINE-STEP2-PROOFREAD.md](PIPELINE-STEP2-PROOFREAD.md) | 每日 18:30 |
| 网站发布 | [PIPELINE-STEP3-PUBLISH.md](PIPELINE-STEP3-PUBLISH.md) | 每日 19:00 |

---

## 故障排查指南

### 问题：首页备选比分不显示

**原因 1**：HTML 报告只有 `<table class="score">` 格式，缺少段落格式。
**修复**：在报告的"比分预测"节中添加：
```html
<p>备选比分1：X-X（概率 ~XX%）</p>
<p>备选比分2：X-X（概率 ~XX%）</p>
```

**原因 2**：`build_site.py` 的 `parse_reports()` 未解析到。检查 `match_data.json` 中该比赛的 `alt_score` 字段是否为空。

### 问题：首页推演比分显示"暂无数据"

**原因 1**：`simulation_scores.json` 缺少该比赛数据。
**修复**：运行 `python build_simulation_data.py`，检查 Dixon-Coles MD 文件是否存在、队名是否已翻译为中文。

**原因 2**：key 名称不匹配。`index.html` 用 `schedule.json` 的 `team_a vs team_b` 作为 key 查找 `simulation_scores.json`。

### 问题：预测比分方向颠倒

（如卡片显示"巴拿马 3:0 克罗地亚"但实际预测克罗地亚赢）
**原因**：预测文本缺少球队名（纯数字"3-0"），或球队顺序与 schedule.json 不一致。
**修复**：
1. 确保 `match_data.json` 的 `prediction` 字段格式为 "TeamX N-M TeamY"
2. `index.html` 的 `formatPredScore()` 函数会自动匹配方向

### 问题：build_site.py 报错

**常见原因**：HTML 报告格式不规范（缺少闭合标签、未使用标准 class 名）。
**修复**：检查新生成的 HTML 报告是否符合历史报告格式。

### 问题：git push 失败

**原因**：远程有新的提交。
**修复**：`git pull --rebase origin main` 后再 push。

### 问题：CloudStudio 部署失败

**修复**：重试一次。如果仍失败，检查 build 输出是否正常（match_data.json 存在且 JSON 格式合法）。

---

## 内容禁令

所有生成的网页、文档、报告中严禁出现：
- "由 WorkBuddy 生成" / "AI 自动生成" / "数妙妙" / "Phoebe"
- "每日自动更新" / "本页由 xxx 自动生成"
- 页脚只允许"报告数据仅供参考，不构成投注建议"
- "AI预测" → 替换为"预测模型"

## 设计规范

- 主色：`#0033A0` | 辅色：`#85B7EB` | 网格：1px `#000` | 留白 ≥65%
- 禁止渐变 / 阴影 / 暖色调
