import nflgame
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from apps.base.models import Matchup, Player


@user_passes_test(lambda u: u.is_superuser)
def commish_home(request):
    """ Story View """
    template_context = {}

    return render(request, 'base/commish_home.html', context=template_context)


@user_passes_test(lambda u: u.is_superuser)
def commish_update_players(request):
    """ Story View """
    template_context = {}
    if request.method == 'POST':
        do = 'nothing'
        for p in nflgame.players:
            player = nflgame.players[p]
            # Is player an offensive player? If not disregard #FuckIDP
            if player.position in ['QB', 'RB', 'FB', 'WR', 'TE', 'K']:
                # Check if player is currently in the FantasyLeague Database
                try:
                    fl_player = Player.objects.get(ng_id=p)
                    found = True
                except ObjectDoesNotExist:
                    found = False

                if not found:
                    Player.objects.create_player(ng_player=player)

    return render(request, 'base/commish_update_players.html', context=template_context)


@user_passes_test(lambda u: u.is_superuser)
def commish_end_gameweek(request):
    """ Story View """
    template_context = {}
    if request.method == 'POST':
        gameweek = int(request.POST['gameweek'])
        if gameweek:
            week_matchups = Matchup.objects.filter(week_number=gameweek)
            # End Matchups
            for mc in week_matchups:
                mc.completed = True
                mc.home_roster_archive = mc.home_team.get_roster_archive()
                mc.away_roster_archive = mc.away_team.get_roster_archive()
                mc.save()
    return render(request, 'base/commish_end_gameweek.html', context=template_context)
