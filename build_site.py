#!/usr/bin/env python3
"""Build script for wc2026-reports CloudStudio site (teal theme).
Step 1: Parse reports/*.html → match_data.json
Step 2: Convert content/{mystic,research}/*.md → articles/*.html
"""

import json
import os
import re
import glob
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "reports"
ARTICLES_DIR = BASE_DIR / "articles"
CONTENT_DIR = Path("D:/我的坚果云/OB笔记/自媒体/fwc2026/content")

# ── Teal theme CSS shared across all article pages ──
ARTICLE_CSS = """<style>
:root {
  --teal: #0f766e; --teal-light: #14b8a6; --teal-dark: #115e59;
  --bg: #f0fdfa; --card: #ffffff; --text: #134e4a; --text-dim: #5eead4;
  --border: #ccfbf1; --accent: #f0fdfa;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.85; font-size: 15px;
}
.header {
  background: linear-gradient(135deg, var(--teal-dark), var(--teal));
  color: #fff; padding: 28px 24px 24px; text-align: center;
}
.header h1 { font-size: 22px; font-weight: 700; letter-spacing: 0.5px; }
.header .meta { font-size: 13px; opacity: 0.85; margin-top: 6px; }
.back-link {
  display: inline-block; color: var(--teal); text-decoration: none; font-size: 14px;
  margin-bottom: 16px; font-weight: 600;
}
.back-link:hover { text-decoration: underline; }
.container { max-width: 780px; margin: 0 auto; padding: 24px 16px 64px; }
.content { background: var(--card); border-radius: 12px; padding: 28px 24px;
  box-shadow: 0 1px 4px rgba(15,118,110,0.06); border: 1px solid var(--border); }
.content h2 { font-size: 18px; color: var(--teal); margin: 24px 0 10px; padding-bottom: 6px;
  border-bottom: 2px solid var(--border); }
.content h2:first-child { margin-top: 0; }
.content h3 { font-size: 16px; color: var(--teal-dark); margin: 18px 0 8px; }
.content h4 { font-size: 14px; color: var(--text); margin: 12px 0 6px; }
.content p { margin-bottom: 10px; }
.content ul, .content ol { margin: 8px 0 8px 24px; }
.content li { margin-bottom: 4px; }
.content blockquote {
  border-left: 3px solid var(--teal-light); padding: 8px 16px;
  margin: 12px 0; background: var(--accent); border-radius: 0 8px 8px 0;
  color: var(--teal-dark); font-size: 14px;
}
.content table {
  width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13px;
  border-radius: 8px; overflow: hidden;
}
.content th {
  background: var(--teal); color: #fff; padding: 8px 12px; text-align: left; font-weight: 600;
}
.content td { padding: 7px 12px; border-bottom: 1px solid var(--border); }
.content tr:nth-child(even) td { background: var(--bg); }
.content hr { border: none; border-top: 1px solid var(--border); margin: 20px 0; }
.content strong { color: var(--teal-dark); }
.content code {
  background: var(--accent); padding: 2px 6px; border-radius: 4px;
  font-size: 13px; color: var(--teal-dark);
}
.footer {
  text-align: center; color: var(--text-dim); font-size: 12px;
  padding: 24px 16px; max-width: 780px; margin: 0 auto;
}
@media (min-width: 640px) {
  .content { padding: 32px 40px; }
}
</style>"""


