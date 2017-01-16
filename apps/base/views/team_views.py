"""Views for the team pages"""
import sys
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.base.constants import TEAM_CONST, POSITIONS
from apps.base.helpers import *
from apps.base.models import Team
import nflgame
try:
    import nfldb
except ImportError:
    nfldb = None
    pass

# Test team here

from django.conf import settings


@login_required(login_url='/login/')
def team_home(request, team_id=None):
    """ Story View """
    template_context = {}
    # Fetch Current Team
    display_team = Team.objects.get(team_id="Team-"+team_id)
    template_context.update({"team_name": display_team.team_name})
    positions = []
    bench = []
    starters = {}

    # Test Team
    team = display_team.get_roster()

    if nfldb:
        db = nfldb.connect()

    for pos in TEAM_CONST.STARTER_ORDER:
        no_of_pos = TEAM_CONST.STARTING_SPOTS[pos]
        for i in range(0,no_of_pos):
            if pos == POSITIONS.BENCH:
                p_id = 'noplayer'
                if len(team['bench']) > i:
                    p_id = team['bench'][i]
                result = []
                if nfldb:
                    q = nfldb.Query(db).game(season_year=2016, season_type='Regular')
                    q.player(player_id=p_id)
                    result = q.as_aggregate()
                if len(result):
                    stats = result[0]
                    bench.append({
                        "position": str(pos),
                        "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                        "player_id": p_id,
                        "player_name": stats.player.full_name,
                        "player_position": str(stats.player.position),
                        "player_team": stats.player.team,
                        "pass": {"atts": stats.passing_att, "yards": stats.passing_yds, "tds": stats.passing_tds},
                        "rush": {"atts": stats.rushing_att, "yards": stats.rushing_yds, "tds": stats.rushing_tds},
                        "rec": {"tar":stats.receiving_tar,"recep": stats.receiving_rec, "yards": stats.receiving_yds, "tds": stats.receiving_tds}
                    })
                elif not nflgame.players.get(p_id) is None:
                    p = nflgame.players.get(p_id)
                    bench.append({
                        "position": str(pos),
                        "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                        "player_id": p_id,
                        "player_name": p.full_name,
                        "player_position": str(p.position),
                        "player_team": p.team,
                        "pass": {"atts": 0, "yards": 0, "tds": 0},
                        "rush": {"atts": 0, "yards": 0, "tds": 0},
                        "rec": {"tar": 0, "recep": 0, "yards": 0,"tds": 0}
                    })
                else:
                    bench.append({
                        "position": str(pos),
                        "player_id": "noplayer",
                        "player_name": 'Empty'
                    })
            else:
                p_id = team['starting'][pos][i]
                result = []
                if nfldb:
                    q = nfldb.Query(db).game(season_year=2016, season_type='Regular')
                    q.player(player_id=p_id)
                    result = q.as_aggregate()
                p_name = 'Empty'
                if len(result):
                    stats = result[0]
                    p_name = stats.player.full_name
                    positions.append({
                        "position": str(pos),
                        "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                        "player_id": p_id,
                        "player_name": stats.player.full_name,
                        "player_position": str(stats.player.position),
                        "player_team": stats.player.team,
                        "pass":{"atts":stats.passing_att,"yards":stats.passing_yds,"tds":stats.passing_tds},
                        "rush":{"atts":stats.rushing_att,"yards": stats.rushing_yds,"tds":stats.rushing_tds},
                        "rec":{"tar":stats.receiving_tar,"recep":stats.receiving_rec,"yards": stats.receiving_yds,"tds":stats.receiving_tds}
                    })
                elif not nflgame.players.get(p_id) is None:
                    p = nflgame.players.get(p_id)
                    p_name = p.full_name
                    positions.append({
                        "position": str(pos),
                        "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                        "player_id": p_id,
                        "player_name": p.full_name,
                        "player_position": str(p.position),
                        "player_team": p.team,
                        "pass": {"atts": 0, "yards": 0, "tds": 0},
                        "rush": {"atts": 0, "yards": 0, "tds": 0},
                        "rec": {"tar": 0, "recep": 0, "yards": 0, "tds": 0}
                    })
                else:
                    positions.append({
                        "position": str(pos),
                        "player_id": "noplayer",
                        "player_name": 'Empty'
                    })
                if str(pos) not in starters:
                    starters[str(pos)] = []
                starters[str(pos)].append(p_name)

    template_context.update(positions=positions,
                            bench=bench,
                            starters=starters,
                            flex_pos=["RB","WR","TE"],
                            starter_order=TEAM_CONST.STARTER_ORDER)

    return render(request, 'base/team_home.html', context=template_context)


