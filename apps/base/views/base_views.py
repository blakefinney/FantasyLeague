"""Views for the base app"""
import nflgame
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPosts, GetPost

from django.conf import settings

from apps.base.helpers import is_logged_in


@login_required(login_url='/login/')
def home(request):
    """ Home Page View """
    if not is_logged_in(request):
        return HttpResponseRedirect('/login/')
    template_context = {}
    # Fetch Wordpress stories
    wp = Client('https://blakefinney.wordpress.com/xmlrpc.php', settings.WORDPRESS_USERNAME, settings.WORDPRESS_PASSWORD)
    all_posts = wp.call(GetPosts())
    if len(all_posts) > 0:
        stories = []
        for post in all_posts:
            stories.append({"id": post.id,
                            "title": post.title,
                            "image": post.thumbnail['link'],
                            "content":post.content})
        template_context.update(stories=stories)

    # Fetch Standings
    template_context.update(div1_standings=[{"team_id": 1, "team_name": "Team 1"}, {"team_id": 2, "team_name": "Team 2"}, {"team_id": 3, "team_name": "Team 3"}, {"team_id": 4, "team_name": "Team 4"}, {"team_id": 5, "team_name": "Team 5"}, {"team_id": 6, "team_name": "Team 6"}],
                            div2_standings=[{"team_id": 7, "team_name": "Team 7"}, {"team_id": 8, "team_name": "Team 8"}, {"team_id": 9, "team_name": "Team 9"}, {"team_id": 10, "team_name": "Team 10"}, {"team_id": 11, "team_name": "Team 11"}, {"team_id": 12, "team_name": "Team 12"}])

    template_context.update(div1_name='Northern Division',
                            div2_name='Southern Division')

    return render(request, 'base/home.html', context=template_context)


def login_form(request):
    """ Login View """
    if request.method == 'GET':
        template_context = {}
        return render(request, 'base/login.html', context=template_context)
    elif request.method == 'POST':
        # Redirect to homepage
        login_user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if login_user is not None:
            login(user=login_user,request=request)
        return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def logout_form(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_form(request):
    """ Register View """
    if request.method == 'GET':
        template_context = {}
        return render(request, 'base/register.html', context=template_context)
    elif request.method == 'POST':
        # Form Submitted
        if request.POST['secret'] == settings.ADMIN_SECRET_STRING or request.POST['secret'] in settings.SECRET_STRING_ARRAY:
            user = User.objects.create_user(username=request.POST['username'],
                                                 email=request.POST['email'],
                                                password=request.POST['password'],
                                                first_name=request.POST['firstname'],
                                                last_name=request.POST['lastname'])
            if request.POST['secret'] == settings.ADMIN_SECRET_STRING:
                user.is_staff = True
                user.is_superuser = True
            user.save()
            # Redirect to homepage
            return HttpResponseRedirect('/register')
        else:
            # Didn't provide string
            # Redirect to homepage
            return HttpResponseRedirect('/login/')


@login_required(login_url='/login/')
def story(request, story_id=None):
    """ Story View """
    if not is_logged_in(request):
        return HttpResponseRedirect('/login/')
    template_context = {}
    # Fetch Wordpress story
    wp = Client('https://blakefinney.wordpress.com/xmlrpc.php', settings.WORDPRESS_USERNAME,settings.WORDPRESS_PASSWORD)
    story = wp.call(GetPost(story_id))

    template_context.update(id=story.id,
                            title=story.title,
                            image=story.thumbnail['link'],
                            content=story.content)

    return render(request, 'base/story.html', context=template_context)
