from django.urls import path

from . import views
from crud.views import UdsMetaHTMxTableView, UdsMetaAprHTMxTableView, HistoryView

app_name='crud'
urlpatterns = [
    path('', UdsMetaHTMxTableView.as_view(), name='table'),
    path('apr/', UdsMetaAprHTMxTableView.as_view(), name='table_apr'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('profile/bascet/', views.bascet, name='bascet'),
    path('profile/history/', HistoryView.as_view(), name='history'),
    path('test/', views.test, name='test'),
    path('get_html_uds/', views.get_html_uds, name='get_html_uds'),
    path('get_html_apr/', views.get_html_apr, name='get_html_apr'),
    path('password_change/', views.password_change, name = "password_change"),
    path('refresh/', views.refresh_view, name = "refresh_view"),
    path('create/', views.create_post, name='create')
    # path('')
]
