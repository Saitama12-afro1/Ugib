from django_tables2 import tables, TemplateColumn


from .models import UdsMetaGrrAccom, UdsMetaGrrStage


class UdsMetaGrrStageTable(tables.Table):

    Update = TemplateColumn(template_name = "crud/tables_utilits/update_button_with_modal_wind.html")
    Delete = TemplateColumn(template_name = "crud/tables_utilits/delete_button.html")
    Bascet = TemplateColumn(template_name="crud/tables_utilits/bascet_button.html")
    Exel = TemplateColumn(template_name="crud/tables_utilits/csv_button.html")
    
    def get_top_pinned_data(self):
        return super().get_top_pinned_data()
 
    class Meta:
        model = UdsMetaGrrStage
        template_name = "grr/index/grr_stage/uds_meta_grr_stage.html"
        sequence = ('Delete','Exel', 'Update','Bascet')

class UdsMetaGrrAccomTable(tables.Table):

    Update = TemplateColumn(template_name = "crud/tables_utilits/update_button_with_modal_wind.html")
    Delete = TemplateColumn(template_name = "crud/tables_utilits/delete_button.html")
    Bascet = TemplateColumn(template_name="crud/tables_utilits/bascet_button.html")
    Exel = TemplateColumn(template_name="crud/tables_utilits/csv_button.html")
    
    def get_top_pinned_data(self):
        return super().get_top_pinned_data()
 
    class Meta:
        model = UdsMetaGrrAccom
        template_name = "grr/index/grr_accom/uds_meta_grr_accom.html"
        sequence = ('Delete','Exel', 'Update','Bascet')