def md_to_html(md_text):
    """Minimal Markdown-to-HTML converter for our article format."""
    lines = md_text.split('\n')
    html = []
    in_list = False
    in_ol = False
    in_table = False
    in_blockquote = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            if in_list:
                html.append('</ul>')
                in_list = False
            if in_ol:
                html.append('</ol>')
                in_ol = False
            if in_table:
                html.append('</tbody></table>')
                in_table = False
            if in_blockquote:
                html.append('</blockquote>')
                in_blockquote = False
            i += 1
            continue

        # Blockquote
        if line.startswith('>'):
            if not in_blockquote:
                html.append('<blockquote>')
                in_blockquote = True
            content = re.sub(r'^>\s*', '', line)
            html.append(f'<p>{inline_md(content)}</p>')
            i += 1
            continue
        elif in_blockquote:
            html.append('</blockquote>')
            in_blockquote = False

        # H1
        if line.startswith('# ') and not line.startswith('## '):
            if in_list: html.append('</ul>'); in_list = False
            if in_ol: html.append('</ol>'); in_ol = False
            html.append(f'<h2>{inline_md(line[2:].strip())}</h2>')
            i += 1
            continue

        # H2
        if line.startswith('## '):
            if in_list: html.append('</ul>'); in_list = False
            if in_ol: html.append('</ol>'); in_ol = False
            html.append(f'<h3>{inline_md(line[3:].strip())}</h3>')
            i += 1
            continue

        # H3
        if line.startswith('### '):
            if in_list: html.append('</ul>'); in_list = False
            if in_ol: html.append('</ol>'); in_ol = False
            html.append(f'<h4>{inline_md(line[4:].strip())}</h4>')
            i += 1
            continue

        # HR
        if line.strip() in ('---', '***', '___'):
            if in_list: html.append('</ul>'); in_list = False
            if in_ol: html.append('</ol>'); in_ol = False
            html.append('<hr>')
            i += 1
            continue

        # Unordered list
        if re.match(r'^[\-\*]\s+', line):
            if in_ol: html.append('</ol>'); in_ol = False
            if not in_list: html.append('<ul>'); in_list = True
            content = re.sub(r'^[\-\*]\s+', '', line)
            html.append(f'<li>{inline_md(content)}</li>')
            i += 1
            continue

        # Ordered list
        if re.match(r'^\d+\.\s+', line):
            if in_list: html.append('</ul>'); in_list = False
            if not in_ol: html.append('<ol>'); in_ol = True
            content = re.sub(r'^\d+\.\s+', '', line)
            html.append(f'<li>{inline_md(content)}</li>')
            i += 1
            continue

        # Table
        if '|' in line and line.strip().startswith('|'):
            if in_list: html.append('</ul>'); in_list = False
            if in_ol: html.append('</ol>'); in_ol = False
            # Check if next line is separator
            is_sep = bool(re.match(r'^\|[\s\-:|]+\|$', line.strip()))
            if not in_table:
                html.append('<table><thead>')
                in_table = True
                # This is header row
                cells = [c.strip() for c in line.split('|')[1:-1]]
                html.append('<tr>' + ''.join(f'<th>{inline_md(c)}</th>' for c in cells) + '</tr>')
                i += 1
                continue
            elif is_sep:
                html.append('</thead><tbody>')
                i += 1
                continue
            else:
                cells = [c.strip() for c in line.split('|')[1:-1]]
                html.append('<tr>' + ''.join(f'<td>{inline_md(c)}</td>' for c in cells) + '</tr>')
                i += 1
                continue
        elif in_table:
            html.append('</tbody></table>')
            in_table = False

        # Bold-only line (section markers starting with **)
        if line.strip().startswith('**') and line.strip().endswith('**'):
            html.append(f'<p><strong>{line.strip()[2:-2]}</strong></p>')
            i += 1
            continue

        # Paragraph
        if in_list: html.append('</ul>'); in_list = False
        if in_ol: html.append('</ol>'); in_ol = False
        html.append(f'<p>{inline_md(line)}</p>')
        i += 1

    # Close open tags
    if in_list: html.append('</ul>')
    if in_ol: html.append('</ol>')
    if in_table: html.append('</tbody></table>')
    if in_blockquote: html.append('</blockquote>')

    return '\n'.join(html)


