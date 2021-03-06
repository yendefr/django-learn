from django.urls import path
from .views import post_list, post_detail, post_share, post_search
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('search/', post_search, name='post_search'),
    path('rss/', LatestPostsFeed(), name='latest_posts_feed')
]
