from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.aboutUs, name='aboutUs'),
    path('events', views.events, name='events'),
    path('event/<slug:event_slug>', views.event, name='event'),
    path('add_event/', views.add_event, name='add_event'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]