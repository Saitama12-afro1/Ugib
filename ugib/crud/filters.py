from dataclasses import field
import django_filters 
from django.db.models import Q, F
from decimal import Decimal
from .models import UdsMeta, History, UdsMetaApr

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
            Q(obj_authors__icontains=value) | Q(stor_folder__icontains=value) | Q(uniq_id__icontains=value)
            | Q(obj_main_min__icontains=value) | Q(stor_date__icontains=value) | Q(stor_phys__icontains=value) | Q(stor_date__icontains=value)
            | Q(stor_dept__icontains=value) | Q(stor_desc__icontains=value) | Q(stor_fmts__icontains=value) | Q(stor_units__icontains=value)
            | Q(obj_name__icontains=value) | Q(type_of_work__icontains=value) | Q(stor_fmts__icontains=value) | Q(stor_person__icontains=value)
            | Q(obj_name__icontains=value) | Q(obj_synopsis__icontains=value) | Q(obj_type__icontains=value) | Q(obj_sub_type__icontains=value)
            | Q(obj_assoc_inv_nums__icontains=value) | Q(obj_year__icontains=value) | Q(obj_authors__icontains=value) | Q(obj_orgs__icontains=value)
            | Q(obj_restrict__icontains=value) | Q(obj_rights__icontains=value) | Q(obj_rdoc_name__icontains=value) | Q(obj_rdoc_num__icontains=value)
            | Q(obj_terms__icontains=value) | Q(obj_sources__icontains=value) | Q(obj_supl_info__icontains=value) | Q(obj_main_min__icontains=value)
            | Q(obj_group_min__icontains=value) | Q(obj_assoc_geol__icontains=value) | Q(spat_atd_ate__icontains=value) | Q(spat_loc__icontains=value)
            | Q(spat_num_grid__icontains=value) | Q(spat_coords_source__icontains=value) | Q(spat_toponim__icontains=value) | Q(inf_type__icontains=value)
            | Q(path_others__icontains=value) | Q(obj_main_group__icontains=value) | Q(obj_sub_group__icontains=value) | Q(obj_sub_group_ref__icontains=value)
        )
      
        
class UdsMetaAprFilters(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    
    class Meta:
        model = UdsMetaApr
        fields = ["query"] # , "oid", "obj_year", "stor_folder"
        
    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            return UdsMetaApr.objects.filter(
                Q(oid__icontains=value)
            )

        return UdsMetaApr.objects.filter(
            Q(obj_authors__icontains=value) | Q(stor_folder__icontains=value) | Q(uniq_id__icontains=value)
            | Q(obj_main_min__icontains=value) | Q(stor_date__icontains=value) | Q(stor_phys__icontains=value) | Q(stor_date__icontains=value)
            | Q(stor_dept__icontains=value) | Q(stor_desc__icontains=value) | Q(stor_fmts__icontains=value) | Q(stor_units__icontains=value)
            | Q(obj_name__icontains=value) | Q(type_of_work__icontains=value) | Q(stor_fmts__icontains=value) | Q(stor_person__icontains=value)
            | Q(obj_name__icontains=value) | Q(obj_synopsis__icontains=value) | Q(obj_type__icontains=value) | Q(obj_sub_type__icontains=value)
            | Q(obj_assoc_inv_nums__icontains=value) | Q(obj_year__icontains=value) | Q(obj_authors__icontains=value) | Q(obj_orgs__icontains=value)
            | Q(obj_restrict__icontains=value) | Q(obj_rights__icontains=value) | Q(obj_rdoc_name__icontains=value) | Q(obj_rdoc_num__icontains=value)
            | Q(obj_terms__icontains=value) | Q(obj_sources__icontains=value) | Q(obj_supl_info__icontains=value) | Q(obj_main_min__icontains=value)
            | Q(obj_group_min__icontains=value) | Q(obj_assoc_geol__icontains=value) | Q(spat_atd_ate__icontains=value) | Q(spat_loc__icontains=value)
            | Q(spat_num_grid__icontains=value) | Q(spat_coords_source__icontains=value) | Q(spat_toponim__icontains=value) | Q(inf_type__icontains=value)
            | Q(path_others__icontains=value) | Q(obj_main_group__icontains=value) | Q(obj_sub_group__icontains=value)
        )
        
        
class HistoryFilter(django_filters.FilterSet):
    
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    
    class Meta:
        model = History
        fields = ["query"]
        
    def universal_search(self, queryset, name, value:str):
        if "-" in value:
            val = value.split("-")
            buff = val[0].split(".")
            if len(buff) > 1:
                date1 = f"{buff[2]}-{buff[1]}-{buff[0]}"
            buff = val[1].split(".")
            if len(buff) > 1:
                date2 = f"{buff[2]}-{buff[1]}-{buff[0]}"
            return History.objects.filter(date__range=[date1, date2])
        split_value = value.split(' ')
        buff = value.split(".")
        if len(buff) == 3:
            date = f"{buff[2]}-{buff[1]}-{buff[0]}"
        else:
            date = ""
        if value in ('01found', 'apr', 'grr-stage', 'grr-accom'):
            return History.objects.filter(Q(fond__icontains=value))
        if value in ('create', 'bascet', 'delete', 'update'):
            return History.objects.filter(Q(typeAction__icontains=value))
        return History.objects.filter(
            Q(typeAction__icontains=value)| Q(my_user__last_name__icontains=value) | Q(my_user__first_name__icontains=value) 
            | Q(my_user__userinfo__departament__icontains=value) 
            | (Q(my_user__last_name__icontains=split_value[0])) | Q(date__icontains=date)
            )
