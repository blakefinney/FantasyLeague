"""urlconf for the base application"""

from django.conf.urls import url

from .views.team_views import team_home, save_team, live_scores
from .views.player_views import player_info, player_list, transaction_player
from .views.base_views import home, login_form, logout_form, register_form, story
from .views.commish_views import commish_home, commish_update_players, commish_end_gameweek, \
    commish_update_fantasy_points

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/$',login_form, name='login'),
    url(r'^logout/$',logout_form, name='logout'),
    url(r'^register/$',register_form, name='register'),
    url(r'^story/(?P<story_id>\w+)/$', story, name='story'),
    url(r'^my-team/$', team_home, name='team'),
    url(r'^team/(?P<team_id>\w+)/$', team_home, name='team'),
    url(r'^save-team/(?P<team_id>\w+)/$', save_team, name='save-team'),
    url(r'^players/$', player_list, name='players'),
    url(r'^live-scores/$', live_scores, name='live-scores'),
    url(r'^player-info/(?P<player_id>[\w-]+)/$', player_info, name='player-info'),
    url(r'^transaction-player/$', transaction_player, name='transaction-player'),
    # Commish Pages
    url(r'^commish/$', commish_home, name='commish'),
    url(r'^commish/update-players/$', commish_update_players, name='commish_update-players'),
    url(r'^commish/update-fantasy-points/$', commish_update_fantasy_points, name='commish_update-fantasy-points'),
    url(r'^commish/end-gameweek/$', commish_end_gameweek, name='commish_end-gameweek')
]
