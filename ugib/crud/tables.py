from django.utils.html import format_html
from django_tables2 import tables, TemplateColumn, Column, A
from django.db.models import Subquery, OuterRef
from django.db import models
import django_tables2

from .models import UdsMeta, History, UdsMetaApr
from grr.models import UdsMetaProtocols


class UdsMetaTable(tables.Table):
    
    Update = TemplateColumn(template_name = "crud/tables_utilits/update_button_with_modal_wind.html")
    Delete = TemplateColumn(template_name = "crud/tables_utilits/delete_button.html")
    Bascet = TemplateColumn(template_name="crud/tables_utilits/bascet_button.html")
    Exel = TemplateColumn(template_name="crud/tables_utilits/csv_button.html")
    
    class Meta:
        model = UdsMeta
        template_name = "crud/index/01fond/uds_table_htmx.html"
        sequence = ('Delete','Exel', 'Update','Bascet')


class UdsMetaAprTable(UdsMetaTable,tables.Table):
    
    class Meta:
        model = UdsMetaApr
        template_name = "crud/index/apr/uds_meta_apr_table.html"
        sequence = ('Delete','Exel', 'Update','Bascet')
        exclude = ('path_cloud_ref', 'path_local_ref')


class HistoryTable(tables.Table):
    class Meta:
        model = History
        
        
        
        