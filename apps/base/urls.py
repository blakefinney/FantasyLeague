"""urlconf for the base application"""

from django.conf.urls import url

from .views.base_views import home, story
from .views.team_views import team_home


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^story/(?P<story_id>\w+)/$', story, name='story'),
    url(r'^team/(?P<team_id>\w+)/$', team_home, name='team')
]
