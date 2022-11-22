
from django_tables2 import tables, TemplateColumn

from .models import UdsMeta, History, UdsMetaApr

class UdsMetaTable(tables.Table):

    Update = TemplateColumn(template_name = "crud/tables_utilits/update_button_with_modal_wind.html")
    Delete = TemplateColumn(template_name = "crud/tables_utilits/delete_button.html")
    Bascet = TemplateColumn(template_name="crud/tables_utilits/bascet_button.html")
    Exel = TemplateColumn(template_name="crud/tables_utilits/csv_button.html")
    
    def get_top_pinned_data(self):
        return super().get_top_pinned_data()
 
    class Meta:
        model = UdsMeta
        template_name = "crud/index/uds_table_htmx.html"
        sequence = ('Delete','Exel', 'Update','Bascet')


class UdsMetaAprTable(tables.Table):

    Update = TemplateColumn(template_name = "crud/tables_utilits/update_button_with_modal_wind.html")
    Delete = TemplateColumn(template_name = "crud/tables_utilits/delete_button.html")
    Bascet = TemplateColumn(template_name="crud/tables_utilits/bascet_button.html")
    Exel = TemplateColumn(template_name="crud/tables_utilits/csv_button.html")
    
    def get_top_pinned_data(self):
        return super().get_top_pinned_data()
 
    class Meta:
        model = UdsMetaApr
        template_name = "crud/index/uds_meta_apr_table.html"
        sequence = ('Delete','Exel', 'Update','Bascet')
       

class HistoryTable(tables.Table):
    class Meta:
        model = History
        
        
        
        