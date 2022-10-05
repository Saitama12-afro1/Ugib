from django.urls import path

from . import views
from crud.views import UdsMetaHTMxTableView

app_name='crud'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('profile/bascet', views.bascet, name='bascet'),
    path('profile/history', views.history_views, name='history'),
    path('test', views.test, name='test'),
    path('table', UdsMetaHTMxTableView.as_view(), name = "table"),
]
