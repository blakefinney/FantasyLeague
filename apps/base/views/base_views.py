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
    return render(request, 'base/home.html', context=template_context)


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
