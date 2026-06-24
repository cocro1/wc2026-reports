# 校对报告 — 2026-06-24（18:30 定时执行）

**校对范围**：2026-06-25 6 场 A/B/C 组第 3 轮预测报告（HTML + MD + Dixon-Coles 汇总）

**校对方法**：schedule.json 交叉核对 + Excel 权威赛程（`D:/我的坚果云/OB笔记/自媒体/fwc2026/content/new/2026FIFA世界杯赛程表_完整版.xlsx`）+ venue_timezones.json 验证

---

## 📊 综合校对结果

| 类别 | 通过率 | 详情 |
|------|--------|------|
| 6 份 HTML 报告 | ✅ 100% | 9 项校验全部通过 |
| 6 份 MD 笔记 | ✅ 100% | 8 项校验全部通过 |
| Dixon-Coles 汇总 MD | ✅ 100% | 5 项校验全部通过 |

---

## 🔍 发现并修复的关键问题

### 严重错误（影响首页显示）

**1. 概率表方向错位 ×3 份** ❌→✅

`scotland-brazil.html`、`czech-mexico.html`、`south-africa-south-korea.html` 三份报告的概率表列名顺序与 `schedule.json` 的 team_a 错位。

- 例：`south-africa-south-korea.html` 原本写「韩国胜 62% / 平 23% / 南非胜 15%」
- 修复后：「南非胜 15% / 平 23% / 韩国胜 62%」

**影响**：`build_site.py` 把第 1 列当 `a_win`、第 3 列当 `b_win`，原方向会导致 index.html 首页胜率数字颠倒，违反铁律7「比分方向必须与卡片球队位置一致」。

**2. 时区转换错误 ×3 份** ❌→✅

`morocco-haiti.html`、`czech-mexico.html`、`south-africa-south-korea.html` 三份报告的当地时间和北京时间错误。

| 报告 | 报告写 | Excel 权威 | 修复 |
|------|--------|-----------|------|
| morocco-haiti | 15:00 ET / 03:00 BJ | 18:00 ET / 06:00 BJ | ✅ 已改 |
| czech-mexico | 21:00 CST / 09:00 BJ | 19:00 CST / 09:00 BJ | ✅ 已改 |
| south-africa-south-korea | 21:00 CST / 09:00 BJ | 19:00 CST / 09:00 BJ | ✅ 已改 |

**根因**：墨西哥 CST (UTC-6) 与美国 CT (UTC-5) 不同，写报告时把 ET 21:00 直接套用成「21:00 CST」而未做时区转换。

### 格式问题（违反铁律7「比分必须带球队名」）

**3. 备选比分不带球队名 ×4 份** ❌→✅

`switzerland-canada.html`、`bosnia-qatar.html`、`morocco-haiti.html`、`czech-mexico.html` 四份报告的「备选比分1/2」段落只写比分数字。

修复示例（czech-mexico）：
- 修复前：`<p>备选比分1：1-0（概率 ~13%）</p>`
- 修复后：`<p>备选比分1：墨西哥 1-0 捷克（概率 ~13%）</p>`

**方向遵循主预测**：备选比分方向与主预测一致（主预测 team_b 在左则备选 team_b 也在左）。

---

## ✅ 通过的校验项

### 6 份 HTML 报告（9 项）
1. 标题含双方 + 分组
2. 概率表方向（与 schedule.json team_a 一致）
3. 概率总和 = 100%
4. 北京时间 = schedule.json
5. 无违禁词（"由 WorkBuddy"/"由AI生成"/"自动化任务"/"数妙妙"/"数据分析师"）
6. 主预测含双方名 + 比分格式
7. 备选1带球队名
8. 备选2带球队名
9. 含「教练视角」板块（3 个教练）

### 6 份 MD 笔记（8 项）
1. 文件名规范（`2026-06-25-{slug}-prediction.md`）
2. 含日期 + 北京时间
3. 无违禁词
4. 含「数据仅供参考」免责提示
5. 主预测含双方（`**球队A X-Y 球队B**` 双向匹配）
6. 概率总和 = 100%
7. 含正确分组（A/B/C）
8. 含场馆（中文/英文）

