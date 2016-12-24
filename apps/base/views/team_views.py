"""Views for the team pages"""

from django.shortcuts import render
from apps.base.constants import TEAM
import nflgame
import nfldb

from django.conf import settings


def team_home(request, team_id=None):
    """ Story View """
    template_context = {}
    # Fetch Current Team
    positions = []

    # Test Team
    team = {'starting':{'QB':['00-0020531','00-0021429'],
                        'RB':['00-0025394','00-0032241'],
                        'WR':['00-0027944','00-0027793'],
                        'TE':['noplayer'],
                        'FLEX':['00-0030564','00-0027531','00-0031235'],
                        'K':['noplayer'],
                        'DEF':['noplayer']},
            'bench':['00-0031285',
                     '00-0026153',
                     '00-0024334']}

    db = nfldb.connect()



    for pos in TEAM.STARTER_ORDER:
        no_of_pos = TEAM.STARTING_SPOTS[pos]
        for i in range(0,no_of_pos):
            p_id = team['starting'][pos][i]
            q = nfldb.Query(db).game(season_year=2016, season_type='Regular')
            q.player(player_id=p_id)
            result = q.as_aggregate()
            if len(result):
                stats = result[0]
                positions.append({
                    "position": pos,
                    "player_id": p_id,
                    "player_name": stats.player.full_name,
                    "player_position": stats.player.position,
                    "player_team": stats.player.team,
                    "pass":{"atts":stats.passing_att,"yards":stats.passing_yds,"tds":stats.passing_tds},
                    "rush":{"atts":stats.rushing_att,"yards": stats.rushing_yds,"tds":stats.rushing_tds},
                    "rec":{"recep":stats.receiving_rec,"yards": stats.receiving_yds,"tds":stats.receiving_tds}
                })
            else:
                positions.append({
                    "position": pos,
                    "player_id": p_id,
                    "player_name": 'Empty'
                })

    template_context.update(positions=positions)

    return render(request, 'base/team_home.html', context=template_context)
