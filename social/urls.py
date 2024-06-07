from django.urls import path
from .views import (
    IndexView, LoginView,SignOutView, ProfileView, NotificationView, SignUp,PostView,
    AddProfileView,AboutView,CommentView,SearchUsersView,LikePostView,
    FollowUserView,DeletePostView,SendMessageView,InboxView,UsersListView
)
urlpatterns = [
    path('', LoginView.as_view(), name='signin'),
    path('index/', IndexView.as_view(), name='index'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('notification/', NotificationView.as_view(), name='notification'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signout/', SignOutView.as_view(), name='signout'),
    path('posts/', PostView.as_view(), name='posts'),
    path('aboutt/', AboutView.as_view(), name='aboutt'),
    path('edit_about/<int:pk>/', AboutView.as_view(), name='edit_about'),
    path('add_profile/', AddProfileView.as_view(), name='add_profile'),
    path('edit_profile/<int:pk>/', AddProfileView.as_view(), name='edit_profile'),
    path('comment/', CommentView.as_view(), name='comment'), 
    path('edit_comment/', CommentView.as_view(), name='edit_comment'),    
    path('search-users/', SearchUsersView.as_view(), name='search-users'),
    path('like_post/', LikePostView.as_view(), name='like_post'),
    path('posts/edit/<int:pk>/', PostView.as_view(), name='edit_post'),
    path('follow_user/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('posts/delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('users/', UsersListView.as_view(), name='user_list'),  
    path('send_message/<int:recipient_id>/', SendMessageView.as_view(), name='send_message'),

]
