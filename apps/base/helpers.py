""" Some Helper Functions for the Wesbite"""
from django.conf import settings
import nflgame


def is_logged_in(request):
    return request.user.is_active


def get_fg_lengths(game, player):
    fgs = []
    plays = game.drives.plays()
    for play in plays:
        for kicker in play.players.kicking():
            if kicker.playerid == player.playerid:
                if play.kicking_fgm_yds > 0:
                    fgs.append(play.kicking_fgm_yds)
                elif play.kicking_fgmissed_yds > 0:
                    fgs.append(0-play.kicking_fgmissed_yds)
    return fgs


def calculate_week_score(player_stats, fgs):
    score = 0
    text_array = []
    if player_stats:
        # Passing Scoring
        if player_stats.passing_yds:
            score += player_stats.passing_yds*settings.SCORING_SYSTEM['passing']['yards']
            text_array.append(str(player_stats.passing_yds)+" Pass Yds")
            if player_stats.passing_yds >= 400:
                score += settings.SCORING_SYSTEM['passing']['400bonus']
            elif player_stats.passing_yds >= 300:
                score += settings.SCORING_SYSTEM['passing']['300bonus']
        if player_stats.passing_tds:
            score += player_stats.passing_tds*settings.SCORING_SYSTEM['passing']['touchdowns']
            text_array.append(str(player_stats.passing_tds) + " Pass TDs")
        if player_stats.passing_ints:
            score += player_stats.passing_ints*settings.SCORING_SYSTEM['passing']['interceptions']
            text_array.append(str(player_stats.passing_ints) + " INTs")

        # Rushing Scoring
        if player_stats.rushing_yds:
            score += player_stats.rushing_yds*settings.SCORING_SYSTEM['rushing']['yards']
            text_array.append(str(player_stats.rushing_yds) + " Rush Yds")
            if player_stats.rushing_yds >= 200:
                score += settings.SCORING_SYSTEM['rushing']['200bonus']
            elif player_stats.rushing_yds >= 100:
                score += settings.SCORING_SYSTEM['rushing']['100bonus']
        if player_stats.rushing_tds:
            score += player_stats.rushing_tds*settings.SCORING_SYSTEM['rushing']['touchdowns']
            text_array.append(str(player_stats.rushing_tds) + " Rush TDs")

        # Receiving Scoring
        if player_stats.receiving_rec:
            score += player_stats.receiving_rec * settings.SCORING_SYSTEM['receiving']['receptions']
            text_array.append(str(player_stats.receiving_rec) + " Receps")
        if player_stats.receiving_yds:
            score += player_stats.receiving_yds * settings.SCORING_SYSTEM['receiving']['yards']
            text_array.append(str(player_stats.receiving_yds) + " Rec Yds")
            if player_stats.receiving_yds >= 200:
                score += settings.SCORING_SYSTEM['receiving']['200bonus']
            elif player_stats.receiving_yds >= 100:
                score += settings.SCORING_SYSTEM['receiving']['100bonus']
        if player_stats.receiving_tds:
            score += player_stats.receiving_tds * settings.SCORING_SYSTEM['receiving']['touchdowns']
            text_array.append(str(player_stats.receiving_tds) + " Rec TDs")

        # Kicking Stats
        if player_stats.kicking_xpmade:
            score += player_stats.kicking_xpmade * settings.SCORING_SYSTEM['kicking']['madeXP']
            text_array.append(str(player_stats.kicking_xpmade) + " XPs Made")
            if player_stats.kicking_xpmade != player_stats.kicking_xpa:
                misses = player_stats.kicking_xpa - player_stats.kicking_xpmade
                score += misses * settings.SCORING_SYSTEM['kicking']['missXP']
                text_array.append(str(misses) + " XPs Missed")
        # Field Goals Found
        if len(fgs):
            twenties, thirties, fourties, fifties = 0, 0, 0, 0
            m_twenties, m_thirties, m_fourties, m_fifties = 0, 0, 0, 0
            for fg in fgs:
                if fg < -50:
                    m_fifties += 1
                elif fg < -40:
                    m_fourties += 1
                elif fg < -30:
                    m_thirties += 1
                elif fg < 0:
                    m_twenties += 1
                elif fg < 30:
                    twenties += 1
                elif fg < 40:
                    thirties += 1
                elif fg < 50:
                    fourties += 1
                else:
                    fifties += 1
            # Made FGs
            if twenties:
                score += twenties * settings.SCORING_SYSTEM['kicking']['Made20']
                text_array.append(str(twenties) + " 0-29 FG Made")
            if thirties:
                score += thirties * settings.SCORING_SYSTEM['kicking']['Made30']
                text_array.append(str(thirties) + " 30-39 FG Made")
            if fourties:
                score += fourties * settings.SCORING_SYSTEM['kicking']['Made40']
                text_array.append(str(fourties) + " 40-49 FG Made")
            if fifties:
                score += fifties * settings.SCORING_SYSTEM['kicking']['Made50']
                text_array.append(str(fifties) + " 50+ FG Made")
            # Missed FGs
            if m_twenties:
                score += m_twenties * settings.SCORING_SYSTEM['kicking']['Miss20']
                text_array.append(str(m_twenties) + " 0-29 FG Miss")
            if m_thirties:
                score += m_thirties * settings.SCORING_SYSTEM['kicking']['Miss30']
                text_array.append(str(m_thirties) + " 30-39 FG Miss")
            if m_fourties:
                score += m_fourties * settings.SCORING_SYSTEM['kicking']['Miss40']
                text_array.append(str(m_fourties) + " 40-49 FG Miss")
            if m_fifties:
                score += m_fifties * settings.SCORING_SYSTEM['kicking']['Miss50']
                text_array.append(str(m_fifties) + " 50+ FG Miss")

    return score, text_array


