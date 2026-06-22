# 2026 世界杯数据源 URL 速查表

## FBref（一手统计源，优先级最高）

| 页面 | URL | 用途 |
|------|-----|------|
| 赛程与赛果 | https://fbref.com/en/comps/1/schedule/World-Cup-Scores-and-Fixtures | 全部赛程、比分、场地、裁判 |
| 世界杯统计总页 | https://fbref.com/en/comps/1/World-Cup-Stats | 积分榜、射手榜、助攻榜、门将零封 |
| 球队统计（模板） | https://fbref.com/en/squads/{squad_id}/{Team-Name}-Stats | 替换 squad_id（从赛程页获取） |

### 各队 squad_id 速查（已确认可用）
| 球队 | squad_id |
|------|----------|
| Argentina | f9fddd6e |
| Austria | d5121f10 |
| France | b1b36dcd |
| Iraq | ec843efd |
| Norway | 599eba19 |
| Senegal | 9ab5c684 |
| Jordan | 3e22f0fa |
| Algeria | 1e2dba57 |
| Portugal | 4a1b4ea8 |
| England | 1862c019 |
| Croatia | 7b08e376 |
| Colombia | ab73cfe5 |
| Ghana | 9349828d |
| Panama | 6061a82d |
| Uzbekistan | cd389e75 |
| Congo DR | 9be9f315 |

## xGscore（xG 专业平台）

| 页面 | URL |
|------|-----|
| 世界杯 xG 统计 | https://xgscore.io/xg-statistics/world-cup/2026 |
| xG 计算原理 | https://xgscore.io/how-it-works |
| 今日预测 | https://xgscore.io/predictions/today |
| 正确比分预测 | https://xgscore.io/predictions/correct-score |
| 两队均得分预测 | https://xgscore.io/predictions/both-to-score |
| 世界杯总览 | https://xgscore.io/world-cup/2026 |

## 365Scores

| 页面 | URL |
|------|-----|
| 世界杯统计总页 | https://www.365scores.com/football/league/fifa-world-cup-5930/stats |
| 比赛详情页模板 | https://www.365scores.com/football/match/fifa-world-cup-5930/{team1}-{team2}-{id1}-{id2}-5930 |

## Transfermarkt（身价/伤病）

| 页面 | URL |
|------|-----|
| 参赛队总览 | https://www.transfermarkt.com/world-cup/teilnehmer/pokalwettbewerb/FIWC |
| 世界杯主页 | https://www.transfermarkt.com/weltmeisterschaft/startseite/pokalwettbewerb/FIWC |

## Soccergraph（身价聚合 + 阵容）

| 页面 | URL |
|------|-----|
| 48队身价排名 | https://www.soccergraph.com/2026/05/fifa-world-cup-2026-all-48-team-market-values-full-ranking.html |
| 完整赛程 | https://www.soccergraph.com/2025/12/fifa-world-cup-2026-match-schedule-fixtures-times-results-scores.html |

## worldcuppass.com（26人大名单）

| 页面模板 | URL 模板 |
|----------|----------|
| 球队大名单 | https://worldcuppass.com/{team-name}-world-cup-squad-2026/ |

已确认可用的页面：
- https://worldcuppass.com/portugal-world-cup-squad-2026/
- https://worldcuppass.com/england-world-cup-squad-2026/
- https://worldcuppass.com/argentina-world-cup-squad-2026/
- https://worldcuppass.com/austria-world-cup-squad-2026/

## FIFA 官网

| 页面 | URL |
|------|-----|
| 赛程/场馆 | https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums |
| 阵容公告汇总 | https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/all-world-cup-squad-announcements |

## 二手分析来源（仅战术/预测参考）

| 来源 | URL | 用途 |
|------|-----|------|
| totalfootballanalysis | https://totalfootballanalysis.com/competitions/fifa-world-cup-2026/{team1}-v-{team2}-predictions | 战术分析、阵型 |
| soccervital | https://www.soccervital.org/world-cup-predictions/{team1}-vs-{team2}-prediction-{date}/ | 赛前综合预测 |
| sportsmole | https://www.sportsmole.co.uk/football/{team1}/world-cup-2026/preview/{team1}-vs-{team2}-prediction-team-news-lineups_{id}.html | 阵容新闻 |
| footballexplorer | https://www.footballexplorer.com/en/world-cup-2026/matches/{team1}-vs-{team2} | 球队新闻 |

## 其他补充源

| 来源 | URL |
|------|-----|
| FootyStats 世界杯 | https://footystats.org/world-cup |
| thestatsdontlie | https://www.thestatsdontlie.com/football/world-cup-2026/ |
| watchathletics 赛程 | https://www.watchathletics.com/page/7790/fifa-world-cup-2026-fixtures-results-full-match-schedule-and-knockout-bracket |
| fifawc-2026.com | https://www.fifawc-2026.com/full-match-schedule/ |
| flashscore | https://www.flashscore.com/ |
| soccerway | https://us.soccerway.com/ |
| soccer26live 阵容追踪 | https://soccer26live.com/world-cup-2026/squads/announcement-tracker/ |

## 提取策略建议

### 从 FBref 获取球队世界杯数据
1. 打开 https://fbref.com/en/comps/1/schedule/World-Cup-Scores-and-Fixtures
2. 找到目标比赛，点击球队名称跳转到球队统计页
3. 从球队统计页提取：
   - Standard Stats 表：出场、进球、助攻、射门
   - Goalkeeping 表：扑救、零封、PSxG+/-
   - Shooting 表：射门细节、xG
4. 点击比赛详情页获取单场 xG

### 从 365Scores 获取实时数据
- 搜索"Portugal vs Uzbekistan 365Scores"获取比赛专用页面
- 页面含：阵容预测、H2H、近期状态、赔率

### 从 soccergraph 获取身价对比
- 直接抓取 https://www.soccergraph.com/2026/05/fifa-world-cup-2026-all-48-team-market-values-full-ranking.html
- 提取：总身价、平均身价、球员数
- 身价差距>3倍 → 实力悬殊（如 England €1.345B vs 低排名球队 €50M）
