from django.urls import path
from tickets import views
from tickets.views import TicketHome, edit_ticket


app_name = "tickets"


urlpatterns = [
    path('ticket/', TicketHome.as_view(), name='ticket_snippet'),
    path('create_ticket/', views.create_ticket, name='create-ticket'),
    path('edit_ticket/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
]