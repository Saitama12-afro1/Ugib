from dataclasses import field
import csv
import glob
import xlsxwriter
import os
import django_filters 
from xlsxwriter import Workbook 
from django.db.models import Q, F
from decimal import Decimal
from .models import UdsMetaGrrStage, UdsMetaGrrAccom
from crud.HelperUdsMeta import HelperUdsMet

class UdsMetaGrrStageFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    
    class Meta:
        model = UdsMetaGrrStage
        fields = ["query"] # , "oid", "obj_year", "stor_folder"
        
    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            result_query  =  UdsMetaGrrStage.objects.filter(
               Q(oid__icontains=value) | Q(stor_folder__icontains=value)
            )
        elif len(UdsMetaGrrStage.objects.filter(
             Q(stor_folder__icontains=value)
            )) !=0:
            print(111111111111111)
            result_query =  UdsMetaGrrStage.objects.filter(
             Q(stor_folder__icontains=value)
            )
        else: 
            
            result_query =  UdsMetaGrrStage.objects.filter(
            Q(obj_authors__icontains=value)  | Q(uniq_id__icontains=value)
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
    
    
class UdsMetaGrrAccomFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    
    class Meta:
        model = UdsMetaGrrAccom
        fields = ["query"] # , "oid", "obj_year", "stor_folder"
        
    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            result_query =  UdsMetaGrrAccom.objects.filter(
               Q(oid__icontains=value) | Q(stor_folder__icontains=value)
            )
        elif len(UdsMetaGrrAccom.objects.filter(
            Q(stor_folder__icontains=value)
        )) != 0:
            result_query =  UdsMetaGrrAccom.objects.filter(
                Q(stor_folder__icontains=value)
            )
        else:
            result_query =  UdsMetaGrrAccom.objects.filter(
            Q(obj_authors__icontains=value) | Q(uniq_id__icontains=value)
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