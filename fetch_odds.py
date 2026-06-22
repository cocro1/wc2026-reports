#!/usr/bin/env python3
"""
Fetch real odds from OddsPapi for 2026 World Cup matches.
Output: odds.json - indexed by "TeamA vs TeamB" (as in schedule.json)

Strategy:
- Primary bookmaker (default: bet365) for moneyline
- Pinnacle for Asian Handicap (bet365 doesn't provide spreads via this API)
- Market IDs are OddsPapi standard — we use market definitions API to decode them

Sign calibration: use moneyline to determine which side maps to schedule team_a,
then compare spread odds to determine who gives/receives the handicap.
"""

import json
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone, timedelta

API_KEY = 'b14c79fe-bf24-487a-bfc3-723b17dff50b'
WORLD_CUP_TOURNAMENT_ID = 16
PRIMARY_BOOKMAKER = 'bet365'   # for moneyline + display
SPREAD_BOOKMAKER = 'pinnacle'  # fallback for Asian Handicap

BEIJING = timezone(timedelta(hours=8))

# ─── Market definition cache ────────────────────────────────────────────
_market_defs = None


def get_market_defs():
    """Fetch & cache OddsPapi market definitions for soccer."""
    global _market_defs
    if _market_defs is not None:
        return _market_defs

    url = f'https://api.oddspapi.io/v4/markets?sportId=10&apiKey={API_KEY}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Python'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        markets = json.loads(resp.read())

    _market_defs = {}
    for m in markets:
        mid = m['marketId']
        _market_defs[mid] = {
            'type': m.get('marketType', ''),
            'handicap': m.get('handicap', 0),
            'name': m.get('marketName', ''),
            'length': m.get('marketLength', 0),
            'outcomes': {o['outcomeId']: o.get('outcomeName', '')
                         for o in m.get('outcomes', [])},
        }
    return _market_defs


def fetch_fixtures(bookmaker):
    """Fetch odds for a specific bookmaker."""
    url = (f'https://api.oddspapi.io/v4/odds-by-tournaments'
           f'?bookmaker={bookmaker}&tournamentIds={WORLD_CUP_TOURNAMENT_ID}'
           f'&apiKey={API_KEY}&oddsFormat=decimal')
    req = urllib.request.Request(url, headers={'User-Agent': 'Python'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


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
            if diff > 1:
                continue
            score = 10 - diff
        except (ValueError, IndexError):
            continue

        if score > best_score:
            best_score = score
            best_match = s

    return best_match


# ═══ Pinnacle-specific parsing ══════════════════════════════════════════

def pinnacle_parse_moneyline(markets):
    """Parse Pinnacle moneyline — uses bookmakerOutcomeId strings."""
    for mid, mkt in markets.items():
        outcomes = mkt.get('outcomes', {})
        is_ml = False
        for oid, outcome in outcomes.items():
            for pid, player in outcome.get('players', {}).items():
                if player.get('bookmakerOutcomeId') in ('home', 'draw', 'away'):
                    is_ml = True
                    break
            if is_ml:
                break
        if not is_ml:
            continue

        home = draw = away = None
        for oid, outcome in outcomes.items():
            for pid, player in outcome.get('players', {}).items():
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


def pinnacle_collect_spreads(markets):
    """Collect ALL spread outcomes across Pinnacle markets."""
    outcomes = []
    for mid, mkt in markets.items():
        bmid = mkt.get('bookmakerMarketId', '')
        if '/spreads' not in bmid:
            continue
        if not mkt.get('marketActive', True):
            continue
        is_alt = 'altLine' in bmid
        for oid, outcome in mkt.get('outcomes', {}).items():
            for pid, player in outcome.get('players', {}).items():
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
                    'handicap': hcap, 'side': side,
                    'price': price, 'limit': limit, 'is_alt': is_alt,
                })
    return outcomes


def pinnacle_find_main_spread(spread_outcomes):
    """Find main spread (highest limit, non-alt preferred)."""
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
            'total_limit': total_limit, 'is_alt': is_alt,
        })

    if not candidates:
        return None
    candidates.sort(key=lambda c: (c['is_alt'], -c['total_limit']))
    return candidates[0]


# ═══ Bet365-specific parsing (using standard market IDs) ════════════════

def bet365_parse_moneyline(markets, defs):
    """Parse Bet365 moneyline via standard market ID 101."""
    market_101 = markets.get('101')
    if not market_101:
        return None, None, None

    outcomes = market_101.get('outcomes', {})
    _def = defs.get(101, {})
    _def_outcomes = _def.get('outcomes', {})

    # Map outcome name -> price
    prices_by_name = {}
    for oid, outcome in outcomes.items():
        for pid, player in outcome.get('players', {}).items():
            if player.get('active', True):
                name = _def_outcomes.get(int(oid), str(oid))
                prices_by_name[name] = player.get('price')

    return prices_by_name.get('1'), prices_by_name.get('X'), prices_by_name.get('2')


def bet365_get_market_by_id(markets, market_id):
    """Get active prices for a specific market ID."""
    mkt = markets.get(str(market_id))
    if not mkt:
        return None
    outcomes = mkt.get('outcomes', {})
    defs = get_market_defs()
    _def = defs.get(market_id, {})
    _def_outcomes = _def.get('outcomes', {})

    prices = {}
    for oid, outcome in outcomes.items():
        for pid, player in outcome.get('players', {}).items():
            if player.get('active', True):
                name = _def_outcomes.get(int(oid), str(oid))
                prices[name] = player.get('price')
    return prices


# ═══ Shared logic ═══════════════════════════════════════════════════════

