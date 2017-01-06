"""urlconf for the base application"""

from django.conf.urls import url

from .views.team_views import team_home, live_scores
from .views.base_views import home, login_form, logout_form, register_form, story
from .views.commish_views import commish_home


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/$',login_form, name='login'),
    url(r'^logout/$',logout_form, name='logout'),
    url(r'^register/$',register_form, name='register'),
    url(r'^story/(?P<story_id>\w+)/$', story, name='story'),
    url(r'^team/(?P<team_id>\w+)/$', team_home, name='team'),
    url(r'^live-scores/$', live_scores, name='live-scores'),
    url(r'^commish/$', commish_home, name='commish')
]
