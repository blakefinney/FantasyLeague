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


class FpManager(models.Manager):
    def create_fp(self, player, year):
        fp = self.create(player=player, year=year)
        return fp


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

    def drop_player(self, player):
        # Update Player
        player.status = "Free Agent"
        player.fantasy_team = None
        player.save()
        # Add Player to bench
        success = self.roster.drop_player(player)
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

    def is_owned_by(self, team):
        if self.status == 'Owned' and self.fantasy_team == team:
            return True
        else:
            return False

    def toJSON(self):
        pl = {}
        pl['ng_id'] = self.ng_id
        pl['esb_id'] = self.esb_id
        pl['name'] = self.name
        pl['position'] = self.position
        pl['team'] = self.team
        return pl


# Roster class
class FantasyPoints(models.Model):
    objects = FpManager()

    player = models.ForeignKey(Player, default='')
    year = models.IntegerField(default=0)

    total = models.FloatField(default=None, null=True)

    week1 = models.FloatField(default=None, null=True)
    week2 = models.FloatField(default=None, null=True)
    week3 = models.FloatField(default=None, null=True)
    week4 = models.FloatField(default=None, null=True)
    week5 = models.FloatField(default=None, null=True)
    week6 = models.FloatField(default=None, null=True)
    week7 = models.FloatField(default=None, null=True)
    week8 = models.FloatField(default=None, null=True)
    week9 = models.FloatField(default=None, null=True)
    week10 = models.FloatField(default=None, null=True)
    week11 = models.FloatField(default=None, null=True)
    week12 = models.FloatField(default=None, null=True)
    week13 = models.FloatField(default=None, null=True)
    week14 = models.FloatField(default=None, null=True)
    week15 = models.FloatField(default=None, null=True)
    week16 = models.FloatField(default=None, null=True)
    week17 = models.FloatField(default=None, null=True)

    def calc_total(self):
        self.total = 0
        if self.week1:
            self.total += self.week1
        if self.week2:
            self.total += self.week2
        if self.week3:
            self.total += self.week3
        if self.week4:
            self.total += self.week4
        if self.week5:
            self.total += self.week5
        if self.week6:
            self.total += self.week6
        if self.week7:
            self.total += self.week7
        if self.week8:
            self.total += self.week8
        if self.week9:
            self.total += self.week9
        if self.week10:
            self.total += self.week10
        if self.week11:
            self.total += self.week11
        if self.week12:
            self.total += self.week12
        if self.week13:
            self.total += self.week13
        if self.week14:
            self.total += self.week14
        if self.week15:
            self.total += self.week15
        if self.week16:
            self.total += self.week16
        if self.week17:
            self.total += self.week17


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
    DEF1 = models.ForeignKey(Player, null=True, related_name="DEF1")
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

    def set_lineup(self, st, bench_array):
        def check_player(string):
            if string == 'noplayer':
                return None
            else:
                return Player.objects.get(ng_id=string)

        self.QB1 = check_player(st[0])
        self.QB2 = check_player(st[1])
        self.RB1 = check_player(st[2])
        self.RB2 = check_player(st[3])
        self.WR1 = check_player(st[4])
        self.WR2 = check_player(st[5])
        self.TE1 = check_player(st[6])
        self.FLEX1 = check_player(st[7])
        self.FLEX2 = check_player(st[8])
        self.FLEX3 = check_player(st[9])
        self.K1 = check_player(st[10])
        self.DEF1 = check_player(st[11])

        self.BENCH = bench_array

        self.save()

    def get_roster_array(self):
        arr = [self.QB1, self.QB2, self.RB1, self.RB2, self.WR1, self.WR2, self.TE1, self.FLEX1, self.FLEX2, self.FLEX3, self.K1, self.DEF1]
        ret_arr = []
        ben = self.BENCH.split(',')
        for b in ben:
            if b and b != '':
                arr.append(Player.objects.get(ng_id=b).toJSON())
        for a in arr:
            if not a:
                arr.remove(a)
            else:
                ret_arr.append(a.toJSON())
        return ret_arr

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

    def drop_player(self, player):
        dropped = False
        if player.ng_id in self.BENCH:
            self.BENCH = self.BENCH.replace(','+player.ng_id, '')
            self.BENCH = self.BENCH.replace(player.ng_id+',', '')
            dropped = True
        else:
            if self.QB1 == player:
                self.QB1 = None
                dropped = True
            elif self.QB2 == player:
                self.QB2 = None
                dropped = True
            elif self.RB1 == player:
                self.RB1 = None
                dropped = True
            elif self.RB2 == player:
                self.RB2 = None
                dropped = True
            elif self.WR1 == player:
                self.WR1 = None
                dropped = True
            elif self.WR2 == player:
                self.WR2 = None
                dropped = True
            elif self.TE1 == player:
                self.TE1 = None
                dropped = True
            elif self.FLEX1 == player:
                self.FLEX1 = None
                dropped = True
            elif self.FLEX2 == player:
                self.FLEX2 = None
                dropped = True
            elif self.FLEX3 == player:
                self.FLEX3 = None
                dropped = True
            elif self.K1 == player:
                self.K1 = None
                dropped = True
            elif self.DEF1 == player:
                self.DEF1 = None
                dropped = True
        self.save()
        return dropped


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
    year = models.IntegerField(default=0)
    archive = models.CharField(max_length=1000, default="")
    division_name = models.CharField(max_length=20, default="Division Name here")
    number_of_teams = models.IntegerField(default=1)
    playoff_teams = models.IntegerField(default=1)


class Trade(models.Model):
    proposing_team = models.ForeignKey(Team, related_name="PropTeam")
    receiving_team = models.ForeignKey(Team, related_name="RecTeam")

    prop_players = models.CharField(max_length=1000)
    rec_players = models.CharField(max_length=1000)

    accepted_date = models.DateTimeField()
    process_date = models.DateTimeField()
