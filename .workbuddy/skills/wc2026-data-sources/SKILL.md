---
name: wc2026-data-sources
description: >-
  2026世界杯预测报告增强数据采集协议。当执行世界杯预测或复盘任务时使用此技能，
  按优先级从FBref、xGscore、WhoScored/Sofascore、Transfermarkt、365Scores、
  FIFA官网等权威源采集结构化数据，替代从二手分析网站抓取的不可靠数据。
  V3/V4强制要求（球员20人覆盖、xG量化、对手强度校准、门将分析、教练评估）
  的数据缺口通过此技能补齐。
agent_created: true
---

# 2026 世界杯数据采集增强协议

## 核心原则

所有数据采集以**一手统计源**和**专业数据平台**为优先，不再依赖二手分析网站的摘要转述。

## 数据源优先级矩阵

| 优先级 | 数据源 | 采集内容 | 验证状态 |
|--------|--------|----------|----------|
| P0 | **FBref** (fbref.com) | 赛程、赛果、球员数据、xG/xGA、射门图 | ✅ 已验证 |
| P0 | **FIFA 官网** (fifa.com) | 官方阵容、伤停、赛程确认 | ✅ 已验证 |
| P1 | **xGscore** (xgscore.io) | 赛事xG统计、球队xG档案 | ✅ 已验证 |
| P1 | **365Scores** (365scores.com) | 球员评分、对阵数据、实时xG | ✅ 已验证 |
| P1 | **Transfermarkt** (transfermarkt.com) | 身价、伤病、转会状态 | ✅ 已验证 |
| P2 | **Sofascore** (sofascore.com) | 球员近5场评分、热图、攻防统计 | ✅ 已验证 |
| P2 | **Soccergraph** (soccergraph.com) | 阵容名单、身价汇总、赛程 | ✅ 已验证 |
| P2 | **worldcuppass.com** | 26人完整大名单（按位置分） | ✅ 已验证 |
| P2 | **totalfootballanalysis.com** | 战术预览、阵型预测、对位分析 | ✅ 已验证 |
| P3 | **FootyStats** (footystats.org) | 角球、牌数、进球时间分布 | ⚠️ 待验证 |

## 数据采集工作流

### 阶段 1：赛程确认（每次预测任务启动时）

```
1. 确认"明天"有哪些比赛（北京时间 UTC+8）
2. 交叉验证：FBref schedule + FIFA 官网 schedule + fwcschedule.com
3. 提取：比赛双方、组别、轮次、开球时间、场地、裁判
```

**FBref 赛程页**：`https://fbref.com/en/comps/1/schedule/World-Cup-Scores-and-Fixtures`
**FIFA 赛程**：`https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums`

### 阶段 2：小组形势与已完赛赛果（每场比赛）

```
1. 从 FBref schedule 提取同组已完赛赛果
2. 计算小组积分榜（胜/平/负/进球/失球/净胜球）
3. 标注出线形势：已出线 / 关键战 / 荣誉战
```

### 阶段 3：球员数据采集——20人覆盖（每队）

**一手源（优先）**：
- **FBref 球队统计页**：`https://fbref.com/en/squads/{squad_id}/{Team-Name}-Stats`
  - 球员名单、位置、年龄、俱乐部
  - 世界杯赛事内的 xG、射门、传球、防守数据
- **worldcuppass.com**：`https://worldcuppass.com/{team}-world-cup-squad-2026/`
  - 26人大名单（按位置分类）
  - 俱乐部归属、国家队出场/进球

**二手源（补充）**：
- **Soccergraph**：阵容深度图和身价
- **Transfermarkt**：身价、伤停状态

**球员覆盖强制清单**：
- 首发11人（所有位置）+ 5-9名关键轮换
- 必须包含：核心射手、组织核心、防守核心、首发门将
- 标注：首发概率（高>80%/中50-80%/低<50%）

### 阶段 4：xG 量化数据（每队，强制）

**一手源**：
- **FBref 世界杯统计**：`https://fbref.com/en/comps/1/World-Cup-Stats`
  - 赛事阶段 xG/xGA（需点击进入比赛详情页获取逐场 xG）
- **xGscore 世界杯 xG 统计**：`https://xgscore.io/xg-statistics/world-cup/2026`
  - 球队 xG 档案（xG created/xG conceded per match）
