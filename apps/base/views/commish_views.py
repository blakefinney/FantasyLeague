import os

import nflgame.update_players
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from apps.base.helpers import *
from apps.base.models import Matchup, Player, FantasyPoints


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
        # Loop through players after update
        for p in nflgame.players:
            player = nflgame.players[p]
            # Check if player is currently in the FantasyLeague Database
            try:
                fl_player = Player.objects.get(ng_id=p)
                # Add ESB
                ng_player = nflgame.players.get(fl_player.ng_id)
                if hasattr(ng_player, 'esb_id'):
                    fl_player.esb_id = ng_player.esb_id
                if hasattr(ng_player, 'team') and ng_player.team != '':
                    fl_player.team = ng_player.team
                else:
                    # Player exists but has been cut, LOL
                    fl_player.team = 'UNK'
                fl_player.save()
                found = True
            except ObjectDoesNotExist:
                found = False

            if not found:
                # Is player an offensive player? If not disregard #FuckIDP
                if player.position in ['QB', 'RB', 'FB', 'WR', 'TE', 'K']:
                    Player.objects.create_player(ng_player=player)

    return render(request, 'base/commish_update_players.html', context=template_context)


@user_passes_test(lambda u: u.is_superuser)
def commish_update_fantasy_points(request):
    """ Story View """
    template_context = {}
    year, week = nflgame.live.current_year_and_week()
    fp_array = []
    if request.method == 'POST':
        # Loop through players after update
        for p in Player.objects.all():
            try:
                fp = FantasyPoints.objects.get(player=p, year=year)
            except ObjectDoesNotExist:
                fp = FantasyPoints.objects.create_fp(p, year)
            fp_array.append(fp)

        for g in range(1, 18):
            games = nflgame.games(year, week=g, kind='REG')
            for game in games:
                for fp in fp_array:
                    if "DEF-" in fp.player.ng_id:
                        defc = fp.player.ng_id.split('-')[1]
                        if game.away == defc or game.home == defc:
                            score, d = calculate_def_score(defc, [game])
                            setattr(fp, 'week' + str(g), score)
                            fp.calc_total()
                            fp.save()
                    else:
                        player_in_game = game.players.playerid(fp.player.ng_id)
                        if player_in_game:
                            # Player played in this game
                            fgs = []
                            if player_in_game.kicking_fga:
                                fgs = get_fg_lengths(game, player_in_game)
                            score, d = calculate_week_score(game, player_in_game, fgs)
                            setattr(fp, 'week'+str(g), score)
                            fp.calc_total()
                            fp.save()

    return render(request, 'base/commish_update_fantasy_points.html', context=template_context)


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
