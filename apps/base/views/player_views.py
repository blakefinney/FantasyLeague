"""Views for the player pages"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from apps.base.helpers import *
from apps.base.models import Team, Schedule, Player
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
    if 'add_player' in request.GET:
        ng_id = request.GET['add_player']
        player = nflgame.players.get(ng_id)
        template_context.update(player=player)
        temp_name = 'base/add_player.html'
    else:
        # Default is all unowned players
        unowned = Player.objects.filter(fantasy_team=None)[:25]
        template_context.update(player_list=unowned)
        temp_name = 'base/player_list.html'
    return render(request, temp_name, context=template_context)


@login_required(login_url='/login/')
def add_player(request):
    """ Story View """
    template_context = {}
    if request.method == 'POST':
        pid = None
        if 'player_id' in request.POST:
            pid = request.POST['player_id']
            db_player = Player.objects.get(ng_id=pid)
            user_team = Team.objects.get(team_owner=request.user.username)
            success = False
            if db_player.is_free_agent():
                success = user_team.add_player(db_player)

        return HttpResponseRedirect('/team/1/')
    else:
        # Shouldn't get here
        return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def player_info(request, player_id=None):
    """ Story View """
    template_context = {}
    if request.method == 'POST':
        return render(request, 'base/player_info.html', context=template_context)
    else:
        # Shouldn't get here
        return HttpResponseRedirect('/')
