from django.urls import path

from . import views
from crud.views import UdsMetaHTMxTableView, UdsMetaAprHTMxTableView

app_name='crud'
urlpatterns = [
    path('', UdsMetaHTMxTableView.as_view(), name='table'),
    path('apr/', UdsMetaAprHTMxTableView.as_view(), name='table_apr'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('profile/bascet/', views.bascet, name='bascet'),
    path('profile/history/', views.history_views, name='history'),
    path('test/', views.test, name='test'),
    path('get_html_uds/', views.get_html_uds, name='test'),
    path('get_html_apr/', views.get_html_apr, name='test'),
    path('password_change', views.password_change, name = "password_change"),
]