def calculate_def_score(team, game):
    score = 0
    text_array = []
    if len(game):
        game = game[0]
        if game.away == team:
            points_against = game.score_home
        else:
            points_against = game.score_away
        # Get points based on game score
        if points_against > 35:
            score += settings.SCORING_SYSTEM['defence']['Conc35']
            text_array.append('PA 35+')
        elif points_against > 27:
            score += settings.SCORING_SYSTEM['defence']['Conc28']
            text_array.append('PA 28-34')
        elif points_against > 20:
            score += settings.SCORING_SYSTEM['defence']['Conc21']
            text_array.append('PA 21-27')
        elif points_against > 13:
            score += settings.SCORING_SYSTEM['defence']['Conc14']
            text_array.append('PA 14-20')
        elif points_against > 6:
            score += settings.SCORING_SYSTEM['defence']['Conc7']
            text_array.append('PA 7-13')
        elif points_against > 0:
            score += settings.SCORING_SYSTEM['defence']['Conc1']
            text_array.append('PA 1-6')
        else:
            score += settings.SCORING_SYSTEM['defence']['Conc0']
            text_array.append('Shutout')

        # Get other game stats for defence
        sks, frc, frc_td, ints, int_td, safe = 0, 0, 0, 0, 0, 0
        for p in nflgame.combine_plays([game]).filter(team=team):
            # Sacks
            if p.defense_sk > 0:
                sks += 1
            # Fumbles
            if p.defense_frc > 0:
                frc += 1
                if p.defense_frc_tds > 0:
                    frc_td += 1
            # Interceptions
            if p.defense_int > 0:
                ints += 1
                if p.defense_int_tds > 0:
                    int_td += 1
            # Safeties
            if p.defense_safe > 0:
                safe += 1
        # Any Sacks?
        if sks:
            score += sks * settings.SCORING_SYSTEM['defence']['sack']
            text_array.append(str(sks)+' sacks')
        # Fumble Recoveries
        if frc:
            score += frc * settings.SCORING_SYSTEM['defence']['fumblerec']
            text_array.append(str(frc) + ' Fumble Rec')
            if frc_td:
                score += frc_td * settings.SCORING_SYSTEM['defence']['fumblesix']
                text_array.append(str(frc_td) + ' Fumble TDs')
        # Interceptions
        if ints:
            score += ints * settings.SCORING_SYSTEM['defence']['interceptions']
            text_array.append(str(ints) + ' INTs')
            if int_td:
                score += int_td * settings.SCORING_SYSTEM['defence']['picksix']
                text_array.append(str(int_td) + ' Pick 6s')
        # Safeties
        if safe:
            score += safe * settings.SCORING_SYSTEM['defence']['safeties']
            text_array.append(str(safe) + ' Safeties')

        return score, text_array
    else:
        return 0, ['']


def get_player_opponent_string(team, week, year):
    if team == 'JAC':
        team = 'JAX'
    try:
        game = nflgame.games(year, week=week, kind='REG', home=team, away=team)
    except TypeError as e:
        # Likely team on bye week, returned NoneType Error
        game = []
    if len(game):
        game = game[0]
        if game.home == team:
            ret_string = 'v ' + game.away
        else:
            ret_string = '@ ' + game.home
        if game.game_over():
            # Final Score
            ret_string += ' | ' + game.nice_score()
        elif game.playing():
            # LIVE
            ret_string += ' | ' + game.nice_score() + ' LIVE'
        else:
            # Pre-game
            ret_string += ' | Kickoff Time:' + game.time

    else:
        ret_string = 'Bye Week'

    return ret_string
