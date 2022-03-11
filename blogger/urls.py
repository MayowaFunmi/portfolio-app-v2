from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blogger'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('add_post/', views.post_create, name='post_create'),
    path('edit_post/<int:id>/<str:slug>/', views.post_edit, name='post_edit'),
    #path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:id>/<int:year>/<int:month>/<int:day>/<slug:posts>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    #path("<category>/", views.blog_category, name="blog_category"),
    path("category/<str:cats>/", views.post_category, name="post_category"),
    path("tags/<str:tag>/", views.post_tags, name="post_tags"),
    path('like/<int:id>/<int:year>/<int:month>/<int:day>/<slug:posts>/', views.like_view, name='like_post'),
    path('post_detail_search/', views.post_detail_search, name='post_detail_search'),
    path('<int:id>/<str:slug>/delete/', views.post_delete, name='post_delete'),
]