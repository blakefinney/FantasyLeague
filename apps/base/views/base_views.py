"""Views for the base app"""

from django.shortcuts import render

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPosts, GetPost

from django.conf import settings


def home(request):
    """ Home Page View """
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

def login(request):
    """ Login View """
    template_context = {}
    return render(request, 'base/login.html', context=template_context)


def story(request, story_id=None):
    """ Story View """
    template_context = {}
    # Fetch Wordpress story
    wp = Client('https://blakefinney.wordpress.com/xmlrpc.php', settings.WORDPRESS_USERNAME,settings.WORDPRESS_PASSWORD)
    story = wp.call(GetPost(story_id))

    template_context.update(id=story.id,
                            title=story.title,
                            image=story.thumbnail['link'],
                            content=story.content)

    return render(request, 'base/story.html', context=template_context)
