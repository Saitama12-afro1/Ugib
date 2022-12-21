from dataclasses import field
import django_filters
import csv
import glob
import xlsxwriter
import os
from xlsxwriter import Workbook 
from django.db.models import Q, F
from decimal import Decimal
from .models import UdsMeta, History, UdsMetaApr
from .HelperUdsMeta import HelperUdsMet
from django.contrib.auth.models import User, Group


class UdsMetaFilters(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    
    class Meta:
        model = UdsMeta
        fields = ["query"] # , "oid", "obj_year", "stor_folder"
        
    def universal_search(self, queryset, name, value):
        
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            result_query =  UdsMeta.objects.filter(
                Q(oid__icontains=value)
            )
        else:
            result_query =  UdsMeta.objects.filter(
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
     
            
            with open('stockitems_misuper.csv', 'w', newline="", encoding="utf-8") as myfile:  
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=",", dialect=csv.Dialect.delimiter)
                wr.writerow(HelperUdsMet._all_columns,)
                for i in result_query:
                    form_data = HelperUdsMet.create_dict_from_uds(i)
                    wr.writerow(list(form_data.values()))

            for csvfile in glob.glob(os.path.join('.', '*.csv')):
                workbook = xlsxwriter.Workbook()
                workbook = Workbook("result_query" + '.xlsx')
                worksheet = workbook.add_worksheet()
                with open(csvfile, 'rt', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for r, row in enumerate(reader):
                        for c, col in enumerate(row):
                            worksheet.write(r, c, col)
                workbook.close()
        return result_query
        
class UdsMetaAprFilters(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    
    class Meta:
        model = UdsMetaApr
        fields = ["query"] # , "oid", "obj_year", "stor_folder"
        
    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            result_query =  UdsMetaApr.objects.filter(
                Q(oid__icontains=value)
            )

        else: 
            result_query = UdsMetaApr.objects.filter(
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
        with open('stockitems_misuper.csv', 'w', newline="", encoding="utf-8") as myfile:  
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=",", dialect=csv.Dialect.delimiter)
            wr.writerow(HelperUdsMet._all_columns,)
            for i in result_query:
                form_data = HelperUdsMet.create_dict_from_uds(i)
                wr.writerow(list(form_data.values()))

        for csvfile in glob.glob(os.path.join('.', '*.csv')):
            workbook = xlsxwriter.Workbook()
            workbook = Workbook("result_query" + '.xlsx')
            worksheet = workbook.add_worksheet()
            with open(csvfile, 'rt', encoding='utf-8') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)
            workbook.close()
        return result_query
        
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
            query =  History.objects.filter(date__range=[date1, date2]).order_by("-id")
        else:
            split_value = value.split(' ')
            buff = value.split(".")
            if len(buff) == 3:
                date = f"{buff[2]}-{buff[1]}-{buff[0]}"
            else:
                date = ""
            if value in ('01found', 'apr', 'grr-stage', 'grr-accom'):
                query =  History.objects.filter(Q(fond__icontains=value)).order_by("-id")
            if value in ('create', 'bascet', 'delete', 'update'):
                query = History.objects.filter(Q(typeAction__icontains=value)).order_by("-id")
            if User.objects.filter(last_name=value).exists():
                query =  History.objects.filter(Q(my_user__last_name__icontains=value)).order_by("-id")
            query = History.objects.filter(Q(date__icontains=date)
                ).order_by("-id")
        if query:
            return query
        else:
            return queryset