@login_required(login_url='/login/')
def live_scores(request):
    """ Story View """
    template_context = {}
    weeks = 17
    # Test Team
    team_1 = Team.objects.get(team_id="Team-1")
    team_2 = Team.objects.get(team_id="Team-2")

    team = team_1.get_roster()
    team2 = team_2.get_roster()

    positions = []
    positions2 = []

    bench = []
    bench2 = []

    team1score = 0
    team2score = 0

    find_year, find_week = nflgame.live.current_year_and_week()
    find_kind = "POST" # Should always be "REG" except testing
    find_week = 2

    if 'week' in request.GET:
        find_week = int(request.GET['week'])

    week_games = nflgame.games(find_year, week=2, kind=find_kind)

    for pos in TEAM_CONST.STARTER_ORDER:
        no_of_pos = TEAM_CONST.STARTING_SPOTS[pos]
        for i in range(0, no_of_pos):
            pid = 'noplayer'
            pid2 = 'noplayer'
            if pos == 'BEN':
                if len(team['bench']) > i:
                    pid = team['bench'][i]
                if len(team2['bench']) > i:
                    pid2 = team2['bench'][i]
            else:
                pid = team['starting'][pos][i]
                pid2 = team2['starting'][pos][i]
            found = False
            found2 = False
            if pos != 'DEF':
                player_details = nflgame.players.get(pid)
                player_details2 = nflgame.players.get(pid2)
                for game in week_games:
                    player_in_game = game.players.playerid(pid)
                    player2_in_game = game.players.playerid(pid2)
                    if player_in_game:
                        found = True
                        fgs = []
                        if player_in_game.kicking_fga:
                            fgs = get_fg_lengths(game, player_in_game)
                        score, score_summary = calculate_week_score(player_in_game, fgs)
                        esb_id = ''
                        if hasattr(player_details, 'esb_id'):
                            esb_id = player_details.esb_id
                        injury_status = ''
                        if hasattr(player_details, 'injury_status'):
                            injury_status = player_details.injury_status
                        live_status1 = ''
                        if game.playing:
                            live_status1 = player_in_live(player_details, game)
                        format_player = {
                                "position": str(pos),
                                "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                                "player_id": pid,
                                "esb_id": esb_id,
                                "status": player_details.status,
                                "live_status": live_status1,
                                "injury_status": injury_status,
                                "player_name": player_in_game.player.full_name,
                                "player_position": str(player_in_game.player.position),
                                "player_team": player_in_game.player.team,
                                "score": ("%.2f" % score),
                                "score_summary": score_summary,
                                "opponent": get_player_opponent_string(player_in_game.player.team, find_week,
                                                                       find_year, find_kind)
                            }
                        if pos == 'BEN':
                            bench.append(format_player)
                        else:
                            positions.append(format_player)
                            team1score += score
                    if player2_in_game:
                        found2 = True
                        fgs2 = []
                        if player2_in_game.kicking_fga:
                            fgs2 = get_fg_lengths(game, player2_in_game)
                        score2, score2_summary = calculate_week_score(player2_in_game, fgs2)
                        esb_id2 = ''
                        if hasattr(player_details, 'esb_id'):
                            esb_id2 = player_details2.esb_id
                        injury_status2 = ''
                        if hasattr(player_details2, 'injury_status'):
                            injury_status2 = player_details2.injury_status
                        live_status2 = ''
                        if game.playing:
                            live_status2 = player_in_live(player_details2, game)
                        format_player2 = {
                                "position": str(pos),
                                "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                                "player_id": pid,
                                "esb_id": esb_id2,
                                "status": player_details2.status,
                                "live_status": live_status2,
                                "injury_status": injury_status2,
                                "player_name": player2_in_game.player.full_name,
                                "player_position": str(player2_in_game.player.position),
                                "player_team": player2_in_game.player.team,
                                "score": ("%.2f" % score2),
                                "score_summary": score2_summary,
                                "opponent": get_player_opponent_string(player2_in_game.player.team, find_week,
                                                                       find_year, find_kind)
                            }
                        if pos == 'BEN':
                            bench2.append(format_player2)
                        else:
                            positions2.append(format_player2)
                            team2score += score2
            else:
                if pid and pid != 'noplayer':
                    # Active defence
                    found = True
                    def1 = pid.split('-')[1]
                    try:
                        def_game = nflgame.games(2016, week=find_week, kind='REG', home=def1, away=def1)
                        def_score, def_score_summary = calculate_def_score(def1, def_game)
                    except TypeError as e:
                        # Defence on bye week
                        def_score, def_score_summary = 0, []
                    positions.append({
                        "position": str(pos),
                        "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                        "player_id": pid,
                        "player_name": def1+' DEF/ST',
                        "player_position": 'DEF',
                        "player_team": def1,
                        "score": ("%.2f" % def_score),
                        "score_summary": def_score_summary,
                        "opponent": get_player_opponent_string(def1, find_week, find_year, find_kind)
                    })
                    team1score += def_score
                if pid2 and pid2 != 'noplayer':
                    # Active defence
                    found2 = True
                    def2 = pid2.split('-')[1]
                    try:
                        def2_game = nflgame.games(find_year, week=find_week, kind=find_kind, home=def2, away=def2)
                        def_score2, def_score_summary2 = calculate_def_score(def2, def2_game)
                    except TypeError as e:
                        # Defence on bye week
                        def_score2, def_score_summary2 = 0, []
                    positions2.append({
                        "position": str(pos),
                        "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                        "player_id": pid,
                        "player_name": def2 + ' DEF/ST',
                        "player_position": 'DEF',
                        "player_team": def2,
                        "score": ("%.2f" % def_score2),
                        "score_summary": def_score_summary2,
                        "opponent": get_player_opponent_string(def2, find_week, find_year, find_kind)
                    })
                    team2score += def_score2
            if not found:
                if pos == 'BEN':
                    if player_details != None:
                        esb_id = ''
                        if hasattr(player_details, 'esb_id'):
                            esb_id = player_details.esb_id
                        bench.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid,
                            "esb_id": esb_id,
                            "player_name": player_details.full_name,
                            "player_position": str(player_details.position),
                            "player_team": player_details.team,
                            "score": "0.00",
                            "opponent": get_player_opponent_string(player_details.team, find_week,
                                                                   find_year, find_kind)
                        })
                    else:
                        bench.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid,
                            "player_name": 'Empty',
                            "player_position": 'Empty',
                            "player_team": 'Empty',
                            "score": "0.00",
                            "opponent": ''
                        })
                else:
                    if player_details != None:
                        esb_id = ''
                        if hasattr(player_details, 'esb_id'):
                            esb_id = player_details.esb_id
                        positions.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid,
                            "esb_id": esb_id,
                            "player_name": player_details.full_name,
                            "player_position": str(player_details.position),
                            "player_team": player_details.team,
                            "score": "0.00",
                            "opponent": get_player_opponent_string(player_details.team, find_week,
                                                                   find_year, find_kind)
                        })
                    else:
                        positions.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid,
                            "player_name": 'Empty',
                            "player_position": 'Empty',
                            "player_team": 'Empty',
                            "score": "0.00",
                            "opponent": ''
                        })
            if not found2:
                if pos == 'BEN':
                    if player_details2 != None:
                        esb_id2 = ''
                        if hasattr(player_details2,'esb_id'):
                            esb_id2 = player_details2.esb_id
                        bench2.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid2,
                            "esb_id": esb_id2,
                            "player_name": player_details2.full_name,
                            "player_position": str(player_details2.position),
                            "player_team": player_details2.team,
                            "score": "0.00",
                            "opponent": get_player_opponent_string(player_details2.team, find_week,
                                                                   find_year, find_kind)
                        })
                    else:
                        bench2.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid2,
                            "player_name": 'Empty',
                            "player_position": 'Empty',
                            "player_team": 'Empty',
                            "score": "0.00",
                            "opponent": ''
                        })
                else:
                    if player_details2 != None:
                        esb_id2 = ''
                        if hasattr(player_details2,'esb_id'):
                            esb_id2 = player_details2.esb_id
                        positions2.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid2,
                            "esb_id": esb_id2,
                            "player_name": player_details2.full_name,
                            "player_position": str(player_details2.position),
                            "player_team": player_details2.team,
                            "score": "0.00",
                            "opponent": get_player_opponent_string(player_details2.team, find_week,
                                                                   find_year, find_kind)
                        })
                    else:
                        positions2.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid2,
                            "player_name": 'Empty',
                            "player_position": 'Empty',
                            "player_team": 'Empty',
                            "score": "0.00",
                            "opponent": ''
                        })

    template_context.update(team=team, starter_order=TEAM_CONST.STARTER_ORDER, positions=positions,
                            positions2=positions2,bench=bench, bench2=bench2,team1score=team1score,
                            team2score=team2score, starter_length=range(0,len(positions)),
                            bench_length=range(0,max(TEAM_CONST.STARTING_SPOTS[POSITIONS.BENCH],len(bench),len(bench2))),
                            weeks=range(1,weeks+1),find_week=find_week)

    return render(request, 'base/live_scores.html', context=template_context)
