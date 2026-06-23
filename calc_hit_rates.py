"""
计算预测比分命中率、推演比分命中率、大球概率命中率

规则（用户明确要求）：
- 预测比分命中率：预测比分 OR 备选比分命中实际比分 → 命中
- 推演比分命中率：推演前两名精准比分任一命中实际比分 → 命中
- 大球概率命中率：over25概率>50%预测大球，实际总进球>2为大球，预测与实际一致 → 命中
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
    # 1. Parse actual scores from match_results.json (primary) and reviews (fallback)
    actual_scores = {}
    
    # Source 1: match_results.json (manual, highest priority)
    with open('match_results.json', 'r', encoding='utf-8') as f:
        mr_data = json.load(f)
    for key, score in mr_data.items():
        parts = re.split(r'\s+vs\s+', key)
        if len(parts) == 2:
            actual_scores[frozenset(parts)] = score.strip()
    
    # Source 2: parse review HTMLs as fallback
    review_scores, review_dates = parse_review_scores()
    for k, v in review_scores.items():
        if k not in actual_scores:
            actual_scores[k] = v
    print(f'Loaded {len(actual_scores)} actual scores ({len(mr_data)} manual + {len(review_scores)} from reviews)')
    
    # 2. Load match_data.json (predictions + alt_scores)
    with open('match_data.json', 'r', encoding='utf-8') as f:
        match_data = json.load(f)
    
    # 3. Load simulation_scores.json
    with open('simulation_scores.json', 'r', encoding='utf-8') as f:
        sim_scores = json.load(f)
    
    # 4. Load over25_data.json
    with open('over25_data.json', 'r', encoding='utf-8') as f:
        over25_data = json.load(f)
    
    # 5. Filter to June 23+ matches only
    pred_total = 0
    pred_hits = 0
    sim_total = 0
    sim_hits = 0
    over_total = 0
    over_hits = 0
    
    detail = []
    
    for m in match_data:
        date = m.get('date', '')
        if date < CUTOFF_DATE:
            continue
        
        # Parse team names from title — handle both "X vs Y J组" and "X vs Y预测 | K组"
        title = m.get('title', '')
        # First try: strip "预测" suffix and group suffix
        title_clean = re.sub(r'预测\s*\|', '', title)
        title_clean = re.sub(r'预测$', '', title_clean)
        teams_m = re.match(r'(.+?)\s+vs\s+(.+?)(?:\s+[A-Z]组|\s*$)', title_clean)
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
        
        # Over 2.5 goals check
        over25 = over25_data.get(f'{team_a} vs {team_b}')
        over_hit = None
        if over25:
            over25_pct = over25['over25']
            # Predict: >50% → over, ≤50% → under
            pred_over = over25_pct > 50
            # Actual: parse score, total goals > 2.5
            parts = actual_norm.split('-')
            actual_total = int(parts[0]) + int(parts[1]) if len(parts) == 2 else 0
            actual_over = actual_total > 2
            over_hit = (pred_over == actual_over)
        
        detail.append({
            'match': f'{team_a} vs {team_b}',
            'date': date,
            'actual': actual_norm,
            'actual_total': actual_total if over25 else 0,
            'over25_pct': over25['over25'] if over25 else None,
            'pred_over': pred_over if over25 else None,
            'actual_over': actual_over if over25 else None,
            'prediction': pred,
            'alt_score': alt,
            'pred_hit': hit_pred,
            'sim_scores': sim_list,
            'sim_hit': sim_hit,
            'over_hit': over_hit,
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
        
        if over25 and over_hit is not None:
            over_total += 1
            if over_hit:
                over_hits += 1
    
    pred_rate = round(pred_hits / pred_total * 100) if pred_total > 0 else 0
    sim_rate = round(sim_hits / sim_total * 100) if sim_total > 0 else 0
    over_rate = round(over_hits / over_total * 100) if over_total > 0 else 0
    
    print(f'\n=== 预测比分命中率 (6/23起) ===')
    print(f'  命中: {pred_hits}/{pred_total} = {pred_rate}%')
    
    print(f'\n=== 推演比分命中率 (6/23起) ===')
    print(f'  命中: {sim_hits}/{sim_total} = {sim_rate}%')
    
    print(f'\n=== 大球概率命中率 (6/23起) ===')
    print(f'  命中: {over_hits}/{over_total} = {over_rate}%')
    
    print(f'\n=== 逐场明细 ===')
    for d in detail:
        status = '✅' if d['pred_hit'] else ('❌' if d['prediction'] or d['alt_score'] else '—')
        sim_status = '✅' if d['sim_hit'] else ('❌' if d['sim_scores'] else '—')
        over_info = ''
        if d['over25_pct'] is not None:
            over_info = f' 大球概率={d["over25_pct"]}% 预测{"大" if d["pred_over"] else "小"} 实际{"大" if d["actual_over"] else "小"}={"✅" if d["over_hit"] else "❌"}'
        print(f'  {d["date"]} {d["match"]}')
        print(f'    实际: {d["actual"]} | 预测: {d["prediction"] or "无"} | 备选: {d["alt_score"] or "无"}')
        print(f'    预测命中: {status}  推演: {d["sim_scores"]} {sim_status}{over_info}')
    
    # 5. Write hit_rates.json
    result = {
        'prediction_hit_rate': pred_rate,
        'simulation_hit_rate': sim_rate,
        'over25_hit_rate': over_rate,
        'prediction_hits': pred_hits,
        'prediction_total': pred_total,
        'simulation_hits': sim_hits,
        'simulation_total': sim_total,
        'over25_hits': over_hits,
        'over25_total': over_total,
        'cutoff_date': CUTOFF_DATE,
        'detail': detail,
    }
    
    with open('hit_rates.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f'\nWrote hit_rates.json')
    print(f'  prediction_hit_rate: {pred_rate}')
    print(f'  simulation_hit_rate: {sim_rate}')
    print(f'  over25_hit_rate: {over_rate}')


if __name__ == '__main__':
    main()
