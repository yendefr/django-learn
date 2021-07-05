from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = 'Yendefr blog'
    link = '/blog/'
    description = 'Better then yours'

    @staticmethod
    def items():
        return Post.published.all()[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
