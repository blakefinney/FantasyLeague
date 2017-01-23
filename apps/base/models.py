"""Base models"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings


class TeamManager(models.Manager):
    def create_team(self, team_id):
        team = self.create(team_id=team_id)
        return team


class RosterManager(models.Manager):
    def create_roster(self):
        roster = self.create()
        return roster


class PlayerManager(models.Manager):
    def create_player(self, ng_player=None):
        esb_id = ''
        if hasattr(ng_player, 'esb_id'):
            esb_id = ng_player.esb_id
        player = self.create(ng_id=ng_player.playerid, esb_id=esb_id, team=ng_player.team, fantasy_team=None,
                             position=ng_player.position, name=ng_player.name, status='Free Agent')
        return player


class Team(models.Model):
    # Team Manager Class
    objects = TeamManager()
    # Fields
    team_id = models.CharField(max_length=7, default="Team-0")
    team_owner = models.CharField(max_length=30, default="noowner")
    team_name = models.CharField(max_length=30, default="Insert Team Name Here")
    championships = models.IntegerField(default=0)

    def get_roster(self):
        return self.roster.get_roster()

    def add_player(self, player):
        # Update Player
        player.status = "Owned"
        player.fantasy_team = self
        player.save()
        # Add Player to bench
        success = self.roster.add_to_bench(player)
        return success

    pass


# Roster class
class Player(models.Model):
    objects = PlayerManager()
    ng_id = models.CharField(max_length=30, default='noplayer')
    esb_id = models.CharField(max_length=30, default='')
    name = models.CharField(max_length=50, default='unknown')
    position = models.CharField(max_length=5, default='UNK')
    team = models.CharField(max_length=5, default='UNK')
    fantasy_team = models.ForeignKey(Team, null=True)
    status = models.CharField(max_length=15, default='Free Agent')

    def is_free_agent(self):
        if self.status == 'Free Agent' or not self.status:
            return True
        else:
            return False


# Roster class
class Roster(models.Model):
    # Roster Key
    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Quarterbacks
    QB1 = models.ForeignKey(Player, null=True, related_name="QB1")
    QB2 = models.ForeignKey(Player, null=True, related_name="QB2")
    # Running Backs
    RB1 = models.ForeignKey(Player, null=True, related_name="RB1")
    RB2 = models.ForeignKey(Player, null=True, related_name="RB2")
    # Wide Receivers
    WR1 = models.ForeignKey(Player, null=True, related_name="WR1")
    WR2 = models.ForeignKey(Player, null=True, related_name="WR2")
    # Tight Ends
    TE1 = models.ForeignKey(Player, null=True, related_name="TE1")
    # Flex Spots
    FLEX1 = models.ForeignKey(Player, null=True, related_name="FLEX1")
    FLEX2 = models.ForeignKey(Player, null=True, related_name="FLEX2")
    FLEX3 = models.ForeignKey(Player, null=True, related_name="FLEX3")
    # Kicker
    K1 = models.ForeignKey(Player, null=True, related_name="K1")
    # Defence
    DEF1 = models.CharField(max_length=15, default="noplayer")
    # Bench Array
    BENCH = models.CharField(max_length=150, default="[]")

    def get_roster(self):
        return {"starting": {
                        "QB": [self.QB1, self.QB2],
                        "RB": [self.RB1, self.RB2],
                        "WR": [self.WR1, self.WR2],
                        "TE": [self.TE1],
                        "FLEX": [self.FLEX1, self.FLEX2, self.FLEX3],
                        "K": [self.K1],
                        "DEF": [self.DEF1]
                    },
                "bench": self.BENCH.split(',')
            }

    def set_roster(self, lineup_object):
        do = 'nothing'
        #self.QB1 = lineup_array[0] or 'noplayer'
        #self.QB2 = lineup_array[1] or 'noplayer'
        #self.RB1 = lineup_array[2] or 'noplayer'
        #self.RB2 = lineup_array[3] or 'noplayer'
        #self.WR1 = lineup_array[4] or 'noplayer'
        #self.WR2 = lineup_array[5] or 'noplayer'
        #self.TE1 = lineup_array[6] or 'noplayer'
        #self.FLEX1 = lineup_array[7] or 'noplayer'
        #self.FLEX2 = lineup_array[8] or 'noplayer'
        #self.FLEX3 = lineup_array[9] or 'noplayer'
        #self.K1 = lineup_array[10] or 'noplayer'
        #self.DEF1 = lineup_array[11] or 'noplayer'

    def get_roster_size(self):
        players = 0
        if self.QB1:
            players += 1
        if self.QB2:
            players += 1
        if self.RB1:
            players += 1
        if self.RB2:
            players += 1
        if self.WR1:
            players += 1
        if self.WR2:
            players += 1
        if self.TE1:
            players += 1
        if self.FLEX1:
            players += 1
        if self.FLEX2:
            players += 1
        if self.FLEX3:
            players += 1
        if self.K1:
            players += 1
        players += len(self.BENCH.split(','))

        return players

    def add_to_bench(self, player):
        if self.get_roster_size() >= settings.MAX_ROSTER_SIZE:
            return False
        b_array = self.BENCH.split(',')
        b_array.append(player.ng_id)
        b_string = ''
        for b in b_array:
            if b_string != '':
                b_string += ','
            b_string += b
        self.BENCH = b_string
        self.save()
        return True

class Playoffs(models.Model):
    playoff_teams = models.IntegerField(default=2)


class Schedule(models.Model):
    year = models.IntegerField(default=0)
    number_of_weeks = models.IntegerField(default=1)
    playoffs = models.OneToOneField(
        Playoffs,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def get_number_of_weeks(self):
        return self.number_of_weeks

    def get_matchup(self, team_id=None, week_no=None):
        opponent_id = None
        try:
            matchup = Matchup.objects.get(parent_schedule=self, week_number=week_no, home_team=team_id)
            opponent_id = matchup.away_team
        except ObjectDoesNotExist:
            # Team not at home, check away
            matchup = None
        if not matchup:
            try:
                matchup = Matchup.objects.get(parent_schedule=self, week_number=week_no, away_team=team_id)
                opponent_id = matchup.home_team
            except ObjectDoesNotExist:
                # Team not away, on bye week so return None
                matchup = None
        return matchup, opponent_id


class Matchup(models.Model):
    parent_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    week_number = models.IntegerField(default=0)

    home_team = models.ForeignKey(Team, on_delete=None, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=None, related_name='away_team')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)


class Standings(models.Model):
    parent_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    division_name = models.CharField(max_length=20, default="Division Name here")
    number_of_teams = models.IntegerField(default=1)
    playoff_teams = models.IntegerField(default=1)

