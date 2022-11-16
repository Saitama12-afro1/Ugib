from django.urls import path

from . import views
from crud.views import UdsMetaHTMxTableView

app_name='crud'
urlpatterns = [
    path('', UdsMetaHTMxTableView.as_view(), name='table'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('profile/bascet/', views.bascet, name='bascet'),
    path('profile/history/', views.history_views, name='history'),
    path('test/', views.test, name='test'),
    path('get_html/', views.get_html, name='test'),
    path('password_change', views.password_change, name = "password_change"),
]
