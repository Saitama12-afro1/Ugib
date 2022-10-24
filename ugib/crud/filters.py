from dataclasses import field
import django_filters 
from django.db.models import Q
from decimal import Decimal
from .models import UdsMeta, History

class UdsMetaFilters(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    
    class Meta:
        model = UdsMeta
        fields = ["query"] # , "oid", "obj_year", "stor_folder"
        
    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            return UdsMeta.objects.filter(
                Q(oid__icontains=value)
            )

        return UdsMeta.objects.filter(
            Q(obj_authors__icontains=value) | Q(stor_folder__icontains=value) | Q(stor_reason__icontains=value)
        )
        
        
class HistoryFilter(django_filters.FilterSet):
    
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    
    class Meta:
        model = History
        fields = ["query"]
        
    def universal_search(self, queryset, name, value):
        return History.objects.filter(
            Q(typeAction__icontains=value) | Q(order__icontains=value) | Q(udsMeta__icontains=value)
        )