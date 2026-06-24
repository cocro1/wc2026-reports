"""
Parse Dixon-Coles Monte Carlo simulation MD reports and extract
top-2 predicted exact scores for each match from score recommendation sections.

Handles multiple output formats across different report versions:
  v1 (6/23): **推荐精准比分**（价值排序）：\n1. **2-0**（9.7%）
  v2 (6/24): #### 推荐精准比分（按概率排序）\n1. **2-1**（9.7%）
  v3 (6/25): **推荐比分**（按概率排序）：\n1. **1-1** (8.4%)
  v4 (6/26): **推荐 2-3 个精准比分**：**0-3**（11.2%）、**0-2**（9.7%）

Output: simulation_scores.json — keyed by "teamA vs teamB" team pair.
"""

import json, re, os
from pathlib import Path

SIM_DIR = Path("D:/我的坚果云/OB笔记/自媒体/fwc2026/content/dixon-coles-monte-carlo")
OUT_FILE = Path(__file__).parent / "simulation_scores.json"

def strip_emoji(text: str) -> str:
    """Remove emoji flags and other emoji from team names."""
    return re.sub(r'[\U0001F1E0-\U0001F1FF\u2600-\u27BF\uD83C-\uDBFF\uDC00-\uDFFF]+', '', text).strip()

# English-to-Chinese team name mapping
EN_TO_ZH_TEAM = {
    'Portugal': '葡萄牙', 'Uzbekistan': '乌兹别克斯坦',
    'England': '英格兰', 'Ghana': '加纳',
    'Panama': '巴拿马', 'Croatia': '克罗地亚',
    'Colombia': '哥伦比亚', 'DR Congo': '刚果(金)',
    'Argentina': '阿根廷', 'Austria': '奥地利',
    'France': '法国', 'Norway': '挪威', 'Senegal': '塞内加尔',
    'Jordan': '约旦', 'Algeria': '阿尔及利亚', 'Iraq': '伊拉克',
    # 6/25+6/26新增
    'Switzerland': '瑞士', 'Canada': '加拿大',
    'Bosnia and Herzegovina': '波黑', 'Qatar': '卡塔尔',
    'Scotland': '苏格兰', 'Brazil': '巴西',
    'Morocco': '摩洛哥', 'Haiti': '海地',
    'South Africa': '南非', 'South Korea': '韩国',
    'Czechia': '捷克', 'Mexico': '墨西哥',
    'Curacao': '库拉索', 'Ivory Coast': '科特迪瓦',
    'Ecuador': '厄瓜多尔', 'Germany': '德国',
    'Japan': '日本', 'Sweden': '瑞典',
    'Tunisia': '突尼斯', 'Netherlands': '荷兰',
    'Turkey': '土耳其', 'United States': '美国',
    'Paraguay': '巴拉圭', 'Australia': '澳大利亚',
}

def clean_team_name(name: str) -> str:
    """Strip parenthetical labels, emoji, and whitespace from team names."""
    # Strip all parenthetical content (handles nested/chained parens)
    while re.search(r'[（(][^）)]*[）)]', name):
        name = re.sub(r'[（(][^）)]*[）)]', '', name)
    name = strip_emoji(name)
    return name.strip().rstrip('*').strip()

def to_zh_name(name: str) -> str:
    """Translate English team name to Chinese, or return as-is."""
    return EN_TO_ZH_TEAM.get(name, name)

def parse_section_header(line: str):
    """Parse '## N. TeamA vs TeamB (...)' -> (team_a_cn, team_b_cn)"""
    # Match ## headers: "## 1. 瑞士 vs 加拿大（BC Place 温哥华）"
    m = re.match(r'^##\s+\d+\.\s*(.+?)\s+vs\s+(.+?)(?:[（(]|$)', line, re.IGNORECASE)
    if not m:
        return None
    a = clean_team_name(m.group(1))
    b = clean_team_name(m.group(2))
    a = to_zh_name(a)
    b = to_zh_name(b)
    if a and b and a != b and 'vs' not in a and 'vs' not in b:
        return (a, b)
    return None

def extract_scores_from_line(line: str) -> list:
    """Extract score strings from a line like '**0-3**（11.2%）、**日本 2-1**（5.9%）'"""
    scores = []
    for m in re.finditer(r'\*\*(.+?)\*\*', line):
        content = m.group(1).strip()
        # Skip trigger phrases like "推荐 2-3 个精准比分" or "推荐比分"
        if '推荐' in content or '比分' in content:
            continue
        # Extract score from content (may have team name prefix: "日本 2-1" → "2-1")
        score_m = re.search(r'(\d+[-:]\d+)', content)
        if score_m:
            score = score_m.group(1)
            if score not in scores:
                scores.append(score)
        if len(scores) >= 2:
            break
    return scores

def parse_recommended_scores(lines, start_idx):
    """Parse score recommendation section, return top 2 scores."""
    trigger_line = lines[start_idx].strip()
    scores = []

    # Check for inline format (v4 6/26): all scores on same line
    # "**推荐 2-3 个精准比分**：**0-3**（11.2%）、**0-2**（9.7%）"
    if '推荐' in trigger_line and '比分' in trigger_line:
        inline_scores = extract_scores_from_line(trigger_line)
        if len(inline_scores) >= 2:
            # Remove team name suffixes like "日本 2-1" → "2-1"
            cleaned = []
            for s in inline_scores:
                # If score starts with a non-digit (like "日本 2-1"), strip prefix
                cm = re.match(r'^(\d+[-:]\d+)', s)
                if cm:
                    cleaned.append(cm.group(1))
                else:
                    cleaned.append(s)
            return cleaned[:2]

    # Multi-line format (v1/v2/v3): scores on separate lines
    in_section = False
    for i in range(start_idx, min(start_idx + 20, len(lines))):
        line = lines[i].strip()
        # Trigger detection
        if re.search(r'推荐.*比分', line):
            in_section = True
            # Also check for inline scores on trigger line
            inline = extract_scores_from_line(line)
            scores.extend(inline)
            if len(scores) >= 2:
                return scores[:2]
            continue
        if not in_section:
            continue

        # Match numbered list: "1. **2-1**（9.7%）" or "1. **2-1 瑞士** (8.4%)"
        m = re.match(r'^(\d+)\.\s*\*\*(.+?)\*\*', line)
        if m:
            content = m.group(2).strip()
            # Extract score: may be "2-1" or "2-1 瑞士" or "1:1"
            score_m = re.match(r'(\d+[-:]\d+)', content)
            if score_m:
                s = score_m.group(1)
                if s not in scores:
                    scores.append(s)
                if len(scores) >= 2:
                    return scores[:2]
            continue

        # Stop conditions
        if len(scores) > 0:
            if not line or line.startswith('**') or line.startswith('#'):
                break

    return scores[:2]

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
        if current_teams and re.search(r'推荐.*比分', line):
            scores = parse_recommended_scores(lines, i)
            if len(scores) >= 2:
                key = f"{current_teams[0]} vs {current_teams[1]}"
                results[key] = scores
                rev_key = f"{current_teams[1]} vs {current_teams[0]}"
                results[rev_key] = scores
            current_teams = None

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

    # Deduplicate: keep first occurrence per team pair
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
