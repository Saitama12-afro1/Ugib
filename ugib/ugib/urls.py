
from django.contrib import admin
from django.urls import path, include
from crud.views import UdsMetaHTMxTableView
urlpatterns = [
    path('', include("crud.urls")),
    path('', include("grr.urls")),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
]
handler404 = 'crud.views.page_not_found'