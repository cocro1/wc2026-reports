#!/usr/bin/env python3
"""
Fetch real odds from OddsPapi for 2026 World Cup matches.
Output: odds.json - indexed by "TeamA vs TeamB" (as in schedule.json)

Key insight: Pinnacle spread outcomes are split across multiple markets.
We collect ALL spread outcomes, group by handicap value, then pick the main line.

Sign calibration: use moneyline to determine which API side maps to schedule team_a,
then compare spread odds to determine who gives/receives the handicap.
"""

import json
import re
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone, timedelta

API_KEY = 'b14c79fe-bf24-487a-bfc3-723b17dff50b'
WORLD_CUP_TOURNAMENT_ID = 16
BOOKMAKER = 'pinnacle'

BEIJING = timezone(timedelta(hours=8))


def fetch_fixtures():
    url = (f'https://api.oddspapi.io/v4/odds-by-tournaments'
           f'?bookmaker={BOOKMAKER}&tournamentIds={WORLD_CUP_TOURNAMENT_ID}'
           f'&apiKey={API_KEY}&oddsFormat=decimal')
    req = urllib.request.Request(url, headers={'User-Agent': 'Python'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def collect_all_spreads(markets):
    """Collect ALL spread outcomes across ALL markets."""
    outcomes = []
    for mid, mkt in markets.items():
        bmid = mkt.get('bookmakerMarketId', '')
        if '/spreads' not in bmid:
            continue
        if not mkt.get('marketActive', True):
            continue
        is_alt = 'altLine' in bmid
        for oid, outcome in mkt.get('outcomes', {}).items():
            players = outcome.get('players', {})
            for pid, player in players.items():
                if not player.get('active', True):
                    continue
                outcome_id = player.get('bookmakerOutcomeId', '')
                price = player.get('price')
                limit = player.get('limit', 0)
                if '/' not in outcome_id:
                    continue
                hcap_str, side = outcome_id.split('/', 1)
                try:
                    hcap = float(hcap_str)
                except ValueError:
                    continue
                if side not in ('home', 'away'):
                    continue
                outcomes.append({
                    'handicap': hcap,
                    'side': side,
                    'price': price,
                    'limit': limit,
                    'is_alt': is_alt,
                })
    return outcomes


def find_main_spread(spread_outcomes):
    """Find the main spread pair (highest limit, non-alt preferred)."""
    by_handicap = defaultdict(list)
    for o in spread_outcomes:
        by_handicap[o['handicap']].append(o)

    candidates = []
    for hcap, items in by_handicap.items():
        home_items = [o for o in items if o['side'] == 'home']
        away_items = [o for o in items if o['side'] == 'away']
        if not home_items or not away_items:
            continue

        best_home = max(home_items, key=lambda o: o['limit'])
        best_away = max(away_items, key=lambda o: o['limit'])
        total_limit = best_home['limit'] + best_away['limit']
        is_alt = best_home['is_alt'] or best_away['is_alt']

        candidates.append({
            'abs_hcap': abs(hcap),
            'home_odds': best_home['price'],
            'away_odds': best_away['price'],
            'total_limit': total_limit,
            'is_alt': is_alt,
        })

    if not candidates:
        return None

    # Prefer non-alt, then highest limit
    candidates.sort(key=lambda c: (c['is_alt'], -c['total_limit']))
    return candidates[0]


def parse_moneyline(markets):
    """Parse moneyline (1X2) odds."""
    for mid, mkt in markets.items():
        outcomes = mkt.get('outcomes', {})
        # Check if this is a moneyline market
        is_ml = False
        for oid, outcome in outcomes.items():
            players = outcome.get('players', {})
            for pid, player in players.items():
                if player.get('bookmakerOutcomeId') in ('home', 'draw', 'away'):
                    is_ml = True
                    break
            if is_ml:
                break
        if not is_ml:
            continue

        home = draw = away = None
        for oid, outcome in outcomes.items():
            players = outcome.get('players', {})
            for pid, player in players.items():
                oid_str = player.get('bookmakerOutcomeId', '')
                price = player.get('price')
                if oid_str == 'home':
                    home = price
                elif oid_str == 'draw':
                    draw = price
                elif oid_str == 'away':
                    away = price
        return home, draw, away
    return None, None, None


def calibrate_handicap(spread_info, ml_home, ml_away):
    """
    Determine handicap display string with correct sign.

    Algorithm:
    1. Use moneyline: lower ml → stronger team → maps to API home/away
    2. Use spread odds: lower spread odds → favored side
    3. Always assume schedule team_a = the STRONGER team
    4. If team_a's API side IS the spread-favored side → handicap = -abs (team_a gives)
       If team_a's API side is NOT favored → handicap = +abs (team_a receives)
    """
    abs_hcap = spread_info['abs_hcap']
    home_odds = spread_info['home_odds']
    away_odds = spread_info['away_odds']

    # Which API side is stronger? (lower ml = stronger)
    api_stronger = 'home' if (ml_home and ml_away and ml_home < ml_away) else 'away'

    # Which API side is favored in the spread? (lower spread odds = favored)
    spread_favored = 'home' if home_odds < away_odds else 'away'

    # team_a = stronger team = API's stronger side (by moneyline)
    team_a_api_side = api_stronger

    # team_a gives handicap if team_a's API side = spread favored side
    if team_a_api_side == spread_favored:
        hcap_display = -abs_hcap  # team_a gives
    else:
        hcap_display = abs_hcap   # team_a receives

    hcap_str = f'{hcap_display:+.2f}'.replace('.00', '')
    return hcap_str


def match_fixture_to_schedule(fixture, schedule):
    """Match fixture to schedule.json by Beijing time."""
    start_utc = datetime.fromisoformat(fixture['startTime'].replace('Z', '+00:00'))
    start_bj = start_utc.astimezone(BEIJING)
    date_bj = start_bj.strftime('%Y-%m-%d')
    time_bj = start_bj.strftime('%H:%M')

    best_match = None
    best_score = -1

    for s in schedule:
        if s['date'] != date_bj:
            continue
        s_time = s.get('time_bj', '')
        if not s_time:
            continue
        try:
            s_hour = int(s_time.split(':')[0])
            f_hour = int(time_bj.split(':')[0])
            diff = abs(s_hour - f_hour)
            if diff <= 1:
                score = 10 - diff
            else:
                continue
        except (ValueError, IndexError):
            continue

        if score > best_score:
            best_score = score
            best_match = s

    return best_match


def main():
    with open('schedule.json', 'r', encoding='utf-8') as f:
        schedule = json.load(f)

    print(f'Fetching odds from OddsPapi (Pinnacle, tournament {WORLD_CUP_TOURNAMENT_ID})...')
    try:
        fixtures = fetch_fixtures()
        print(f'  Got {len(fixtures)} fixtures')
    except Exception as e:
        print(f'  Error: {e}')
        with open('odds.json', 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return

    odds_map = {}
    matched = 0
    spread_ok = 0

    for fixture in fixtures:
        s = match_fixture_to_schedule(fixture, schedule)
        if not s:
            continue

        team_a = s['team_a']
        team_b = s['team_b']
        key = f'{team_a} vs {team_b}'

        if key in odds_map:
            continue
        matched += 1

        pinnacle = fixture.get('bookmakerOdds', {}).get(BOOKMAKER, {})
        markets = pinnacle.get('markets', {})

        # Parse moneyline first (for mapping and sign)
        ml_home, ml_draw, ml_away = parse_moneyline(markets)

        # Find main spread line
        all_spreads = collect_all_spreads(markets)
        spread_info = find_main_spread(all_spreads)

        if spread_info and ml_home and ml_away:
            handicap = calibrate_handicap(spread_info, ml_home, ml_away)
            odds_up = spread_info['home_odds']
            odds_down = spread_info['away_odds']
            spread_ok += 1
        elif spread_info:
            # Have spread but no moneyline — just show absolute
            handicap = f'-{spread_info["abs_hcap"]:.2f}'.replace('.00', '')
            odds_up = spread_info['home_odds']
            odds_down = spread_info['away_odds']
            spread_ok += 1
        else:
            handicap = '—'
            odds_up = '—'
            odds_down = '—'

        odds_map[key] = {
            'handicap': handicap,
            'odds_up': odds_up or '—',
            'odds_down': odds_down or '—',
            'ml_home': ml_home or '—',
            'ml_draw': ml_draw or '—',
            'ml_away': ml_away or '—',
        }

        print(f'  {key}: handicap={handicap}, up={odds_up}, down={odds_down}')

    with open('odds.json', 'w', encoding='utf-8') as f:
        json.dump(odds_map, f, ensure_ascii=False, indent=2)

    print(f'\n  Matched {matched} fixtures, {spread_ok} with spread data → odds.json')


if __name__ == '__main__':
    main()
