"""Views for the player pages"""
import json

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from apps.base.helpers import *
from apps.base.models import Team, Schedule, Player, FantasyPoints, Roster
import nflgame
try:
    import nfldb
except ImportError:
    nfldb = None
    pass


@login_required(login_url='/login/')
def player_list(request):
    """ Story View """
    template_context = {}
    # Filters is available
    pos_filter = None
    offset = 0
    if 'pos' in request.GET:
        pos_filter = request.GET['pos']
    if 'page' in request.GET:
        offset = int(request.GET['page']) * 25
    if 'add_player' in request.GET:
        ng_id = request.GET['add_player']
        player = Player.objects.get(ng_id=ng_id)
        template_context.update(player=player)
        template_context.update(btn_type='success', transaction_type='Add')
        temp_name = 'base/add_player.html'
    elif 'drop_player' in request.GET:
        ng_id = request.GET['drop_player']
        player = Player.objects.get(ng_id=ng_id)
        template_context.update(player=player)
        template_context.update(btn_type='danger', transaction_type='Drop')
        temp_name = 'base/add_player.html'
    else:
        # Default is all unowned players
        top_scorers = FantasyPoints.objects.filter(player__status='Free Agent').order_by('-total')[offset:(offset+25)]
        if pos_filter:
            top_scorers = top_scorers.filter(player__position=pos_filter)
        return_list = []
        for scorer in top_scorers:
            return_list.append(scorer)
        template_context.update(player_list=return_list)
        temp_name = 'base/player_list.html'
    return render(request, temp_name, context=template_context)


@login_required(login_url='/login/')
def transaction_player(request):
    """ Story View """
    template_context = {}
    if request.method == 'POST':
        pid = None
        user_team = Team.objects.get(team_owner=request.user.username)
        if 'player_id' in request.POST:
            pid = request.POST['player_id']
            t_type = request.POST['transaction_type']
            db_player = Player.objects.get(ng_id=pid)
            success = False
            if t_type == 'Add':
                if db_player.is_free_agent():
                    success = user_team.add_player(db_player)
            elif t_type == 'Drop':
                if db_player.is_owned_by(user_team):
                    success = user_team.drop_player(db_player)

        return HttpResponseRedirect('/team/'+str(user_team.id)+'/')
    else:
        # Shouldn't get here
        return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def player_info(request, player_id=None):
    """ Story View """
    template_context = {}
    current_year, current_week = nflgame.live.current_year_and_week()
    p = Player.objects.get(ng_id=player_id)
    fp = FantasyPoints.objects.get(player=p)
    ng_p = nflgame.players.get(player_id)
    team = p.team.replace('JAC', 'JAX')
    schedule = []
    for g in range(1, 18):
        try:
            game = nflgame.games(current_year, week=g, home=team, away=team)
        except TypeError:
            # Bye week here, probably
            game = []
        if len(game):
            game = game[0]
            fgs = []
            if "DEF-" in player_id:
                score, desc = calculate_def_score(player_id.split('-')[1], [game])
            else:
                if game.players.playerid(player_id).kicking_fga:
                    fgs = get_fg_lengths(game, game.players.playerid(player_id))
                score, desc = calculate_week_score(game, game.players.playerid(player_id), fgs)
            if game.is_home(team) or game.is_home(team.replace('JAX', 'JAC')):
                opp_str = 'v '+game.away
            else:
                opp_str = '@ '+game.home
            schedule.append({"score": score, "desc": desc, "opp": opp_str})
            setattr(fp, 'week' + str(g), score)
            fp.calc_total()
            fp.save()
        else:
            schedule.append({"score": 0, "desc": ["Bye Week"]})
            setattr(fp, 'week' + str(g), 0)
            fp.calc_total()
            fp.save()

    template_context.update({"schedule": schedule, "player": p})
    return render(request, 'base/player_info.html', context=template_context)


@login_required(login_url='/login/')
def propose_trade(request):
    """ Story View """
    template_context = {}
    user_team = Team.objects.get(team_owner=request.user.username)
    roster_array = Roster.objects.get(pk=user_team.id).get_roster_array()

    template_context.update({"team_name": user_team.team_name,
                             "roster": roster_array,
                             "user_json": json.dumps(roster_array).replace("'", ""),
                             "prop_json": json.dumps([]).replace("'", "")})
    return render(request, 'base/propose_trade.html', context=template_context)
