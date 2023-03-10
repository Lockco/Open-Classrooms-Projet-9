from django.urls import path
from . import views
from .views import search_user

app_name = 'followers'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('follow/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
    path('search_user/', search_user, name='search_user'),

]