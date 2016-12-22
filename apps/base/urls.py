"""urlconf for the base application"""

from django.conf.urls import url

from .views.base_views import home, login, story


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/$',login,name='login'),
    url(r'^story/(?P<story_id>\w+)/$', story, name='story'),
]
