"""Views for the team pages"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.base.constants import TEAM_CONST, POSITIONS
import nflgame
import nfldb

from django.conf import settings


@login_required(login_url='/login/')
def team_home(request, team_id=None):
    """ Story View """
    template_context = {}
    # Fetch Current Team
    positions = []
    bench = []
    starters = {}

    # Test Team
    team = {'starting':{'QB':['00-0020531','00-0021429'],
                        'RB':['00-0025394','00-0032241'],
                        'WR':['00-0027944','00-0027793'],
                        'TE':['00-0024389'],
                        'FLEX':['00-0030564','00-0027531','00-0031235'],
                        'K':['00-0028660'],
                        'DEF':['noplayer']},
            'bench':['00-0031285',
                     '00-0026153',
                     '00-0024334']}

    db = nfldb.connect()



    for pos in TEAM_CONST.STARTER_ORDER:
        no_of_pos = TEAM_CONST.STARTING_SPOTS[pos]
        for i in range(0,no_of_pos):
            if pos == POSITIONS.BENCH:
                p_id = 'noplayer'
                if len(team['bench']) > i:
                    p_id = team['bench'][i]
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
                else:
                    bench.append({
                        "position": str(pos),
                        "player_id": p_id,
                        "player_name": 'Empty'
                    })
            else:
                p_id = team['starting'][pos][i]
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
                else:
                    positions.append({
                        "position": str(pos),
                        "player_id": p_id,
                        "player_name": 'Empty'
                    })
                if str(pos) not in starters:
                    starters[str(pos)] = []
                starters[str(pos)].append(p_name)

    template_context.update(positions=positions,bench=bench,starters=starters)

    return render(request, 'base/team_home.html', context=template_context)
