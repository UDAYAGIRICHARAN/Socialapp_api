from django.contrib import admin
from django.urls import path
from . import views, viewsPost



urlpatterns = [
    path('api/authenticate', views.userAuthentification),
    path('api/follow', views.userFollow),
    path('api/unfollow', views.userUnFollow),
    path('api/user', views.getFollowers),
    path('admin/', admin.site.urls),
    path('api/posts', viewsPost.managePost),
    path('api/posts/', viewsPost.managePost),

    path('api/like/', viewsPost.addLike),
    path('api/unlike/', viewsPost.removeLike),
    path('api/comment/', viewsPost.addComment),
    path('api/all_posts', viewsPost.allPosts),
]