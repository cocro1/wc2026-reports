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
from pathlib import Path

CUTOFF_DATE = '2026-06-23'


def parse_review_scores(reports_dir):
    """Parse review HTMLs -> {frozenset(ta,tb): 'a-b'} actual scores"""
    scores = {}

    for f in sorted(glob.glob(os.path.join(reports_dir, 'review-*.html'))):
        with open(f, 'r', encoding='utf-8') as fh:
            html = fh.read()

        names = re.findall(r'<div class="name">(.+?)</div>', html)
        if len(names) < 2:
            continue
        team_a, team_b = names[0], names[1]

        actual_match = re.search(
            r'<span class="badge badge-red">实际</span>.*?'
            r'<div class="score-num"[^>]*>(\d+)</div>\s*'
            r'<div class="score-vs"[^>]*>:</div>\s*'
            r'<div class="score-num"[^>]*>(\d+)</div>',
            html, re.DOTALL
        )

        if actual_match:
            score_a, score_b = actual_match.group(1), actual_match.group(2)
        else:
            continue

        key = frozenset([team_a, team_b])
        scores[key] = f'{score_a}-{score_b}'

    return scores


def norm_score(score_str):
    """Normalize score string: '2-1', '2:1', '2 - 1' → '2-1'"""
    if not score_str:
        return ''
    s = re.sub(r'\s+', '', score_str)
    s = s.replace(':', '-')
    return s


def calc_hit_rates(base_dir='.'):
    """Calculate prediction, simulation, and over25 hit rates from June 23 onwards.

    Args:
        base_dir: project root directory (default: current directory)

    Returns:
        dict with hit rate statistics (prediction_hit_rate, simulation_hit_rate,
        over25_hit_rate, plus counts and detail)
    """
    base = Path(base_dir)
    reports_dir = str(base / 'reports')

    # 1. Parse actual scores
    actual_scores = {}

    # Source 1: match_results.json (manual, highest priority)
    mr_path = base / 'match_results.json'
    if mr_path.exists():
        mr_data = json.loads(mr_path.read_text(encoding='utf-8'))
        for key, score in mr_data.items():
            parts = re.split(r'\s+vs\s+', key)
            if len(parts) == 2:
                actual_scores[frozenset(parts)] = score.strip()

    # Source 2: parse review HTMLs as fallback
    review_scores = parse_review_scores(reports_dir)
    for k, v in review_scores.items():
        if k not in actual_scores:
            actual_scores[k] = v

    # 2. Load data files
    md_path = base / 'match_data.json'
    sim_path = base / 'simulation_scores.json'
    o25_path = base / 'over25_data.json'

    match_data = json.loads(md_path.read_text(encoding='utf-8')) if md_path.exists() else []
    sim_scores = json.loads(sim_path.read_text(encoding='utf-8')) if sim_path.exists() else {}
    over25_data = json.loads(o25_path.read_text(encoding='utf-8')) if o25_path.exists() else {}

    # 3. Calculate hit rates
    pred_total = pred_hits = 0
    sim_total = sim_hits = 0
    over_total = over_hits = 0
    detail = []

    for m in match_data:
        date = m.get('date', '')
        if date < CUTOFF_DATE:
            continue

        title = m.get('title', '')
        title_clean = re.sub(r'预测\s*\|', '', title)
        title_clean = re.sub(r'预测$', '', title_clean)
        teams_m = re.match(r'(.+?)\s+vs\s+(.+?)(?:\s+[A-Z]组|\s*$)', title_clean)
        if not teams_m:
            continue
        team_a = teams_m.group(1).strip()
        team_b = teams_m.group(2).strip()
        key = frozenset([team_a, team_b])

        actual = actual_scores.get(key)
        if not actual:
            continue

        actual_norm = norm_score(actual)

        # Prediction check
        pred = m.get('prediction', '')
        pred_score_m = re.search(r'(\d+\s*-\s*\d+)', norm_score(pred)) if pred else None
        pred_n = pred_score_m.group(1) if pred_score_m else norm_score(pred)
        alt_n = norm_score(m.get('alt_score', ''))
        hit_pred = (pred_n == actual_norm or alt_n == actual_norm)

        # Simulation check
        sim_list = sim_scores.get(f'{team_a} vs {team_b}', []) or sim_scores.get(f'{team_b} vs {team_a}', [])
        sim_hit = any(norm_score(s) == actual_norm for s in sim_list)

        # Over 2.5 check
        over_hit = None
        over25_pct = None
        pred_over = None
        actual_total = None
        actual_over = None
        over25_entry = over25_data.get(f'{team_a} vs {team_b}')
        if over25_entry:
            over25_pct = over25_entry['over25']
            pred_over = over25_pct > 50
            parts = actual_norm.split('-')
            actual_total = int(parts[0]) + int(parts[1]) if len(parts) == 2 else 0
            actual_over = actual_total > 2
            over_hit = (pred_over == actual_over)

        detail.append({
            'match': f'{team_a} vs {team_b}',
            'date': date,
            'actual': actual_norm,
            'actual_total': actual_total if over25_entry else 0,
            'over25_pct': over25_pct,
            'pred_over': pred_over,
            'actual_over': actual_over,
            'prediction': pred_n,
            'alt_score': alt_n,
            'pred_hit': hit_pred,
            'sim_scores': sim_list,
            'sim_hit': sim_hit,
            'over_hit': over_hit,
        })

        if pred_n or alt_n:
            pred_total += 1
            if hit_pred:
                pred_hits += 1

        if sim_list:
            sim_total += 1
            if sim_hit:
                sim_hits += 1

        if over25_entry and over_hit is not None:
            over_total += 1
            if over_hit:
                over_hits += 1

    return {
        'prediction_hit_rate': round(pred_hits / pred_total * 100) if pred_total > 0 else 0,
        'simulation_hit_rate': round(sim_hits / sim_total * 100) if sim_total > 0 else 0,
        'over25_hit_rate': round(over_hits / over_total * 100) if over_total > 0 else 0,
        'prediction_hits': pred_hits,
        'prediction_total': pred_total,
        'simulation_hits': sim_hits,
        'simulation_total': sim_total,
        'over25_hits': over_hits,
        'over25_total': over_total,
        'cutoff_date': CUTOFF_DATE,
        'detail': detail,
    }


