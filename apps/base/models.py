"""Base models"""
from django.db import models


class TeamManager(models.Manager):
    def create_team(self, team_id):
        team = self.create(team_id=team_id)
        return team

class RosterManager(models.Manager):
    def create_roster(self):
        roster = self.create()
        return roster


# Roster class
class Roster(models.Model):
    # Quarterbacks
    QB1 = models.CharField(max_length=15, default="noplayer")
    QB2 = models.CharField(max_length=15, default="noplayer")
    # Running Backs
    RB1 = models.CharField(max_length=15, default="noplayer")
    RB2 = models.CharField(max_length=15, default="noplayer")
    # Wide Receivers
    WR1 = models.CharField(max_length=15, default="noplayer")
    WR2 = models.CharField(max_length=15, default="noplayer")
    # Tight Ends
    TE1 = models.CharField(max_length=15, default="noplayer")
    # Flex Spots
    FLEX1 = models.CharField(max_length=15, default="noplayer")
    FLEX2 = models.CharField(max_length=15, default="noplayer")
    FLEX3 = models.CharField(max_length=15, default="noplayer")
    # Kicker
    K1 = models.CharField(max_length=15, default="noplayer")
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



class Team(models.Model):
    # Team Manager Class
    objects = TeamManager()
    # Roster Key
    roster = models.OneToOneField(
        Roster,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Fields
    team_id = models.CharField(max_length=7, default="Team-0")
    team_owner = models.CharField(max_length=30, default="noowner")
    team_name = models.CharField(max_length=30, default="Insert Team Name Here")
    championships = models.IntegerField(default=0)
    schedule = None

    def get_roster(self):
        return self.roster.get_roster()

    def set_roster(self, lineup_object):
        return self.roster.set_roster(lineup_object)

    pass
