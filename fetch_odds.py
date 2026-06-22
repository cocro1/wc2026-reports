#!/usr/bin/env python3
"""
Fetch real odds from OddsPapi for 2026 World Cup matches.

Output: odds.json - indexed by "TeamA vs TeamB" (as in schedule.json)
"""

import json
import os
import re
import urllib.request
from datetime import datetime, timezone, timedelta

API_KEY = 'b14c79fe-bf24-487a-bfc3-723b17dff50b'
WORLD_CUP_TOURNAMENT_ID = 16
BOOKMAKER = 'pinnacle'  # Use Pinnacle odds

# Beijing timezone (UTC+8)
BEIJING = timezone(timedelta(hours=8))

def fetch_fixtures():
    """Fetch all upcoming World Cup fixtures with Pinnacle odds."""
    url = (f'https://api.oddspapi.io/v4/odds-by-tournaments'
            f'?bookmaker={BOOKMAKER}&tournamentIds={WORLD_CUP_TOURNAMENT_ID}'
            f'&apiKey={API_KEY}&oddsFormat=decimal')
    req = urllib.request.Request(url, headers={'User-Agent': 'Python'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def parse_spread(markets):
    """
    Find the main spread market and parse handicap + odds.
    Returns: (handicap_str, home_odds, away_odds) or (None, None, None)
    """
    # Find spread markets (bookmakerMarketId contains '/spreads')
    spread_markets = []
    for mid, mkt in markets.items():
        bmid = mkt.get('bookmakerMarketId', '')
        if '/spreads' in bmid and mkt.get('marketActive', True):
            # Prefer main line (not altLine)
            if 'altLine' not in bmid:
                spread_markets.insert(0, (mid, mkt))
            else:
                spread_markets.append((mid, mkt))

    if not spread_markets:
        return None, None, None

    # Use first (main) spread market
    mid, mkt = spread_markets[0]
    outcomes = mkt.get('outcomes', {})

    # Parse outcomes: bookmakerOutcomeId format is "HANDICAP/home" or "HANDICAP/away"
    handicap = None
    home_odds = None
    away_odds = None

    for oid, outcome in outcomes.items():
        players = outcome.get('players', {})
        for pid, player in players.items():
            outcome_id = player.get('bookmakerOutcomeId', '')
            price = player.get('price')
            if '/' in outcome_id:
                hcap, side = outcome_id.split('/', 1)
                try:
                    hcap = float(hcap)
                except:
                    continue
                if handicap is None:
                    handicap = hcap
                # Note: bookmakerOutcomeId format is "HANDICAP/home" or "HANDICAP/away"
        # "home" means home team is giving handicap (favored)
        # "away" means away team is giving handicap
        if side == 'home':
            home_odds = price  # Home team odds (upper hand)
        elif side == 'away':
            away_odds = price  # Away team odds (lower hand)

    if handicap is None:
        return None, home_odds, away_odds

    # Format handicap string
    hcap_str = f'{handicap:+.2f}'.replace('.00', '')
    return hcap_str, home_odds, away_odds

def parse_moneyline(markets):
    """Parse moneyline (1X2) odds."""
    for mid, mkt in markets.items():
        outcomes = mkt.get('outcomes', {})
        # Check if this is moneyline (has "home"/"draw"/"away" outcome IDs)
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

        # Parse odds
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

def match_fixture_to_schedule(fixture, schedule):
    """
    Match a fixture to schedule.json by startTime (Beijing time).
    Returns (team_a, team_b) or None.
    """
    start_utc = datetime.fromisoformat(fixture['startTime'].replace('Z', '+00:00'))
    start_bj = start_utc.astimezone(BEIJING)
    date_bj = start_bj.strftime('%Y-%m-%d')
    time_bj = start_bj.strftime('%H:%M')

    # Find matching schedule entry by date and approximate time
    best_match = None
    best_score = -1

    for s in schedule:
        if s['date'] != date_bj:
            continue
        # Compare time (allow 1 hour tolerance)
        s_time = s.get('time_bj', '')
        if not s_time:
            continue
        try:
            s_hour = int(s_time.split(':')[0])
            f_hour = int(time_bj.split(':')[0])
            if abs(s_hour - f_hour) <= 1:
                score = 10  # Same hour = good match
            else:
                continue
        except:
            continue
        if score > best_score:
            best_score = score
            best_match = s

    return best_match

def main():
    # Load schedule.json
    with open('schedule.json', 'r', encoding='utf-8') as f:
        schedule = json.load(f)

    print(f'Fetching odds from OddsPapi (tournament {WORLD_CUP_TOURNAMENT_ID})...')
    try:
        fixtures = fetch_fixtures()
        print(f'  Got {len(fixtures)} fixtures')
    except Exception as e:
        print(f'  Error fetching fixtures: {e}')
        with open('odds.json', 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return

    odds_map = {}

    for fixture in fixtures:
        # Match to schedule
        match = match_fixture_to_schedule(fixture, schedule)
        if not match:
            continue

        team_a = match['team_a']
        team_b = match['team_b']
        key = f'{team_a} vs {team_b}'

        # Parse odds
        pinnacle = fixture.get('bookmakerOdds', {}).get(BOOKMAKER, {})
        markets = pinnacle.get('markets', {})

        handicap, spread_home, spread_away = parse_spread(markets)
        ml_home, ml_draw, ml_away = parse_moneyline(markets)

        odds_map[key] = {
            'handicap': handicap or '—',
            'odds_up': spread_home or '—',
            'odds_down': spread_away or '—',
            'ml_home': ml_home or '—',
            'ml_draw': ml_draw or '—',
            'ml_away': ml_away or '—',
        }

    # Save odds.json
    with open('odds.json', 'w', encoding='utf-8') as f:
        json.dump(odds_map, f, ensure_ascii=False, indent=2)

    print(f'  Saved {len(odds_map)} matches with odds to odds.json')
    if odds_map:
        sample_key = list(odds_map.keys())[0]
        print(f'  Sample: {sample_key} -> {odds_map[sample_key]}')

if __name__ == '__main__':
    main()
