"""
Parse Dixon-Coles Monte Carlo simulation MD reports and extract
top-2 predicted exact scores for each match from "推荐精准比分" sections.

Output: simulation_scores.json — keyed by "teamA vs teamB" team pair.
"""

import json, re, os
from pathlib import Path

SIM_DIR = Path("D:/我的坚果云/OB笔记/自媒体/fwc2026/content/dixon-coles-monte-carlo")
OUT_FILE = Path(__file__).parent / "simulation_scores.json"

def strip_emoji(text: str) -> str:
    """Remove emoji flags and other emoji from team names."""
    # Remove emoji codepoints (flags are regional indicators, others are misc symbols)
    return re.sub(r'[\U0001F1E0-\U0001F1FF\u2600-\u27BF\uD83C-\uDBFF\uDC00-\uDFFF]+', '', text).strip()

def parse_section_header(line: str):
    """Parse '## 1. 阿根廷 🇦🇷 vs 奥地利 🇦🇹' -> ('阿根廷', '奥地利')"""
    m = re.match(r'^##\s+\d+\.\s*(.+?)\s+vs\s+(.+?)$', line, re.IGNORECASE)
    if not m:
        return None
    a = strip_emoji(m.group(1)).strip().rstrip('*').strip()
    b = strip_emoji(m.group(2)).strip().rstrip('*').strip()
    return (a, b)

def parse_recommended_scores(lines, start_idx):
    """Parse '推荐精准比分' section, return top 2 scores."""
    scores = []
    in_section = False
    for i in range(start_idx, min(start_idx + 15, len(lines))):
        line = lines[i].strip()
        if '推荐精准比分' in line:
            in_section = True
            continue
        if not in_section:
            continue
        # Match: '1. **2-1**（9.7% — 最有价值）' or '1. **3-0**（11.2% — 首选）'
        m = re.match(r'^(\d+)\.\s*\*\*(\d+[-:]\d+)\*\*', line)
        if m:
            scores.append(m.group(2))
            if len(scores) >= 2:
                break
        # Stop if we hit a new section / blank line after the list
        if len(scores) > 0 and (not line or line.startswith('**') or line.startswith('#')):
            break
    return scores

def process_md_file(filepath: Path) -> dict:
    """Parse one MD file, return {team_pair_key: [score1, score2], ...}"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = {}
    current_teams = None

    for i, line in enumerate(lines):
        teams = parse_section_header(line)
        if teams:
            current_teams = teams
            continue
        if current_teams and '推荐精准比分' in line:
            scores = parse_recommended_scores(lines, i)
            if len(scores) >= 2:
                key = f"{current_teams[0]} vs {current_teams[1]}"
                results[key] = scores
                # Also store reverse key for matching flexibility
                rev_key = f"{current_teams[1]} vs {current_teams[0]}"
                results[rev_key] = scores
            current_teams = None  # Reset after processing

    return results

def main():
    all_scores = {}
    for fpath in sorted(SIM_DIR.glob("*.md")):
        print(f"Parsing: {fpath.name}")
        result = process_md_file(fpath)
        print(f"  Found {len(set(tuple(v) for v in result.values()))} matches")
        for k, v in result.items():
            print(f"    {k}: {v}")
        all_scores.update(result)

    # Deduplicate: unique team pairs
    unique = {}
    seen_pairs = set()
    for k, v in all_scores.items():
        pair = frozenset(k.split(" vs "))
        if pair not in seen_pairs:
            unique[k] = v
            seen_pairs.add(pair)

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)

    print(f"\nWrote {len(unique)} matches to {OUT_FILE}")

if __name__ == '__main__':
    main()
