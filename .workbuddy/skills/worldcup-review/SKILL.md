---
name: worldcup-review
description: "2026世界杯赛后复盘自动化技能。对已完赛且有预测报告的比赛进行系统复盘：采集赛果、逐项核对预测、深度偏差分析、生成HTML+Markdown双格式复盘报告、更新index.html、Git推送、CloudStudio部署。"
agent_created: true
---

# 2026世界杯赛后复盘技能

## 项目上下文
- 工作目录: `C:\Users\cocro\WorkBuddy\wc2026-reports`
- 预测报告: `reports/report-YYYY-MM-DD.html`
- 复盘报告: `reports/review-YYYY-MM-DD.html`
- 首页: `index.html`
- Obsidian输出: `D:\我的坚果云\OB笔记\自媒体\fwc2026\`

## 执行流程

### 第一步：确定需要复盘的比赛
1. 列出 `reports/` 下所有预测报告 (report-YYYY-MM-DD*.html)
2. 检查对应复盘是否已存在 (review-YYYY-MM-DD*.html)
3. 只处理预测报告存在但复盘缺失的比赛
4. 如果某天所有比赛都已有复盘，输出"无新比赛需要复盘"并终止

### 第二步：采集实际赛果
对每场需要复盘的比赛，从以下来源获取赛果：
- WebSearch: 搜索 "TeamA TeamB World Cup 2026 June DD result score"
- WebFetch: ESPN, FIFA, FlashScore, 365Scores 等页面
- 采集数据：最终比分、进球者(含分钟)、xG、控球率、关键事件

### 第三步：读取原始预测报告
- 读取对应 `report-YYYY-MM-DD*.html`
- 提取关键预测项：赛果、比分、关键球员、战术判断、进球数

### 第四步：复盘分析

#### 4.1 核心对比
- 预测比分 vs 实际比分
- 胜平负预测 vs 实际赛果
- 大小球判断 vs 实际进球数
- 备选比分是否覆盖实际结果

#### 4.2 逐项核对 (约15-20项)
- ✅ 命中 / ⚠️ 部分命中 / ❌ 偏差
- 每条标注预测内容和实际发生
- 统计命中率

#### 4.3 偏差原因深度分析 (4-5条)
禁止表面归因，追溯到：
- 数据采集环节问题
- 分析方法问题（线性推演？过度平均主义？对手强度校准？）
- 模型盲区

#### 4.4 概率校准评估
- 预测概率 vs 实际赛果对比
- "过度平均主义"诊断
- 概率诚实度评价

#### 4.5 缺失数据清单
预测时未采集的关键数据，标注严重程度(高/中/低)

#### 4.6 优化建议 (5-7条)
每条包含：问题描述 + 操作方案 + 预期效果

#### 4.7 各维度评分 (1-10)
1. 赛前信息准确性 2. 战术框架判断 3. 球员信息覆盖
4. 数据深度 5. 概率模型 6. 比分预测
7. 不确定性表达 8. 结构化程度

#### 4.8 最终结论
- 总体评价 (1-10分)
- 核心缺陷 (3条以内)
- 核心改进方向

### 第五步：输出交付

#### 5.1 生成HTML复盘报告
- 文件: `reports/review-YYYY-MM-DD-teamA-teamB.html`
- 样式: 蓝色 #0033A0 主色调、卡片式布局
- CSS命名: card, badge-green/red/yellow/blue/gray, hit-row/miss-row/partial-row

#### 5.2 生成Markdown复盘 (Obsidian)
- 文件: `D:\我的坚果云\OB笔记\自媒体\fwc2026\review-YYYY-MM-DD-teamA-teamB.md`
- teamA/teamB: 英文名全小写，空格换连字符
- 纯Markdown格式

#### 5.3 更新 index.html
- 找到对应 REPORTS 条目，更新 `actual: true`, `actualScore`, `prediction` 字段
- 在 REVIEWS 数组开头插入复盘条目（按日期倒序）

#### 5.4 Git推送
```bash
cd C:\Users\cocro\WorkBuddy\wc2026-reports
git add -A
git commit -m "复盘: YYYY-MM-DD比赛日N场完赛更新"
git push origin main
```
仓库: https://github.com/cocro1/wc2026-reports

#### 5.5 CloudStudio部署
使用 `workbuddy_cloudstudio_deploy` 从 `C:\Users\cocro\WorkBuddy\wc2026-reports` 部署

### 第六步：自动化记忆更新
- 更新 `C:\Users\cocro\WorkBuddy\wc2026-reports\.workbuddy\automations\automation-1781255922826\memory.md`
- 追加执行记录：复盘比赛列表、评分、关键发现、交付物、Git commit hash、部署URL
- 更新 `C:\Users\cocro\WorkBuddy\wc2026-reports\.workbuddy\memory\YYYY-MM-DD.md`
- 记录当日工作内容

### 设计规范
- 主色: #0033A0 (Cobalt Blue)
- 辅色: #85B7EB (Sky Blue)
- 网格线: 1px #000000
- 留白: ≥65%
- 无渐变、无阴影、无暖色调
- 页脚: "报告数据仅供参考，不构成投注建议"
- 禁止出现"由AI生成""自动生成""数妙妙"等字眼