- **365Scores 球队统计**：`https://www.365scores.com/football/league/fifa-world-cup-5930/stats`

**采集指标**：
- 近10场 xG（预期进球）
- 近10场 xGA（预期失球）
- 加权平均 xG 区间（按对手强度加权）
- 射门转化率
- ⚠️ 禁止只写"大球/小球"

### 阶段 5：门将专项数据（每队首发门将，强制）

**来源**：FBref 球队统计页 → Goalkeeping 表格

**采集指标**：
- 扑救率 (Save%)
- xG 阻止值 (PSxG+/- 或 Goals Prevented)
- 面对不同类型射门表现（远射/近距离/点球）
- 近10场数据加权平均

### 阶段 6：对手强度校准（强制）

**来源**：FIFA 排名（2026年6月最新）

**分档标准**：
- Tier 1：FIFA 前20名
- Tier 2：21-50名
- Tier 3：51-80名
- Tier 4：80名以外

对所有预选赛/友谊赛数据按对手分档重新统计。加权后的数据才算有效预测依据。

### 阶段 7：阵容身价与市场参考

**来源**：Transfermarkt（通过 soccergraph.com 聚合）
**Soccergraph 身价排名页**：`https://www.soccergraph.com/2026/05/fifa-world-cup-2026-all-48-team-market-values-full-ranking.html`

**用途**：
- 阵容深度判断（身价差距>3倍视为实力悬殊）
- 球员个体身价作为"联赛→大赛折扣"基准
- 身价最高的5名球员 vs 实际出场球员对比

### 阶段 8：教练数据（V4要求）

**来源**：综合搜索 + 二手分析 → FBref 执教记录验证

**采集指标**：执教场次、胜率（按Tier拆分）、世界杯/洲际杯成绩

### 阶段 9：环境/场地因子

**来源**：
- 场地海拔 → Google/Wikipedia
- 天气 → weather.com 或当地气象预报
- 中立场判断 → FIFA 赛程说明

### 阶段 10：二手分析补充（仅战术层面）

**totalfootballanalysis.com**：阵型预测、对位分析、概率预测
**soccervital.org**：赛前预测摘要（仅作交叉验证）

⚠️ 战术分析**可以**参考二手来源。**不可以**将二手来源的xG/概率/球员评分当作一手数据。

## 数据采集检查清单

每场预测任务执行前，用以下清单自检：

```
□ 赛程确认（≥2源交叉验证）
□ 小组形势（积分榜+赛果）
□ A队20人名单（含首发概率标注）
□ B队20人名单（含首发概率标注）
□ A队近10场 xG/xGA
□ B队近10场 xG/xGA
□ A队门将扑救率+PSxG+/-
□ B队门将扑救率+PSxG+/-
□ A队对手强度分档统计
□ B队对手强度分档统计
□ 阵容身价对比
□ 主教练数据（≥2源）
□ 伤停/停赛信息
□ 场地/天气/海拔
□ 数据缺失清单（标注哪些数据无法获取）
```

## 数据质量标注规则

在报告中标注数据来源层级：

- **L1（一手统计数据）**：FBref/xGscore 直接获取的 xG、扑救率等 → 置信度高
- **L2（聚合统计）**：365Scores/Soccergraph 聚合数据 → 置信度中
- **L3（二手分析）**：totalfootballanalysis/soccervital 分析文章 → 置信度低
- **L4（推断/假设）**：基于趋势的主观判断 → 需明确标注

## 已知数据缺口

以下数据在当前各来源中**可能不可用**：

1. **球员俱乐部近5场评分**：WhoScored/Sofascore 世界杯专用页面可能不覆盖俱乐部数据
   → 降级方案：使用 FBref 世界杯赛事内评分
2. **替补登场后首次射门时间**：极难从一手源获取
   → 降级方案：基于球员位置的定性判断（如"终结型前锋→即战力型替补"）
3. **教练维度评分**（1-10分制）：所有来源都是主观判断
   → 标注为 L4 推断，不伪装成客观数据
4. **犯规类型细分（战术/失控）**：FBref 可能有犯规次数但不区分类型
   → 可采集犯规次数+黄牌数，类型分析标注为推断
