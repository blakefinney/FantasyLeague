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


def calculate_week_score(game, player_stats, fgs):
    score = 0
    text_array = []
    plays = nflgame.combine_plays([game])
    # Check for 2 point conversion
    two_point = 0
    for d in game.drives:
        if d.result == 'Touchdown':
            for p in d.plays:
                if p.passing_twoptm or p.rushing_twoptm:
                    if p.has_player(player_stats.player.playerid):
                        two_point += 1
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
            # Passing TDs present, check for long TD bonus
            passing_tds = plays.filter(passing_tds=True, team=player_stats.team)
            long_tds = {"50TD": 0, "40TD": 0}
            for pass_td in passing_tds:
                if pass_td.passing_yds > 50:
                    long_tds['50TD'] += 1
                elif pass_td.passing_yds > 40:
                    long_tds['40TD'] += 1
            if long_tds['50TD'] > 0:
                score += long_tds['50TD'] * settings.SCORING_SYSTEM['passing']['50TD']
                text_array.append(str(long_tds['50TD']) + " 50+ Pass TDs")
            if long_tds['40TD'] > 0:
                score += long_tds['40TD'] * settings.SCORING_SYSTEM['passing']['40TD']
                text_array.append(str(long_tds['40TD']) + " 40-49 Pass TDs")
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
            # Rushing TDs present, check for long TD bonus
            rushing_tds = plays.filter(rushing_tds=True, team=player_stats.team)
            long_tds = {"50TD": 0, "40TD": 0}
            for pass_td in rushing_tds:
                if pass_td.rushing_yds > 50:
                    long_tds['50TD'] += 1
                elif pass_td.rushing_yds > 40:
                    long_tds['40TD'] += 1
            if long_tds['50TD'] > 0:
                score += long_tds['50TD'] * settings.SCORING_SYSTEM['rushing']['50TD']
                text_array.append(str(long_tds['50TD']) + " 50+ Rush TDs")
            if long_tds['40TD'] > 0:
                score += long_tds['40TD'] * settings.SCORING_SYSTEM['rushing']['40TD']
                text_array.append(str(long_tds['40TD']) + " 40-49 Rush TDs")
        if player_stats.fumbles_lost:
            score += player_stats.fumbles_lost * settings.SCORING_SYSTEM['rushing']['fumbles']
            text_array.append(str(player_stats.fumbles_lost) + " Fumbles")

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
            # Receiving TDs present, check for long TD bonus
            receiving_tds = plays.filter(receiving_tds=True, team=player_stats.team)
            long_tds = {"50TD": 0, "40TD": 0}
            for pass_td in receiving_tds:
                if pass_td.receiving_yds > 50:
                    long_tds['50TD'] += 1
                elif pass_td.receiving_yds > 40:
                    long_tds['40TD'] += 1
            if long_tds['50TD'] > 0:
                score += long_tds['50TD'] * settings.SCORING_SYSTEM['receiving']['50TD']
                text_array.append(str(long_tds['50TD']) + " 50+ Rec TDs")
            if long_tds['40TD'] > 0:
                score += long_tds['40TD'] * settings.SCORING_SYSTEM['receiving']['40TD']
                text_array.append(str(long_tds['40TD']) + " 40-49 Rec TDs")

        # Two Point Conversion
        if two_point:
            score += two_point * settings.SCORING_SYSTEM['misc']['2PT']
            text_array.append(str(two_point) + " 2PT")

        # Kicking Stats
        if player_stats.kicking_xpa:
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
            opponent = game.home
        else:
            points_against = game.score_away
            opponent = game.away

        # Get other game stats for defence
        sks, frc, frc_td, ints, int_td, safe, ret_td, two_pt = 0, 0, 0, 0, 0, 0, 0, 0
        for p in nflgame.combine_plays([game]):
            # Sacks
            if p.passing_sk > 0 and p.team == opponent:
                if not p.defense_frec:
                    # Dont count strip sack twice
                    sks += 1
            # Fumbles
            if p.defense_frec > 0 or p.fumbles_lost:
                # Accounts for fumbles on Special Teams
                if 'RECOVERED by '+team in p.desc or (p.team == opponent and p.fumbles_oob):
                    frc += 1
                    if p.defense_frec_tds > 0:
                        frc_td += 1
                    if p.passing_sk:
                        # Strip Sack
                        sks += 1
                else:
                    if p.defense_frec_tds > 0:
                        # Dont charge Fumble 6 on Defence, retard offence alert
                        points_against -= 6
            # Interceptions
            if p.defense_int > 0:
                if p.team == opponent:
                    ints += 1
                    if p.defense_int_tds > 0:
                        int_td += 1
                else:
                    if p.defense_int_tds > 0:
                        # Dont charge Pick 6 on Defence, retard offence alert
                        points_against -= 6
            # Safeties
            if p.defense_safe > 0:
                # Safety for defrence
                if p.team == opponent:
                    safe += 1
                else:
                    # Dont charge safety against defence; retarded offence's fault
                    points_against -= 2
            # Kick Return TDs
            if p.kickret_tds > 0 or p.puntret_tds > 0 or p.defense_misc_tds > 0 or p.kicking_rec_tds:
                for e in p.events:
                    if 'kickret_tds' in e or 'puntret_tds' in e or 'defense_misc_yds' in e or 'kicking_rec_tds' in e:
                        if e['team'] == team:
                            ret_td += 1

            if p.defense_xpblk > 0 and p.team == opponent:
                # Blocked Extra point, was it returned?
                if 'DEFENSIVE TWO-POINT ATTEMPT' in p.desc and 'ATTEMPT SUCCEEDS' in p.desc:
                    two_pt +=1
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
        # Two Point Return
        if two_pt:
            score += two_pt * settings.SCORING_SYSTEM['misc']['2PT']
            text_array.append(str(two_pt) + ' 2 PT Return')
        # Return TDs
        if ret_td:
            score += ret_td * settings.SCORING_SYSTEM['misc']['touchdowns']
            text_array.append(str(ret_td) + ' TDs')

        # Get points based on game score
        if points_against > 34:
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

        return score, text_array
    else:
        return 0, ['']


def get_player_opponent_string(team, week, year, kind):
    if team == 'JAC':
        team = 'JAX'
    try:
        game = nflgame.games(year, week=week, kind=kind, home=team, away=team)
        if len(game) == 0:
            # Game not played/in play
            future_games = nflgame.live._games_in_week(year=year, week=week, kind=kind)
            for f_game in future_games:
                ret_string = ''
                if f_game['home'] == team:
                    ret_string = 'v ' + f_game['away']
                elif f_game['away'] == team:
                    ret_string = '@ ' + f_game['home']
                if len(ret_string):
                    return ret_string + ' | Kickoff: ' + f_game['wday'] + ' ' + f_game['time']
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
        elif game.playing:
            # LIVE
            ret_string += ' | ' + game.nice_score() + ' LIVE'

    else:
        ret_string = 'Bye Week'

    return ret_string


def player_in_live(player, game):
    live_status = 'noposession'
    all_plays = list(game.drives.plays())
    if len(all_plays):
        last_play = all_plays[len(all_plays)-1]
        if last_play:
            if last_play.has_player(player.playerid):
                live_status = "onfield"
            elif last_play.team == player.team:
                live_status = "offfield"
    # Return possibilities "onfield", "offfield", "noposession"
    return live_status