def inline_md(text):
    """Convert inline markdown: bold, italic, links, code, strikethrough."""
    # Bold+italic first
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'(?<!\*)\*([^\*]+)\*(?!\*)', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def parse_reports():
    """Parse all reports/*.html and extract card-level summary data."""
    matches = []
    for f in sorted(REPORTS_DIR.glob("report-*.html")):
        html = f.read_text(encoding='utf-8')

        # Parse filename: report-YYYY-MM-DD-slug.html
        raw_parts = f.stem.split('-')
        if len(raw_parts) >= 4:
            date_str = f"{raw_parts[1]}-{raw_parts[2]}-{raw_parts[3]}"
        else:
            date_str = "2026-06-01"
        # Team slug = everything after "report-YYYY-MM-DD-"
        match_slug = '-'.join(raw_parts[4:]) if len(raw_parts) >= 5 else f.stem

        # Extract title from <title> tag
        title_m = re.search(r'<title>(.+?)</title>', html)
        title = title_m.group(1) if title_m else f"{team_a} vs {team_b}"

        # Extract group
        group_m = re.search(r'([A-Z])组', title)
        group = group_m.group(1) + '组' if group_m else ''

        # Extract probability — try format A (prob-bar divs) first
        prob_a_m = re.search(r'class="p-a"[^>]*>([^<]+)</div>', html)
        prob_d_m = re.search(r'class="p-d"[^>]*>([^<]+)</div>', html)
        prob_b_m = re.search(r'class="p-b"[^>]*>([^<]+)</div>', html)

        prob_a = prob_a_m.group(1).strip() if prob_a_m else ''
        prob_d = prob_d_m.group(1).strip() if prob_d_m else ''
        prob_b = prob_b_m.group(1).strip() if prob_b_m else ''

        # Format B fallback: <table class="prob"><tr><th>...</th></tr><tr><td class="win">72%</td><td>18%</td><td>10%</td></tr></table>
        if not prob_a:
            pt = re.search(r'<table class="prob">.*?<tr>.*?</tr>\s*<tr>(.*?)</tr>', html, re.DOTALL)
            if pt:
                tds = re.findall(r'<td[^>]*>([^<]+)</td>', pt.group(1))
                if len(tds) >= 3:
                    prob_a, prob_d, prob_b = tds[0].strip(), tds[1].strip(), tds[2].strip()

        # Extract score prediction — try verdict-box first, then table.score format
        score = ''
        score_m = re.search(r'最可能比分[：:]\s*(.+?)(?:（|\(|概率)', html)
        if score_m:
            score = score_m.group(1).strip()
        else:
            # Format B: <td><strong>Portugal 3-0 Uzbekistan</strong></td> in score table
            st = re.search(r'<table class="score">.*?<td>最可能</td>\s*<td><strong>(.+?)</strong></td>', html, re.DOTALL)
            if st:
                score = st.group(1).strip()

        # Extract confidence
        conf_m = re.search(r'置信度[^：:]*[：:]\s*(高|中|低)', html)
        confidence = conf_m.group(1) if conf_m else '中'

        # Extract alt score (备选比分1) — try paragraph format first, then table format
        alt_score = ''
        alt_m = re.search(r'备选比分\d*[：:]\s*(\d+\s*[-:]\s*\d+)', html)
        if alt_m:
            alt_score = alt_m.group(1).strip()
        else:
            # Fallback: parse table.score format — first <td>备选1</td> row
            alt_td_m = re.search(r'<td>备选1</td>\s*<td>(?:<strong>)?(.+?)(?:</strong>)?</td>', html)
            if alt_td_m:
                alt_raw = alt_td_m.group(1).strip()
                # Extract just the score from e.g. "葡萄牙 2-0 乌兹别克斯坦" → "2-0"
                score_m = re.search(r'(\d+\s*[-:]\s*\d+)', alt_raw)
                if score_m:
                    alt_score = score_m.group(1).strip()

        matches.append({
            "date": date_str,
            "file": f"reports/{f.name}",
            "title": title.replace(' — 2026世界杯', '').replace(' 预测报告', '').strip(),
            "slug": match_slug,
            "group": group,
            "prediction": score,
            "alt_score": alt_score,
            "confidence": confidence,
            "a_win": prob_a,
            "draw": prob_d if prob_d else '',
            "b_win": prob_b,
        })

    # Sort by date descending
    matches.sort(key=lambda x: x['date'], reverse=True)
    return matches


def convert_articles():
    """Convert markdown articles to HTML files."""
    articles = {"mystic": [], "research": [], "simulation": []}

    for category in ["mystic", "research", "simulation"]:
        src_dir = CONTENT_DIR / ("dixon-coles-monte-carlo" if category == "simulation" else category)
        if not src_dir.exists():
            continue

        out_dir = ARTICLES_DIR / category
        out_dir.mkdir(parents=True, exist_ok=True)

        for md_file in sorted(src_dir.glob("*.md")):
            md_text = md_file.read_text(encoding='utf-8')
            body_html = md_to_html(md_text)

            # Extract title from first H1
            title_m = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
            page_title = title_m.group(1).strip() if title_m else md_file.stem

            # Clean emojis from title for display
            display_title = page_title

            # Extract date if present
            date_m = re.search(r'生成日期[：:]\s*(\S+)', md_text)
            date_str = date_m.group(1) if date_m else ''

            # Category label
            cat_label = "玄学" if category == "mystic" else ("推演" if category == "simulation" else "专题")

            slug = md_file.stem
            out_path = out_dir / f"{slug}.html"

            full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
{ARTICLE_CSS}
</head>
<body>
<div class="header">
  <h1>{display_title}</h1>
  <div class="meta">{cat_label} · {date_str}</div>
</div>
<div class="container">
  <a href="../index.html#{'mystic' if category == 'mystic' else ('simulation' if category == 'simulation' else 'research')}" class="back-link">← 返回{'玄学' if category == 'mystic' else ('推演' if category == 'simulation' else '专题')}</a>
  <div class="content">
{body_html}
  </div>