### Dixon-Coles 汇总 MD（5 项）
1. 无违禁词
2. 含免责提示
3. 含日期 2026-06-25
4. 含全部 12 支球队名
5. 含 29 处粗体比分标注

---

## 📅 比赛信息总览（6 场 A/B/C 组第 3 轮）

| 北京时间 | 比赛 | 分组 | 场馆 | 时区 |
|---------|------|------|------|------|
| 03:00 | 瑞士 vs 加拿大 | B | BC Place, Vancouver | PT (UTC-7) |
| 03:00 | 波黑 vs 卡塔尔 | B | Lumen Field, Seattle | PT (UTC-7) |
| 06:00 | 摩洛哥 vs 海地 | C | Mercedes-Benz Stadium, Atlanta | ET (UTC-4) |
| 06:00 | 苏格兰 vs 巴西 | C | Hard Rock Stadium, Miami | ET (UTC-4) |
| 09:00 | 捷克 vs 墨西哥 | A | Estadio Azteca, Mexico City | CST (UTC-6) |
| 09:00 | 南非 vs 韩国 | A | Estadio BBVA, Monterrey | CST (UTC-6) |

---

## 🎯 主要预测

| 比赛 | 最可能比分 | 主胜 | 平 | 客胜 | 置信度 |
|------|-----------|------|-----|------|--------|
| 瑞士 vs 加拿大 | 加拿大 2-1 瑞士 | 34% | 28% | 38% | 中 |
| 波黑 vs 卡塔尔 | 波黑 2-1 卡塔尔 | 52% | 27% | 21% | 中-高 |
| 摩洛哥 vs 海地 | 摩洛哥 3-0 海地 | 87% | 9% | 4% | 高 |
| 苏格兰 vs 巴西 | 巴西 2-0 苏格兰 | 11% | 18% | 71% | 高 |
| 捷克 vs 墨西哥 | 墨西哥 2-0 捷克 | 13% | 22% | 65% | 高 |
| 南非 vs 韩国 | 韩国 2-1 南非 | 15% | 23% | 62% | 中-高 |

---

## 📝 经验教训

1. **概率表方向是常见错误**：报告生成时把「胜方/热门方」放在第 1 列更易读，但 `build_site.py` 解析时按 schedule.json 顺序（第 1 列 = team_a）取值。需要确保「热门方不一定是 team_a」时手动调整方向。

2. **墨西哥时区特殊**：墨西哥已取消夏令时，Guadalajara/Mexico City/Monterrey 全年 CST (UTC-6)。**不能** 把 ET 21:00 直接套用为「21:00 CST」，实际是 19:00 CST（ET-CST=2h）。

3. **备选比分格式**：铁律7要求所有比分必须带球队名，备选比分不能例外。build_site.py 通过 `(\d+\s*[-:]\s*\d+)` 提取数字，但人工阅读时不带球队名会造成歧义。

4. **Dixon-Coles 汇总 MD 的 `**X-X**` 格式**：必须严格使用 `**X-X**` 粗体格式（在表格内），便于后续脚本解析提取主预测。

---

## 📁 校对范围文件

**6 份 HTML 报告**（已修复）：
- `reports/report-2026-06-25-switzerland-canada.html`
- `reports/report-2026-06-25-bosnia-qatar.html`
- `reports/report-2026-06-25-morocco-haiti.html`
- `reports/report-2026-06-25-scotland-brazil.html`
- `reports/report-2026-06-25-czech-mexico.html`
- `reports/report-2026-06-25-south-africa-south-korea.html`

**6 份 MD 笔记**（OB 库）：
- `D:\我的坚果云\OB笔记\自媒体\fwc2026\content\predictions\2026-06-25-{slug}-prediction.md`

**1 份 Dixon-Coles 汇总**：
- `D:\我的坚果云\OB笔记\自媒体\fwc2026\content\dixon-coles-monte-carlo\2026-06-25_worldcup-dixon-coles-predictions.md`

---

**校对执行**：2026-06-24 13:10 GMT+8
**校对工具**：schedule.json + Excel 权威赛程 + venue_timezones.json + Python regex
**校对范围**：13 份文件（6 HTML + 6 MD + 1 Dixon-Coles 汇总）
**问题总数**：3 类共 10 处错误（全部已修复）
