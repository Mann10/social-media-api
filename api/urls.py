from django.urls import path
from api.views import *

urlpatterns = [
    path('posts/',PostsView.as_view(),name='posts'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='details-posts'),
    path('comment/',CommentsView.as_view(),name='comments'),
    path('comment/<int:pk>/',CommentDetailView.as_view(),name='details-comments'),
    path('register/',Register.as_view(),name='register'),
    path('posts/users/<int:user_id>/',PostByRespectiveUser.as_view(),name='details-users'),
    path('posts/<int:post_id>/comments/',CommentsfromPostId.as_view(),name='details-comments'),
    path('posts/<int:post_id>/like/',LikePost.as_view(),name='like-post'),
    path('login/',LoginView.as_view(),name='login'),
    path('users/comments/',FetchLoggedInUsersComments.as_view(),name='details-users-comments'),
]