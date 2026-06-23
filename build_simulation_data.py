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

# English-to-Chinese team name mapping for simulation data lookup
EN_TO_ZH_TEAM = {
    'Portugal': '葡萄牙', 'Uzbekistan': '乌兹别克斯坦',
    'England': '英格兰', 'Ghana': '加纳',
    'Panama': '巴拿马', 'Croatia': '克罗地亚',
    'Colombia': '哥伦比亚', 'DR Congo': '刚果(金)',
    'Argentina': '阿根廷', 'Austria': '奥地利',
    'France': '伊拉克',  # Actually France → 法国 but not needed for current data
    'Norway': '挪威', 'Senegal': '塞内加尔',
    'Jordan': '约旦', 'Algeria': '阿尔及利亚',
    'Iraq': '伊拉克',
}

def clean_team_name(name: str) -> str:
    """Strip Chinese/English parenthetical group labels and emoji from team names."""
    # Strip Chinese parenthetical group labels: （Group K MD2）, （Group L MD2）etc.
    name = re.sub(r'[（(][^）)]*[）)]', '', name)
    name = strip_emoji(name)
    return name.strip().rstrip('*').strip()

def to_zh_name(name: str) -> str:
    """Translate English team name to Chinese, or return as-is if not in mapping."""
    return EN_TO_ZH_TEAM.get(name, name)

def parse_section_header(line: str):
    """Parse '## 1. Portugal vs Uzbekistan（Group K MD2）' -> ('葡萄牙', '乌兹别克斯坦')"""
    m = re.match(r'^##\s+\d+\.\s*(.+?)\s+vs\s+(.+?)$', line, re.IGNORECASE)
    if not m:
        return None
    a = clean_team_name(m.group(1))
    b = clean_team_name(m.group(2))
    # Translate to Chinese for index.html lookup compatibility
    a = to_zh_name(a)
    b = to_zh_name(b)
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
        # Match: '1. **2-1**（9.7%）' or '2. **1-0 England**（11.1%）' (may have team name after score)
        m = re.match(r'^(\d+)\.\s*\*\*(\d+[-:]\d+)', line)
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
