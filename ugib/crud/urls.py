from django.urls import path
from . import views

app_name='crud'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('profile/bascet', views.bascet, name='bascet'),
]