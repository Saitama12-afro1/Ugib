
from django.contrib import admin
from django.urls import path, include

from crud.views import UdsMetaHTMxTableView
urlpatterns = [
    path('', include("crud.urls")),

    path('admin/', admin.site.urls),
]
handler404 = 'crud.views.page_not_found'