def main():
    result = calc_hit_rates()

    print(f'\n=== 预测比分命中率 (6/23起) ===')
    print(f'  命中: {result["prediction_hits"]}/{result["prediction_total"]} = {result["prediction_hit_rate"]}%')

    print(f'\n=== 推演比分命中率 (6/23起) ===')
    print(f'  命中: {result["simulation_hits"]}/{result["simulation_total"]} = {result["simulation_hit_rate"]}%')

    print(f'\n=== 大球概率命中率 (6/23起) ===')
    print(f'  命中: {result["over25_hits"]}/{result["over25_total"]} = {result["over25_hit_rate"]}%')

    print(f'\n=== 逐场明细 ===')
    for d in result['detail']:
        status = '✅' if d['pred_hit'] else ('❌' if d['prediction'] or d['alt_score'] else '—')
        sim_status = '✅' if d['sim_hit'] else ('❌' if d['sim_scores'] else '—')
        over_info = ''
        if d['over25_pct'] is not None:
            over_info = f' 大球概率={d["over25_pct"]}% 预测{"大" if d["pred_over"] else "小"} 实际{"大" if d["actual_over"] else "小"}={"✅" if d["over_hit"] else "❌"}'
        print(f'  {d["date"]} {d["match"]}')
        print(f'    实际: {d["actual"]} | 预测: {d["prediction"] or "无"} | 备选: {d["alt_score"] or "无"}')
        print(f'    预测命中: {status}  推演: {d["sim_scores"]} {sim_status}{over_info}')

    with open('hit_rates.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f'\nWrote hit_rates.json')
    print(f'  prediction_hit_rate: {result["prediction_hit_rate"]}')
    print(f'  simulation_hit_rate: {result["simulation_hit_rate"]}')
    print(f'  over25_hit_rate: {result["over25_hit_rate"]}')


if __name__ == '__main__':
    main()