def calibrate_handicap(spread_info, ml_home, ml_away, schedule_team_a):
    """
    Determine handicap display string with correct sign.

    Assumption: schedule team_a = the STRONGER team (by ranking/expectation).
    We use moneyline to confirm which API side is stronger.
    """
    abs_hcap = spread_info['abs_hcap']
    home_odds = spread_info['home_odds']
    away_odds = spread_info['away_odds']

    # Moneyline: lower odds = stronger
    if ml_home and ml_away:
        api_stronger = 'home' if ml_home < ml_away else 'away'
    else:
        api_stronger = 'home'

    # Spread: lower odds = favored
    spread_favored = 'home' if home_odds < away_odds else 'away'

    # team_a's API side = stronger side (by moneyline)
    if api_stronger == spread_favored:
        hcap_display = -abs_hcap  # team_a gives handicap
    else:
        hcap_display = abs_hcap   # team_a receives handicap

    hcap_str = f'{hcap_display:+.2f}'.replace('.00', '')
    return hcap_str


# ═══ Main ═══════════════════════════════════════════════════════════════

def main():
    with open('schedule.json', 'r', encoding='utf-8') as f:
        schedule = json.load(f)

    defs = get_market_defs()
    print(f'Loaded {len(defs)} market definitions')

    # ── Fetch Bet365 (primary) ──
    print(f'\nFetching {PRIMARY_BOOKMAKER} odds...')
    try:
        primary_fixtures = fetch_fixtures(PRIMARY_BOOKMAKER)
        print(f'  Got {len(primary_fixtures)} fixtures')
    except Exception as e:
        print(f'  Error: {e}')
        primary_fixtures = []

    # ── Fetch Pinnacle (for spreads) ──
    print(f'\nFetching {SPREAD_BOOKMAKER} odds (for Asian Handicap)...')
    try:
        spread_fixtures = fetch_fixtures(SPREAD_BOOKMAKER)
        print(f'  Got {len(spread_fixtures)} fixtures')
    except Exception as e:
        print(f'  Error: {e}')
        spread_fixtures = []

    odds_map = {}
    matched = 0

    for fixture in primary_fixtures:
        s = match_fixture_to_schedule(fixture, schedule)
        if not s:
            continue

        team_a = s['team_a']
        team_b = s['team_b']
        key = f'{team_a} vs {team_b}'
        if key in odds_map:
            continue
        matched += 1

        bk_data = fixture.get('bookmakerOdds', {}).get(PRIMARY_BOOKMAKER, {})
        markets = bk_data.get('markets', {})

        # ── Moneyline (from Bet365, using standard market ID 101) ──
        ml_home, ml_draw, ml_away = bet365_parse_moneyline(markets, defs)

        # ── Also extract Over/Under 2.5 for reference ──
        ou25 = bet365_get_market_by_id(markets, 1010)  # market 1010 = O/U 2.5
        ou_over = ou25.get('Over') if ou25 else None
        ou_under = ou25.get('Under') if ou25 else None

        # ── Asian Handicap — find matching Pinnacle fixture ──
        handicap = '—'
        odds_up = '—'
        odds_down = '—'
        spread_source = '—'

        if spread_fixtures:
            for sf in spread_fixtures:
                s2 = match_fixture_to_schedule(sf, schedule)
                if s2 and s2['team_a'] == team_a and s2['team_b'] == team_b:
                    pk_data = sf.get('bookmakerOdds', {}).get(SPREAD_BOOKMAKER, {})
                    pk_markets = pk_data.get('markets', {})

                    pk_ml_home, pk_ml_draw, pk_ml_away = pinnacle_parse_moneyline(pk_markets)

                    all_spreads = pinnacle_collect_spreads(pk_markets)
                    spread_info = pinnacle_find_main_spread(all_spreads)

                    if spread_info:
                        # Use primary ML for sign calibration if available
                        cal_ml_home = ml_home or pk_ml_home
                        cal_ml_away = ml_away or pk_ml_away

                        if cal_ml_home and cal_ml_away:
                            handicap = calibrate_handicap(
                                spread_info, cal_ml_home, cal_ml_away, team_a)
                        else:
                            handicap = f'-{spread_info["abs_hcap"]:.2f}'.replace('.00', '')

                        odds_up = spread_info['home_odds']
                        odds_down = spread_info['away_odds']
                        spread_source = SPREAD_BOOKMAKER
                    break

        odds_map[key] = {
            'bookmaker': PRIMARY_BOOKMAKER,
            'handicap': handicap,
            'odds_up': odds_up if odds_up else '—',
            'odds_down': odds_down if odds_down else '—',
            'ml_home': ml_home if ml_home else '—',
            'ml_draw': ml_draw if ml_draw else '—',
            'ml_away': ml_away if ml_away else '—',
            'ou_over': ou_over if ou_over else '—',
            'ou_under': ou_under if ou_under else '—',
            'spread_source': spread_source,
        }

        src_note = f'[spread={spread_source}]' if spread_source != '—' else ''
        print(f'  {key}: ML={ml_home}/{ml_draw}/{ml_away}  '
              f'hcap={handicap}({odds_up}/{odds_down})  '
              f'O/U2.5={ou_over}/{ou_under} {src_note}')

    with open('odds.json', 'w', encoding='utf-8') as f:
        json.dump(odds_map, f, ensure_ascii=False, indent=2)

    print(f'\n  Matched {matched} fixtures → odds.json')
    print(f'  Moneyline source: {PRIMARY_BOOKMAKER}')
    print(f'  Spread source:    {SPREAD_BOOKMAKER} (fallback)')


if __name__ == '__main__':
    main()
