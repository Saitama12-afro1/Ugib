from django.urls import path

from . import views



app_name='grr'
urlpatterns = [
    path('grr/', views.test , name='tttt'),
    path('grr-accom/', views.UdsMetaGrrAccomHTMxTableView.as_view(), name = "grr-accom"),
    path('grr-stage/', views.UdsMetaGrrStageHTMxTableView.as_view(), name = "grr-stage"),
    path('get_html_grr_stage/', views.get_html_grr_stage, name='test'),
]
