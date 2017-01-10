"""Views for the team pages"""
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

    team1score = 0
    team2score = 0

    find_week = 1

    if 'week' in request.GET:
        find_week = int(request.GET['week'])

    week_games = nflgame.games(2016, week=find_week, kind='REG')

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
            player_details = nflgame.players.get(pid)
            player_details2 = nflgame.players.get(pid2)
            for game in week_games:
                player_in_game = game.players.playerid(pid)
                player2_in_game = game.players.playerid(pid2)
                if player_in_game:
                    found = True
                    if pos == 'BEN':
                        s = 's'#team['bench'][i] = player_in_game
                    else:
                        fgs = []
                        if player_in_game.kicking_fga:
                            fgs = get_fg_lengths(game, player_in_game)
                        score, score_summary = calculate_week_score(player_in_game, fgs)
                        positions.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid,
                            #"esb_id": player_in_game.player.esb_id,
                            "player_name": player_in_game.player.full_name,
                            "player_position": str(player_in_game.player.position),
                            "player_team": player_in_game.player.team,
                            "score": ("%.2f" % score),
                            "score_summary": score_summary
                        })
                        team1score += score
                if player2_in_game:
                    found2 = True
                    if pos == 'BEN':
                        s = 's'#team['bench'][i] = player_in_game
                    else:
                        fgs2 = []
                        if player2_in_game.kicking_fga:
                            fgs2 = get_fg_lengths(game, player2_in_game)
                        score2, score2_summary = calculate_week_score(player2_in_game, fgs2)
                        positions2.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid,
                            #"esb_id": player2_in_game.player.esb_id,
                            "player_name": player2_in_game.player.full_name,
                            "player_position": str(player2_in_game.player.position),
                            "player_team": player2_in_game.player.team,
                            "score": ("%.2f" % score2),
                            "score_summary": score2_summary
                        })
                        team2score += score2
            if not found:
                if pos == 'BEN':
                    if pid != 'noplayer':
                        s = 's'
                        #team['bench'][i] = pid
                else:
                    if player_details != None:
                        positions.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid,
                            #"esb_id": player_details.esb_id,
                            "player_name": player_details.full_name,
                            "player_position": str(player_details.position),
                            "player_team": player_details.team,
                            "score": "0.00"
                        })
            if not found2:
                if pos == 'BEN':
                    if pid != 'noplayer':
                        s = 's'
                        #team['bench'][i] = pid
                else:
                    if player_details != None:
                        positions2.append({
                            "position": str(pos),
                            "position_accepts": TEAM_CONST.POSITION_ACCEPTS[pos],
                            "player_id": pid,
                            #"esb_id": player_details2.esb_id,
                            "player_name": player_details2.full_name,
                            "player_position": str(player_details2.position),
                            "player_team": player_details2.team,
                            "score": "0.00"
                        })

    template_context.update(team=team, starter_order=TEAM_CONST.STARTER_ORDER, positions=positions, positions2=positions2,
                            team1score=team1score, team2score=team2score, starter_length=range(0,len(positions)), weeks=range(1,weeks+1))

    return render(request, 'base/live_scores.html', context=template_context)
