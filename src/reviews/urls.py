from django.urls import path
from reviews import views
from reviews.views import user_posts, delete_ticket, delete_review

app_name = "reviews"


urlpatterns = [
    path('',  views.feed, name='home'),
    path('feed/', views.feed, name='feed'),
    path('create/', views.create_review, name='create_review'),
    path('reply_to_ticket/<int:ticket_id>', views.reply_to_ticket, name='reply_to_ticket'),
    path('user_posts', views.user_posts, name='user_post'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('user_posts/', user_posts, name='user_posts'),
    path('delete_review/<int:id>/', delete_review, name='delete_review'),
    path('delete_ticket/<int:id>/', delete_ticket, name='delete_ticket'),
]