# 项目记忆 — wc2026-reports

## 自动化架构

### 自动化任务列表（2026-06-22 拆分为3步流水线）
| 名称 | ID | 调度 | 状态 |
|------|-----|------|------|
| 世界杯复盘 | automation-1781255922826 | 每日12:00 | ACTIVE |
| 写文稿-2026世界杯 | automation-1782113868431 | 每日17:30 | ACTIVE |
| 校对文稿-2026世界杯 | automation-1782113912520 | 每日18:30 | ACTIVE |
| 网站发布-2026世界杯 | automation-1782113961671 | 每日19:30 | ACTIVE |
| 2026世界杯（旧） | automation-1781220477234 | 每日18:00 | PAUSED |
| 热词解释 | automation-1781015821249 | 每日09:00 | PAUSED |

### 预测流水线（写→校→发）
1. **写文稿** (17:30)：数据采集+分析+生成HTML/MD报告。只写文件，不更新index/不部署。
2. **校对文稿** (18:30)：**核心是数据准确性校验**（赛程表、对战双方、比分），其次扫违禁词/格式/一致性。**两条铁律**：(a) 所有时间必须以北京时间(GMT+8)为准；(b) 赛程/对阵/比分必须与FIFA官方交叉核对。自动修复数据错误，生成校对报告到 `.workbuddy/proofreads/`
3. **网站发布** (19:30)：运行 build_site.py → CloudStudio部署 → GitHub推送

### 世界杯复盘 Skill
- 位置: `.workbuddy/skills/worldcup-review/SKILL.md`
- 包含完整6步复盘方法论（找比赛→采赛果→读预测→复盘分析→输出交付→记忆更新）
- 自动化 prompt 精简为触发指令（~225字），方法论在 skill 中维护
- **2026-06-17 根治**：此前因 prompt 过长（2173字）导致自动化超时被取消

### 部署信息
- GitHub Pages: https://cocro1.github.io/wc2026-reports/
- CloudStudio: https://4ba4efb5528941e79173f029176fe567.app.codebuddy.work
- 仓库: https://github.com/cocro1/wc2026-reports

### 数据采集技能
- 位置: `.workbuddy/skills/wc2026-data-sources/`
- 增强数据源: FBref (xG/球员)、xGscore、Transfermarkt(身价)、FIFA 官网、365Scores
- 数据质量标注: L1(一手) > L2(聚合) > L3(二手分析) > L4(推断)
- 采集检查清单: 15项自检 + 10阶段工作流

### 文件结构约定
- 预测报告: `reports/report-YYYY-MM-DD-teamA-teamB.html`
- 复盘报告: `reports/review-YYYY-MM-DD-teamA-teamB.html`
- Obsidian输出: `D:\我的坚果云\OB笔记\自媒体\fwc2026\`
- Index: `index.html` (REPORTS + REVIEWS 两个数组)
- **赛程数据源**: `schedule.json` — 73场小组赛完整赛程（北京时间，但非绝对权威，需与FIFA官方交叉核对）
- **预测数据源**: `match_data.json` — 由 build_site.py 从 reports/ 生成
- **首页合并逻辑**: index.html 先加载 schedule.json（赛程），再加载 match_data.json（预测），按队名模糊匹配合并。有预测显示预测，无预测显示"待发布"

### 校对铁律（2026-06-22 用户明确要求）
1. **所有时间必须以北京时间为准（GMT+8）**：信息源如用UTC/EST等时区，必须换算为北京时间后写入
2. **数据准确性是校对核心**：赛程表、对战双方、比分——这三项如有错误必须立即修正，与FIFA官方交叉核对
3. 2026世界杯有12个小组(A-L)，每组4队，共48队。小组归属错误是常见问题
4. **文件命名日期以北京时间为准（不可协商）**：文件名中的 YYYY-MM-DD 必须与北京时间日期一致（对照 schedule.json）。例如：比赛在北京时间6月23日凌晨开赛，文件名应为2026-06-23而非美东时间的6月22日。不一致时必须重命名修正。**这条规则在生成/校对每个文件时必须手动核查**
5. **schedule.json不是绝对权威**：如schedule.json与外部源(FIFA官网/ESPN)不一致，必须用FIFA官方源(fifawc-2026.com)做最终仲裁。2026-06-22发现schedule.json有4处日期错误（跨日比赛归属错误），盲信schedule.json导致错误扩散

### 时区安全规范（2026-06-22 建立防错机制）
**这是最频繁出错的环节，必须严格遵守：**
- 北美跨4个时区：ET(UTC-4)/CT(UTC-5)/MT(UTC-6)/PT(UTC-7)，不可统一标注为EDT
- 墨西哥不使用夏令时：Guadalajara/Mexico City/Monterrey 全年CST(UTC-6)，不是美国CT(UTC-5)
- 输出格式：`⏰ 当地时间 时区 (城市当地时间) / 北京时间`
- 场馆时区映射表：`.workbuddy/references/venue_timezones.json` 和 `.workbuddy/skills/wc2026-schedule-timezone/references/venue_timezones.json`
- 时区安全技能：`.workbuddy/skills/wc2026-schedule-timezone/SKILL.md`
- 验证来源：goaltimeguide.com/zh（直接标注北京时间）

### 设计规范
- 主色: #0033A0 | 辅色: #85B7EB | 网格: 1px #000 | 留白≥65%
- 禁止渐变/阴影/暖色调
- 禁止"由AI生成""自动生成""数妙妙"等字眼
