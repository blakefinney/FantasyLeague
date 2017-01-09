""" Some Helper Functions for the Wesbite"""
from django.conf import settings

def is_logged_in(request):
    return request.user.is_active


def calculate_week_score (player_stats):
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
    return score, text_array
