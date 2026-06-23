"""
计算预测比分命中率 和 推演比分命中率

规则（用户明确要求）：
- 预测比分命中率：预测比分 OR 备选比分命中实际比分 → 命中
- 推演比分命中率：推演前两名精准比分任一命中实际比分 → 命中
- 只从北京时间 2026-06-23 起计
"""

import json, glob, re, os
from collections import defaultdict

REPORTS_DIR = 'reports'
CUTOFF_DATE = '2026-06-23'


def parse_review_scores():
    """Parse review HTMLs -> {frozenset(ta,tb): 'a-b'} actual scores"""
    scores = {}
    date_map = {}
    
    for f in sorted(glob.glob(f'{REPORTS_DIR}/review-*.html')):
        with open(f, 'r', encoding='utf-8') as fh:
            html = fh.read()
        
        # Extract date from filename or title
        date_m = re.search(r'review-(\d{4}-\d{2}-\d{2})', f)
        date_str = date_m.group(1) if date_m else ''
        
        # Extract team names from score-hero section
        names = re.findall(r'<div class="name">(.+?)</div>', html)
        if len(names) < 2:
            continue
        team_a, team_b = names[0], names[1]
        
        # Extract actual score: find "实际" badge then nearby score-num values
        # The actual score is the second score block (after the "→" arrow)
        score_blocks = re.findall(
            r'<div class="score-num"[^>]*>(\d+)</div>', html
        )
        
        # Structure: pred_home, pred_away, actual_home, actual_away
        # or sometimes just home, away depending on layout
        # The actual score block is after the "实际" badge
        actual_match = re.search(
            r'<span class="badge badge-red">实际</span>.*?<div class="score-num"[^>]*>(\d+)</div>\s*<div class="score-vs"[^>]*>:</div>\s*<div class="score-num"[^>]*>(\d+)</div>',
            html, re.DOTALL
        )
        
        if actual_match:
            score_a, score_b = actual_match.group(1), actual_match.group(2)
        elif len(score_blocks) >= 4:
            # Fallback: last two score-num values are actual
            score_a, score_b = score_blocks[2], score_blocks[3]
        else:
            continue
        
        key = frozenset([team_a, team_b])
        scores[key] = f'{score_a}-{score_b}'
        date_map[key] = date_str
    
    return scores, date_map


def norm_score(score_str):
    """Normalize score string: '2-1', '2:1', '2 - 1' → '2-1'"""
    if not score_str:
        return ''
    s = re.sub(r'\s+', '', score_str)
    s = s.replace(':', '-')
    return s


def main():
    # 1. Parse actual scores from reviews
    actual_scores, review_dates = parse_review_scores()
    print(f'Parsed {len(actual_scores)} review reports with actual scores')
    
    # 2. Load match_data.json (predictions + alt_scores)
    with open('match_data.json', 'r', encoding='utf-8') as f:
        match_data = json.load(f)
    
    # 3. Load simulation_scores.json
    with open('simulation_scores.json', 'r', encoding='utf-8') as f:
        sim_scores = json.load(f)
    
    # 4. Filter to June 23+ matches only
    pred_total = 0
    pred_hits = 0
    sim_total = 0
    sim_hits = 0
    
    detail = []
    
    for m in match_data:
        date = m.get('date', '')
        if date < CUTOFF_DATE:
            continue
        
        # Parse team names from title (e.g. "阿根廷 vs 奥地利 J组" or "阿根廷 vs 奥地利预测 | J组")
        title = m.get('title', '')
        teams_m = re.match(r'(.+?)\s+vs\s+(.+?)(?:\s+预测|\s+[A-Z]组|\s*$)', title)
        if not teams_m:
            continue
        team_a = teams_m.group(1).strip()
        team_b = teams_m.group(2).strip()
        key = frozenset([team_a, team_b])
        
        # Get actual score
        actual = actual_scores.get(key)
        if not actual:
            continue
        
        actual_norm = norm_score(actual)
        
        # Prediction check: prediction OR alt_score must match
        pred = norm_score(m.get('prediction', ''))
        alt = norm_score(m.get('alt_score', ''))
        
        # Extract pure score from "Team 2-0 Team" format
        pred_score = re.search(r'(\d+\s*-\s*\d+)', pred) if pred else None
        if pred_score:
            pred = pred_score.group(1)
        
        pred_matches = (pred or alt) and (pred == actual_norm or alt == actual_norm or (pred and alt and (pred == actual_norm or alt == actual_norm)))
        
        hit_pred = (pred == actual_norm or alt == actual_norm)
        
        # Simulation check: top 1 or top 2 must match
        sim_list = sim_scores.get(f'{team_a} vs {team_b}', []) or sim_scores.get(f'{team_b} vs {team_a}', [])
        sim_hit = any(norm_score(s) == actual_norm for s in sim_list)
        
        detail.append({
            'match': f'{team_a} vs {team_b}',
            'date': date,
            'actual': actual_norm,
            'prediction': pred,
            'alt_score': alt,
            'pred_hit': hit_pred,
            'sim_scores': sim_list,
            'sim_hit': sim_hit,
        })
        
        # Only count if we have prediction data for this match
        if pred or alt:
            pred_total += 1
            if hit_pred:
                pred_hits += 1
        
        if sim_list:
            sim_total += 1
            if sim_hit:
                sim_hits += 1
    
    pred_rate = round(pred_hits / pred_total * 100) if pred_total > 0 else 0
    sim_rate = round(sim_hits / sim_total * 100) if sim_total > 0 else 0
    
    print(f'\n=== 预测比分命中率 (6/23起) ===')
    print(f'  命中: {pred_hits}/{pred_total} = {pred_rate}%')
    
    print(f'\n=== 推演比分命中率 (6/23起) ===')
    print(f'  命中: {sim_hits}/{sim_total} = {sim_rate}%')
    
    print(f'\n=== 逐场明细 ===')
    for d in detail:
        status = '✅' if d['pred_hit'] else ('❌' if d['prediction'] or d['alt_score'] else '—')
        sim_status = '✅' if d['sim_hit'] else ('❌' if d['sim_scores'] else '—')
        print(f'  {d["date"]} {d["match"]}')
        print(f'    实际: {d["actual"]} | 预测: {d["prediction"] or "无"} | 备选: {d["alt_score"] or "无"}')
        print(f'    预测命中: {status}  推演: {d["sim_scores"]} {sim_status}')
    
    # 5. Write hit_rates.json
    result = {
        'prediction_hit_rate': pred_rate,
        'simulation_hit_rate': sim_rate,
        'prediction_hits': pred_hits,
        'prediction_total': pred_total,
        'simulation_hits': sim_hits,
        'simulation_total': sim_total,
        'cutoff_date': CUTOFF_DATE,
        'detail': detail,
    }
    
    with open('hit_rates.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f'\nWrote hit_rates.json')
    print(f'  prediction_hit_rate: {pred_rate}')
    print(f'  simulation_hit_rate: {sim_rate}')


if __name__ == '__main__':
    main()
