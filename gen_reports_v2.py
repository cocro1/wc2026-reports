#!/usr/bin/env python3
"""Generate World Cup prediction reports for June 22, 2026"""
import os, json

REPORTS_DIR = r"C:\Users\cocro\WorkBuddy\wc2026-reports\reports"
MD_DIR = r"D:\我的坚果云\OB笔记\自媒体\fwc2026"
os.makedirs(MD_DIR, exist_ok=True)

# Load match data from JSON
DATA_FILE = os.path.join(os.path.dirname(__file__), "match_data_0622.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    matches = json.load(f)

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{team_a} vs {team_b} — 2026世界杯 {group} 预测报告</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system,"PingFang SC","Microsoft YaHei",sans-serif; background:#f5f7fa; color:#1a1a2e; line-height:1.8; }}
.header {{ background:#0033A0; color:white; padding:32px 24px 28px; text-align:center; border-bottom:4px solid #002070; }}
.header h1 {{ font-size:24px; font-weight:700; letter-spacing:2px; }}
.header p {{ font-size:14px; opacity:0.85; margin-top:8px; }}
.container {{ max-width:960px; margin:0 auto; padding:24px 16px 48px; }}
.match-info {{ background:white; border-radius:10px; box-shadow:0 2px 12px rgba(0,0,0,0.06); padding:28px; margin-bottom:20px; border-left:4px solid #0033A0; }}
.match-info h2 {{ color:#0033A0; font-size:22px; margin-bottom:12px; }}
.match-info .meta {{ font-size:13px; color:#666; line-height:1.8; }}
.match-info .meta strong {{ color:#0033A0; }}
.section {{ background:white; border-radius:10px; box-shadow:0 2px 12px rgba(0,0,0,0.06); padding:28px; margin-bottom:16px; }}
.section h2 {{ font-size:17px; font-weight:700; color:#0033A0; border-bottom:2px solid #e0e8f5; padding-bottom:6px; margin-bottom:14px; }}
.section h3 {{ font-size:15px; font-weight:700; color:#1a1a2e; margin:16px 0 8px; }}
.section p {{ font-size:14px; margin-bottom:10px; }}
.section ul, .section ol {{ margin:8px 0 8px 20px; font-size:14px; }}
.section li {{ margin-bottom:4px; }}
table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:13px; }}
th {{ background:#0033A0; color:white; padding:8px 10px; text-align:left; font-weight:600; }}
td {{ padding:7px 10px; border-bottom:1px solid #e8e8e8; }}
tr:nth-child(even) td {{ background:#f8fafd; }}
.tag {{ display:inline-block; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600; margin-right:4px; }}
.tag-r {{ background:#fde8e8; color:#c62828; }}
.tag-g {{ background:#e8f5e9; color:#2e7d32; }}
.tag-b {{ background:#e3f2fd; color:#0033A0; }}
.tag-o {{ background:#fff3e0; color:#e65100; }}
.tag-y {{ background:#fffde7; color:#f9a825; }}
.prob-box {{ background:#f0f4ff; border-radius:8px; padding:20px; margin:16px 0; }}
.prob-bar {{ display:flex; border-radius:8px; overflow:hidden; height:36px; margin:10px 0; font-size:12px; font-weight:600; text-align:center; line-height:36px; }}
.p-a {{ background:#0033A0; color:white; }}
.p-d {{ background:#85B7EB; color:#1a1a2e; }}
.p-b {{ background:#c5d5f0; color:#1a1a2e; }}
.verdict-box {{ background:#f0f8f0; border-left:4px solid #2e7d32; padding:16px 20px; margin:16px 0; border-radius:4px; }}
.verdict-box strong {{ color:#2e7d32; }}
.warn-box {{ background:#fff8e1; border-left:4px solid #f9a825; padding:12px 16px; margin:12px 0; border-radius:4px; font-size:13px; }}
.coach-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:12px 0; }}
.coach-card {{ background:#f8fafd; border-radius:8px; padding:16px; border:1px solid #e0e8f5; }}
.coach-card h4 {{ color:#0033A0; margin-bottom:8px; font-size:15px; }}
.dim-row {{ display:flex; justify-content:space-between; padding:3px 0; font-size:13px; border-bottom:1px dotted #e0e8f5; }}
.dim-row span:last-child {{ font-weight:700; color:#0033A0; }}
.footer {{ text-align:center; font-size:11px; color:#aaa; padding:24px; border-top:1px solid #eee; margin-top:32px; }}
@media (max-width:700px) {{ .coach-grid {{ grid-template-columns:1fr; }} .section {{ padding:20px 16px; }} }}
</style>
</head>
<body>
<div class="header"><h1>{team_a} vs {team_b}</h1><p>{group} {round} · 预测报告</p></div>
<div class="container">

{content}

<div class="footer">报告数据仅供参考，不构成投注建议</div>
</div>
</body>
</html>'''

SECTION_TEMPLATE = '<div class="section">\n<h2>{title}</h2>\n{body}\n</div>\n'

def make_table(headers, rows):
    h = '<tr>' + ''.join(f'<th>{x}</th>' for x in headers) + '</tr>\n'
    r = ''
    for row in rows:
        r += '<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>\n'
    return f'<table>\n{h}{r}</table>\n'

def make_prob_bar(pa, pd, pb, ta, tb):
    return f'''<div class="prob-box">
<div class="prob-bar">
<div class="p-a" style="width:{pa}%">{ta} {pa}%</div>
<div class="p-d" style="width:{pd}%">平局 {pd}%</div>
<div class="p-b" style="width:{pb}%">{tb} {pb}%</div>
</div>
</div>'''

def make_coach_card(coach, team):
    dims = [
        ("战术哲学与风格", coach["scores"]["tactics"]),
        ("大赛履历与胜率", coach["scores"]["tournament"]),
        ("临场决策能力", coach["scores"]["in_game"]),
        ("危机管理能力", coach["scores"]["crisis"]),
        ("更衣室管控", coach["scores"]["locker"]),
        ("对手研究能力", coach["scores"]["opponent"]),
        ("大赛压力应对", coach["scores"]["pressure"]),
        ("战术灵活性", coach["scores"]["flexibility"]),
    ]
    dim_html = '\n'.join(f'<div class="dim-row"><span>{d}</span><span>{v}/10</span></div>' for d, v in dims)
    return f'''<div class="coach-card">
<h4>{team}主教练——{coach["name"]}</h4>
<p><strong>战术哲学：</strong>{coach["philosophy"]}</p>
<p><strong>大赛履历：</strong>{coach["record"]}</p>
<p><strong>执教胜率（按Tier拆分）：</strong>{coach["tier_record"]}</p>
<p><strong>综合能力评分：</strong></p>
{dim_html}
<p><strong>综合等级：{coach["level"]}</strong></p>
</div>'''

def make_coach_pov(pov, team):
    return f'''<h3>🔄 我是{team}主教练——</h3>
<p><strong>小组形势判断：</strong>{pov["group_assessment"]}</p>
<p><strong>本场战略目标：</strong>{pov["strategic_goal"]}</p>
<p><strong>出线路径规划：</strong></p>
<ul>
<li>最优路径：{pov["best_path"]}</li>
<li>现实路径：{pov["realistic_path"]}</li>
<li>最坏场景预案：{pov["worst_case"]}</li>
</ul>
<p><strong>赛程策略：</strong>{pov["schedule_strategy"]}</p>
<p><strong>针对性策略：</strong></p>
<ul>
<li>对最强对手：{pov["vs_strongest"]}</li>
<li>对最弱对手：{pov["vs_weakest"]}</li>
<li>对同档对手：{pov["vs_equal"]}</li>
</ul>
<p><strong>风险清单：</strong>{pov["risk_list"]}</p>
<p><strong>教练的B计划：</strong>{pov["plan_b"]}</p>'''

def generate_html(m):
    ta, tb = m["team_a"], m["team_b"]
    sections = []

    # Match info
    body = f'<h2>{ta} vs {tb}</h2>\n<div class="meta"><strong>{m["group"]} {m["round"]}</strong><br>⏰ {m["date_local"]} / {m["date_bj"]} 北京时间<br>📍 {m["venue"]}<br>📊 数据更新时间：{m["data_time"]}</div>'
    sections.append(f'<div class="match-info">\n{body}\n</div>')

    # Group standings
    gt = make_table(["#","球队","赛","胜","平","负","进球","失球","GD","积分"], m["group_table"])
    sections.append(SECTION_TEMPLATE.format(title="同组形势", body=gt + f'<p>{m["md1_results"]}</p>'))

    # Recent form
    fa = m["form_a"]
    fb = m["form_b"]
    form_body = f'<h3>{fa["title"]}</h3>\n' + make_table(["对手","比分","赛事","对手档次","评分"], fa["rows"]) + f'<p>{fa["analysis"]}</p>\n'
    form_body += f'<h3>{fb["title"]}</h3>\n' + make_table(["对手","比分","赛事","对手档次","评分"], fb["rows"]) + f'<p>{fb["analysis"]}</p>\n'
    form_body += f'<p>{m["xg_summary"]}</p>'
    sections.append(SECTION_TEMPLATE.format(title="近期状态（对手强度校准后）", body=form_body))

    # Players
    pa_players = m["players_a"]
    pb_players = m["players_b"]
    pl_body = f'<h3>{ta}核心球员（{len(pa_players)}人）</h3>\n' + make_table(["球员","位置","俱乐部","世界杯经验","近期状态","大赛折扣"], pa_players)
    pl_body += f'<h3>{tb}核心球员（{len(pb_players)}人）</h3>\n' + make_table(["球员","位置","俱乐部","世界杯经验","近期状态","大赛折扣"], pb_players)
    sections.append(SECTION_TEMPLATE.format(title="球员覆盖（16-20人/队）", body=pl_body))

    # Lineup uncertainty
    lu_body = f'<p>{m["lineup_uncertainty_a"]}</p>\n<p>{m["lineup_uncertainty_b"]}</p>'
    sections.append(SECTION_TEMPLATE.format(title="首发/替补不确定性", body=lu_body))

    # Attack/Defense
    ad_body = f'<h3>{ta}进攻</h3>\n<p>{m["atk_def_a"]["atk"]}</p>\n<h3>{ta}防守</h3>\n<p>{m["atk_def_a"]["def"]}</p>\n'
    ad_body += f'<h3>{tb}进攻</h3>\n<p>{m["atk_def_b"]["atk"]}</p>\n<h3>{tb}防守</h3>\n<p>{m["atk_def_b"]["def"]}</p>'
    sections.append(SECTION_TEMPLATE.format(title="攻防对比", body=ad_body))

    # Goalkeepers
    gk_body = f'<h3>{ta}门将</h3>\n<p>{m["gk_a"]}</p>\n<h3>{tb}门将</h3>\n<p>{m["gk_b"]}</p>'
    sections.append(SECTION_TEMPLATE.format(title="门将分析", body=gk_body))

    # Fouls
    foul_body = f'<p>{m["fouls_a"]}</p>\n<p>{m["fouls_b"]}</p>\n<div class="warn-box">{m["fouls_impact"]}</div>'
    sections.append(SECTION_TEMPLATE.format(title="犯规率/纪律指数", body=foul_body))

    # Discount
    disc_body = f'<h3>{ta}关键球员折扣系数标注</h3>\n<p>{m["discount_a"]}</p>\n<h3>{tb}关键球员折扣系数标注</h3>\n<p>{m["discount_b"]}</p>'
    sections.append(SECTION_TEMPLATE.format(title="联赛→大赛状态折扣", body=disc_body))

    # Coach
    coach_body = '<div class="coach-grid">\n' + make_coach_card(m["coach_a"], ta) + '\n' + make_coach_card(m["coach_b"], tb) + '\n</div>\n'
    coach_body += f'<div class="warn-box"><strong>⚠️ 教练博弈分析：</strong><br>{m["coach_duel"]}</div>'
    sections.append(SECTION_TEMPLATE.format(title="主教练综合能力评估（V4升级）", body=coach_body))

    # Substitutes
    sub_body = f'<h3>{ta}替补储备</h3>\n<p>{m["sub_a"]}</p>\n<h3>{tb}替补储备</h3>\n<p>{m["sub_b"]}</p>'
    sections.append(SECTION_TEMPLATE.format(title="替补攻击力", body=sub_body))

    # Key matchups
    km_html = '<ul>' + ''.join(f'<li>{km}</li>' for km in m["key_matchups"]) + '</ul>'
    sections.append(SECTION_TEMPLATE.format(title="关键对位", body=km_html))

    # Environment
    env_body = f'<p>{m["env_factors"]}</p>\n<h3>大赛心理/逆转因子</h3>\n<p><strong>{ta}：</strong>{m["psych_a"]}</p>\n<p><strong>{tb}：</strong>{m["psych_b"]}</p>'
    sections.append(SECTION_TEMPLATE.format(title="环境因素", body=env_body))

    # Coach perspective
    cp_body = make_coach_pov(m["coach_pov_a"], ta) + '\n' + make_coach_pov(m["coach_pov_b"], tb)
    cp_body += '<h3>🔄 同组另外两支球队的教练视角（简化版）</h3>\n'
    for ot in m["other_teams"]:
        cp_body += f'<h4>{ot["name"]}</h4><ul><li>小组形势判断：{ot["assessment"]}</li><li>出线路径推演：{ot["path"]}</li><li>对本场两队的策略：{ot["vs_match_teams"]}</li></ul>\n'
    cp_body += f'<div class="warn-box"><strong>⚖️ 教练博弈全景：</strong><br>{m["coach_panorama"]}</div>'
    sections.append(SECTION_TEMPLATE.format(title="教练视角：小组出线形势推演（V4新增）", body=cp_body))

    # Probability
    prob_body = make_prob_bar(m["prob_a"], m["prob_d"], m["prob_b"], ta, tb)
    prob_body += f'<p><strong>概率置信度梯级：</strong>{m["prob_confidence"]}</p>\n<p><strong>各概率信号强度标注：</strong>{m["signals"]}</p>'
    sections.append(SECTION_TEMPLATE.format(title="概率预测", body=prob_body))

    # Score prediction
    sm = m["score_main"]
    sa1 = m["score_alt1"]
    sa2 = m["score_alt2"]
    score_body = f'<div class="verdict-box"><strong>最可能比分：{ta} {sm[0]} {tb}（概率 ~{sm[1]}%）</strong></div>\n'
    score_body += f'<p>备选比分1：{sa1[0]}（概率 ~{sa1[1]}%）</p>\n<p>备选比分2：{sa2[0]}（概率 ~{sa2[1]}%）</p>\n<p><strong>预期 xG 区间：</strong>{m["xg_range"]}</p>'
    sections.append(SECTION_TEMPLATE.format(title="比分预测", body=score_body))

    # Conclusion
    sections.append(SECTION_TEMPLATE.format(title="最终结论", body=f'<p>{m["conclusion"]}</p>'))

    return HTML_TEMPLATE.format(
        team_a=ta, team_b=tb, group=m["group"], round=m["round"],
        content='\n'.join(sections)
    )

def generate_md(m):
    ta, tb = m["team_a"], m["team_b"]

    def md_table(headers, rows):
        h = '| ' + ' | '.join(headers) + ' |\n'
        sep = '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'
        r = ''
        for row in rows:
            r += '| ' + ' | '.join(str(x) for x in row) + ' |\n'
        return h + sep + r

    md = f'# {ta} vs {tb} — 2026世界杯 {m["group"]} 预测报告\n\n'
    md += f'## 比赛信息\n\n'
    md += f'- **双方：** {ta} vs {tb}\n- **时间：** {m["date_local"]} / {m["date_bj"]} 北京时间\n- **地点：** {m["venue"]}\n- **阶段：** {m["group"]} {m["round"]}\n- **数据更新时间：** {m["data_time"]}\n\n'

    md += f'## 同组形势\n\n'
    md += md_table(["#","球队","赛","胜","平","负","进球","失球","GD","积分"], m["group_table"]) + '\n'
    md += f'{m["md1_results"]}\n\n'

    md += f'## 近期状态（对手强度校准后）\n\n'
    fa, fb = m["form_a"], m["form_b"]
    md += f'### {fa["title"]}\n\n' + md_table(["对手","比分","赛事","对手档次","评分"], fa["rows"]) + f'\n{fa["analysis"]}\n\n'
    md += f'### {fb["title"]}\n\n' + md_table(["对手","比分","赛事","对手档次","评分"], fb["rows"]) + f'\n{fb["analysis"]}\n\n'
    md += f'{m["xg_summary"]}\n\n'

    md += f'## 球员覆盖（16-20人/队）\n\n'
    md += f'### {ta}核心球员（{len(m["players_a"])}人）\n\n' + md_table(["球员","位置","俱乐部","世界杯经验","近期状态","大赛折扣"], m["players_a"]) + '\n'
    md += f'### {tb}核心球员（{len(m["players_b"])}人）\n\n' + md_table(["球员","位置","俱乐部","世界杯经验","近期状态","大赛折扣"], m["players_b"]) + '\n'

    md += f'## 首发/替补不确定性\n\n{m["lineup_uncertainty_a"]}\n\n{m["lineup_uncertainty_b"]}\n\n'
    md += f'## 攻防对比\n\n### {ta}进攻\n{m["atk_def_a"]["atk"]}\n\n### {ta}防守\n{m["atk_def_a"]["def"]}\n\n### {tb}进攻\n{m["atk_def_b"]["atk"]}\n\n### {tb}防守\n{m["atk_def_b"]["def"]}\n\n'
    md += f'## 门将分析\n\n### {ta}门将\n{m["gk_a"]}\n\n### {tb}门将\n{m["gk_b"]}\n\n'
    md += f'## 犯规率/纪律指数\n\n{m["fouls_a"]}\n\n{m["fouls_b"]}\n\n> {m["fouls_impact"]}\n\n'
    md += f'## 联赛→大赛状态折扣\n\n### {ta}\n{m["discount_a"]}\n\n### {tb}\n{m["discount_b"]}\n\n'

    # Coach MD
    ca, cb = m["coach_a"], m["coach_b"]
    dims = ["战术哲学与风格","大赛履历与胜率","临场决策能力","危机管理能力","更衣室管控","对手研究能力","大赛压力应对","战术灵活性"]
    keys = ["tactics","tournament","in_game","crisis","locker","opponent","pressure","flexibility"]
    md += f'## 主教练综合能力评估（V4升级）\n\n'
    md += f'### {ta}主教练——{ca["name"]}\n\n- 战术哲学：{ca["philosophy"]}\n- 大赛履历：{ca["record"]}\n- 执教胜率：{ca["tier_record"]}\n- 综合能力评分：\n'
    for d, k in zip(dims, keys): md += f'  - {d}：{ca["scores"][k]}/10\n'
    md += f'- 综合等级：{ca["level"]}\n\n'
    md += f'### {tb}主教练——{cb["name"]}\n\n- 战术哲学：{cb["philosophy"]}\n- 大赛履历：{cb["record"]}\n- 执教胜率：{cb["tier_record"]}\n- 综合能力评分：\n'
    for d, k in zip(dims, keys): md += f'  - {d}：{cb["scores"][k]}/10\n'
    md += f'- 综合等级：{cb["level"]}\n\n> 教练博弈分析：{m["coach_duel"]}\n\n'

    md += f'## 替补攻击力\n\n### {ta}\n{m["sub_a"]}\n\n### {tb}\n{m["sub_b"]}\n\n'
    md += f'## 关键对位\n\n' + '\n'.join(f'- {km}' for km in m["key_matchups"]) + '\n\n'
    md += f'## 环境因素\n\n{m["env_factors"]}\n\n### 大赛心理/逆转因子\n\n**{ta}：** {m["psych_a"]}\n\n**{tb}：** {m["psych_b"]}\n\n'

    # Coach perspective MD
    for pov, team in [(m["coach_pov_a"], ta), (m["coach_pov_b"], tb)]:
        md += f'### 🔄 我是{team}主教练——\n\n'
        md += f'- 小组形势判断：{pov["group_assessment"]}\n- 本场战略目标：{pov["strategic_goal"]}\n- 出线路径：最优 {pov["best_path"]} / 现实 {pov["realistic_path"]} / 最坏 {pov["worst_case"]}\n- 赛程策略：{pov["schedule_strategy"]}\n- 针对性策略：强{pov["vs_strongest"]} / 弱{pov["vs_weakest"]} / 同档{pov["vs_equal"]}\n- 风险清单：{pov["risk_list"]}\n- B计划：{pov["plan_b"]}\n\n'

    for ot in m["other_teams"]:
        md += f'#### {ot["name"]}\n- {ot["assessment"]}\n- {ot["path"]}\n- {ot["vs_match_teams"]}\n\n'
    md += f'> 教练博弈全景：{m["coach_panorama"]}\n\n'

    md += f'## 概率预测\n\n| {ta}胜率 | 平局概率 | {tb}胜率 |\n|---------|----------|---------|\n| {m["prob_a"]}% | {m["prob_d"]}% | {m["prob_b"]}% |\n\n'
    md += f'- 概率置信度：{m["prob_confidence"]}\n- 信号强度：{m["signals"]}\n\n'
    sm, sa1, sa2 = m["score_main"], m["score_alt1"], m["score_alt2"]
    md += f'## 比分预测\n\n- **最可能：{ta} {sm[0]} {tb}（~{sm[1]}%）**\n- 备选1：{sa1[0]}（~{sa1[1]}%）\n- 备选2：{sa2[0]}（~{sa2[1]}%）\n- xG区间：{m["xg_range"]}\n\n'
    md += f'## 最终结论\n\n{m["conclusion"]}\n'
    return md

# Generate all reports
for m in matches:
    date = "2026-06-22"
    a_en, b_en = m["team_a_en"], m["team_b_en"]

    html = generate_html(m)
    html_path = os.path.join(REPORTS_DIR, f"report-{date}-{a_en}-{b_en}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML: {html_path}")

    md = generate_md(m)
    md_path = os.path.join(MD_DIR, f"{date}-{a_en}-{b_en}-prediction.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"MD: {md_path}")

print("All 8 files generated!")
