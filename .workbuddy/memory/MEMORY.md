# 项目记忆 — wc2026-reports

## 自动化架构

### 自动化任务列表
| 名称 | ID | 调度 | 状态 |
|------|-----|------|------|
| 世界杯复盘 | automation-1781255922826 | 每日12:00 | ACTIVE |
| 2026世界杯 | automation-1781220477234 | 每日18:00 | ACTIVE |
| 热词解释 | automation-1781015821249 | 每日09:00 | PAUSED |

### 世界杯复盘 Skill
- 位置: `.workbuddy/skills/worldcup-review/SKILL.md`
- 包含完整6步复盘方法论（找比赛→采赛果→读预测→复盘分析→输出交付→记忆更新）
- 自动化 prompt 精简为触发指令（~225字），方法论在 skill 中维护
- **2026-06-17 根治**：此前因 prompt 过长（2173字）导致自动化超时被取消

### 部署信息
- GitHub Pages: https://cocro1.github.io/wc2026-reports/
- CloudStudio: https://4ba4efb5528941e79173f029176fe567.app.codebuddy.work
- 仓库: https://github.com/cocro1/wc2026-reports

### 文件结构约定
- 预测报告: `reports/report-YYYY-MM-DD-teamA-teamB.html`
- 复盘报告: `reports/review-YYYY-MM-DD-teamA-teamB.html`
- Obsidian输出: `D:\我的坚果云\OB笔记\自媒体\fwc2026\`
- Index: `index.html` (REPORTS + REVIEWS 两个数组)

### 设计规范
- 主色: #0033A0 | 辅色: #85B7EB | 网格: 1px #000 | 留白≥65%
- 禁止渐变/阴影/暖色调
- 禁止"由AI生成""自动生成""数妙妙"等字眼
