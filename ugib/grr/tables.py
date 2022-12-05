from django_tables2 import tables, TemplateColumn

from crud.tables import UdsMetaTable
from .models import UdsMetaGrrAccom, UdsMetaGrrStage


class UdsMetaGrrStageTable(UdsMetaTable, tables.Table):

 
    class Meta:
        model = UdsMetaGrrStage
        template_name = "grr/index/grr_stage/uds_meta_grr_stage.html"
        sequence = ('Delete','Exel', 'Update','Bascet')

class UdsMetaGrrAccomTable(UdsMetaTable, tables.Table):
 
    class Meta:
        model = UdsMetaGrrAccom
        template_name = "grr/index/grr_accom/uds_meta_grr_accom.html"
        sequence = ('Delete','Exel', 'Update','Bascet')