</div>
<div class="footer"><p>报告数据仅供参考，不构成投注建议</p></div>
</body>
</html>"""

            out_path.write_text(full_html, encoding='utf-8')

            article_info = {
                "slug": slug,
                "title": display_title.replace('🔮 ', '').replace('📊 ', '').replace('⚽ ', '').strip(),
                "category": category,
                "cat_label": cat_label,
                "date": date_str,
                "file": f"articles/{category}/{slug}.html",
                "preview": md_text[:200].replace('\n', ' ').replace('#', '').strip()[:150] + '...',
            }
            articles[category].append(article_info)

    # Write article index
    (ARTICLES_DIR / "articles_index.json").write_text(
        json.dumps(articles, ensure_ascii=False, indent=2), encoding='utf-8')

    return articles


def calc_hit_rates():
    """Calculate prediction and simulation hit rates from June 23 onwards.
    Data sources (in priority order):
      1. match_results.json — manually maintained actual scores
      2. review-*.html — automated review reports
    """
    CUTOFF = '2026-06-23'
    
    actual_scores = {}
    
    # Source 1: match_results.json (manual, highest priority)
    mr_path = BASE_DIR / "match_results.json"
    if mr_path.exists():
        mr_data = json.loads(mr_path.read_text(encoding='utf-8'))
        for key, score in mr_data.items():
            parts = re.split(r'\s+vs\s+', key)
            if len(parts) == 2:
                actual_scores[frozenset(parts)] = score.strip()
    
    # Source 2: review reports (automated)
    for f in sorted(REPORTS_DIR.glob("review-*.html")):
        html = f.read_text(encoding='utf-8')
        date_m = re.search(r'review-(\d{4}-\d{2}-\d{2})', f.name)
        if not date_m:
            continue
        
        names = re.findall(r'<div class="name">(.+?)</div>', html)
        if len(names) < 2:
            continue
        
        actual_match = re.search(
            r'<span class="badge badge-red">实际</span>.*?'
            r'<div class="score-num"[^>]*>(\d+)</div>\s*'
            r'<div class="score-vs"[^>]*>:</div>\s*'
            r'<div class="score-num"[^>]*>(\d+)</div>',
            html, re.DOTALL
        )
        if actual_match:
            key = frozenset([names[0], names[1]])
            if key not in actual_scores:  # don't overwrite manual data
                actual_scores[key] = f'{actual_match.group(1)}-{actual_match.group(2)}'
    
    # Load match_data and sim_scores
    md_path = BASE_DIR / "match_data.json"
    sim_path = BASE_DIR / "simulation_scores.json"
    
    match_data = json.loads(md_path.read_text(encoding='utf-8')) if md_path.exists() else []
    sim_scores = json.loads(sim_path.read_text(encoding='utf-8')) if sim_path.exists() else {}
    
    pred_hits = pred_total = 0
    sim_hits = sim_total = 0
    
    def _norm(s):
        return re.sub(r'\s+', '', (s or '').replace(':', '-'))
    
    for m in match_data:
        date = m.get('date', '')
        if date < CUTOFF:
            continue
        
        title = m.get('title', '')
        teams_m = re.match(r'(.+?)\s+vs\s+(.+?)(?:\s+预测|\s+[A-Z]组|\s*$)', title)
        if not teams_m:
            continue
        
        ta, tb = teams_m.group(1).strip(), teams_m.group(2).strip()
        key = frozenset([ta, tb])
        actual = actual_scores.get(key)
        if not actual:
            continue
        
        actual_n = _norm(actual)
        
        # Prediction + alt_score
        pred = m.get('prediction', '')
        pred_n = _norm(re.search(r'(\d+\s*-\s*\d+)', pred).group(1) if re.search(r'(\d+\s*-\s*\d+)', pred) else pred)
        alt_n = _norm(m.get('alt_score', ''))
        
        if pred_n or alt_n:
            pred_total += 1
            if pred_n == actual_n or alt_n == actual_n:
                pred_hits += 1
        
        # Simulation top 2
        sim_list = sim_scores.get(f'{ta} vs {tb}', []) or sim_scores.get(f'{tb} vs {ta}', [])
        if sim_list:
            sim_total += 1
            if any(_norm(s) == actual_n for s in sim_list):
                sim_hits += 1
    
    return {
        'prediction_hit_rate': round(pred_hits / pred_total * 100) if pred_total > 0 else 0,
        'simulation_hit_rate': round(sim_hits / sim_total * 100) if sim_total > 0 else 0,
        'prediction_hits': pred_hits,
        'prediction_total': pred_total,
        'simulation_hits': sim_hits,
        'simulation_total': sim_total,
        'cutoff_date': CUTOFF,
    }


def extract_over25():
    """Parse Dixon-Coles simulation HTML articles to extract >2.5 goals probability.
    Returns a dict with forward+reverse lookup keys (Chinese team names)."""
    import glob as _g

    EN_TO_ZH = {
        'Argentina': '阿根廷', 'Austria': '奥地利',
        'France': '法国', 'Iraq': '伊拉克',
        'Jordan': '约旦', 'Algeria': '阿尔及利亚',
        'Norway': '挪威', 'Senegal': '塞内加尔',
        'Portugal': '葡萄牙', 'Uzbekistan': '乌兹别克斯坦',
        'England': '英格兰', 'Ghana': '加纳',
        'Panama': '巴拿马', 'Croatia': '克罗地亚',
        'Colombia': '哥伦比亚', 'DR Congo': '刚果(金)',
    }

    def clean_team(name):
        name = re.sub(r'[（(][^）)]*[）)]', '', name)
        name = re.sub(r'[\U0001F1E0-\U0001F1FF\u2600-\u27BF\uD83C-\uDBFF\uDC00-\uDFFF]+', '', name)
        name = name.strip().rstrip('*').strip()
        return EN_TO_ZH.get(name, name)

    def parse_section_header(line):
        m = re.match(r'^<h3>\s*(\d+)\.\s*(.+?)\s+vs\s+(.+?)\s*</h3>\s*$', line, re.IGNORECASE)
        if not m:
            return None
        return (clean_team(m.group(2)), clean_team(m.group(3)))

    sim_dir = ARTICLES_DIR / "simulation"
    over25 = {}

    for fpath in sorted(_g.glob(str(sim_dir / "*dixon-coles-predictions.html"))):
        with open(fpath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_teams = None
        for line in lines:
            teams = parse_section_header(line.strip())
            if teams:
                current_teams = teams
                continue
            if current_teams and '大于2.5球概率' in line:
                m = re.search(r'(\d+\.?\d*)\s*%', line)
                if m:
                    key = f'{current_teams[0]} vs {current_teams[1]}'
                    over25[key] = {'over25': float(m.group(1))}
                    current_teams = None

    # Add reverse lookup keys
    result = {}
    for k, v in over25.items():
        result[k] = v
        parts = k.split(' vs ')
        if len(parts) == 2:
            result[f'{parts[1]} vs {parts[0]}'] = v

    return result


def main():
    print("=" * 50)
    print("Build site for CloudStudio (teal theme)")
    print("=" * 50)

    # Step 1: Parse reports
    print("\n[1/3] Parsing reports...")
    matches = parse_reports()
    print(f"  Found {len(matches)} report entries")

    # Write match_data.json
    md_path = BASE_DIR / "match_data.json"
    md_path.write_text(json.dumps(matches, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"  Written: {md_path}")

    # Step 2: Convert articles
    print("\n[2/3] Converting articles...")
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    articles = convert_articles()
    for cat, items in articles.items():
        print(f"  {cat}: {len(items)} articles")

    # Step 3: Calculate hit rates
    print("\n[3/5] Calculating hit rates...")
    hit_rates = calc_hit_rates()
    hr_path = BASE_DIR / "hit_rates.json"
    hr_path.write_text(json.dumps(hit_rates, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"  Pred: {hit_rates['prediction_hit_rate']}% ({hit_rates['prediction_hits']}/{hit_rates['prediction_total']})")
    print(f"  Sim:  {hit_rates['simulation_hit_rate']}% ({hit_rates['simulation_hits']}/{hit_rates['simulation_total']})")

    # Step 4: Extract >2.5 goals probability from Dixon-Coles simulation articles
    print("\n[4/5] Extracting >2.5 goals data from simulation articles...")
    over25 = extract_over25()
    o25_path = BASE_DIR / "over25_data.json"
    o25_path.write_text(json.dumps(over25, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"  Extracted >2.5 data for {len(over25)//2} matches ({len(over25)} lookup keys)")

    # Step 5: Summary
    print("\n[5/5] Done!")
    print(f"  Reports: {len(matches)} parsed")
    print(f"  Mystic:  {len(articles.get('mystic', []))} articles")
    print(f"  Simulation: {len(articles.get('simulation', []))} articles")
    print(f"  Research: {len(articles.get('research', []))} articles")
    print(f"\nReady for CloudStudio deploy.")


if __name__ == "__main__":
    main()
