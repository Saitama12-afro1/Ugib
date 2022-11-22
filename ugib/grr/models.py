from django.db import models
from crud.models import UnlimitedCharField

def auto_incr_oid_grr_stage():#функция для осздания нового уникального oid
    largest = UdsMetaGrrStage.objects.all().order_by("oid").last()
    return largest.oid + 1

def auto_incr_oid_apr_accom():#функция для осздания нового уникального oid
    largest = UdsMetaGrrAccom.objects.all().order_by("oid").last()
    return largest.oid + 1

# Create your models here.
class UdsMetaGrrStage(models.Model):
    oid = models.BigIntegerField(default=auto_incr_oid_grr_stage, null = True, blank = True)
    uniq_id = UnlimitedCharField(primary_key = True)
    stor_folder = UnlimitedCharField( blank=True, null=True)
    stor_phys = UnlimitedCharField( blank=True, null=True)
    stor_reason = UnlimitedCharField( blank=True, null=True)
    stor_date = UnlimitedCharField( blank=True, null=True)
    stor_dept = UnlimitedCharField( blank=True, null=True)
    stor_person =UnlimitedCharField( blank=True, null=True)
    stor_desc = UnlimitedCharField( blank=True, null=True)
    stor_fmts = UnlimitedCharField( blank=True, null=True)
    stor_units = UnlimitedCharField( blank=True, null=True)
    obj_name = UnlimitedCharField( blank=True, null=True)
    type_of_work = UnlimitedCharField( blank=True, null=True)
    obj_synopsis = UnlimitedCharField( blank=True, null=True)#all null?
    obj_type = UnlimitedCharField( blank=True, null=True)
    obj_sub_type = UnlimitedCharField( blank=True, null=True)
    obj_assoc_inv_nums = UnlimitedCharField( blank=True, null=True)
    obj_date = UnlimitedCharField( blank=True, null=True)#all null?
    obj_year = UnlimitedCharField( blank=True, null=True)
    obj_authors = UnlimitedCharField(blank=True, null=True)
    obj_orgs = UnlimitedCharField( blank=True, null=True)
    obj_restrict = UnlimitedCharField( blank=True, null=True)#all null?
    obj_rights = UnlimitedCharField(blank=True, null=True)# тема повторятся дважды можно вынести в отдельный столбец
    obj_rdoc_name = UnlimitedCharField( blank=True, null=True)
    obj_rdoc_num = UnlimitedCharField( blank=True, null=True)
    obj_terms = UnlimitedCharField(blank=True, null=True)
    obj_sources = UnlimitedCharField( blank=True, null=True)#all null?
    obj_supl_info = UnlimitedCharField( blank=True, null=True)#all null?
    obj_main_min = UnlimitedCharField(blank=True, null=True)
    obj_supl_min = UnlimitedCharField( blank=True, null=True)
    obj_group_min = UnlimitedCharField( blank=True, null=True)
    obj_assoc_geol = UnlimitedCharField( blank=True, null=True)
    spat_atd_ate = UnlimitedCharField( blank=True, null=True)
    spat_loc = UnlimitedCharField(blank=True, null=True)
    spat_num_grid = UnlimitedCharField( blank=True, null=True)
    spat_coords_source = UnlimitedCharField(blank=True, null=True)
    spat_toponim = UnlimitedCharField(blank=True, null=True)
    inf_type = UnlimitedCharField( blank=True, null=True)
    inf_media = UnlimitedCharField(blank=True, null=True)
    path_others = UnlimitedCharField( blank=True, null=True)#all null 
    obj_main_group = UnlimitedCharField( blank=True, null=True)
    obj_sub_group = UnlimitedCharField( blank=True, null=True)
    path_local = UnlimitedCharField( blank=True, null=True)
    path_cloud =UnlimitedCharField( blank=True, null=True)
    status = UnlimitedCharField( blank=True, null=True)#all null
    timecode = UnlimitedCharField( blank=True, null=True)#all null
    
    
    class Meta:
        managed = False
        db_table = 'uds_meta_grr_stage'
    


class UdsMetaGrrAccom(models.Model):
    oid = models.BigIntegerField(default=auto_incr_oid_apr_accom, null = True, blank = True)
    uniq_id = UnlimitedCharField(primary_key = True)
    stor_folder = UnlimitedCharField( blank=True, null=True)
    stor_phys = UnlimitedCharField( blank=True, null=True)
    stor_reason = UnlimitedCharField( blank=True, null=True)
    stor_date = UnlimitedCharField( blank=True, null=True)
    stor_dept = UnlimitedCharField( blank=True, null=True)
    stor_person =UnlimitedCharField( blank=True, null=True)
    stor_desc = UnlimitedCharField( blank=True, null=True)
    stor_fmts = UnlimitedCharField( blank=True, null=True)
    stor_units = UnlimitedCharField( blank=True, null=True)
    obj_name = UnlimitedCharField( blank=True, null=True)
    type_of_work = UnlimitedCharField( blank=True, null=True)
    obj_synopsis = UnlimitedCharField( blank=True, null=True)#all null?
    obj_type = UnlimitedCharField( blank=True, null=True)
    obj_sub_type = UnlimitedCharField( blank=True, null=True)
    obj_assoc_inv_nums = UnlimitedCharField( blank=True, null=True)
    obj_date = UnlimitedCharField( blank=True, null=True)#all null?
    obj_year = UnlimitedCharField( blank=True, null=True)
    obj_authors = UnlimitedCharField(blank=True, null=True)
    obj_orgs = UnlimitedCharField( blank=True, null=True)
    obj_restrict = UnlimitedCharField( blank=True, null=True)#all null?
    obj_rights = UnlimitedCharField(blank=True, null=True)# тема повторятся дважды можно вынести в отдельный столбец
    obj_rdoc_name = UnlimitedCharField( blank=True, null=True)
    obj_rdoc_num = UnlimitedCharField( blank=True, null=True)
    obj_terms = UnlimitedCharField(blank=True, null=True)
    obj_sources = UnlimitedCharField( blank=True, null=True)#all null?
    obj_supl_info = UnlimitedCharField( blank=True, null=True)#all null?
    obj_main_min = UnlimitedCharField(blank=True, null=True)
    obj_supl_min = UnlimitedCharField( blank=True, null=True)
    obj_group_min = UnlimitedCharField( blank=True, null=True)
    obj_assoc_geol = UnlimitedCharField( blank=True, null=True)
    spat_atd_ate = UnlimitedCharField( blank=True, null=True)
    spat_loc = UnlimitedCharField(blank=True, null=True)
    spat_num_grid = UnlimitedCharField( blank=True, null=True)
    spat_coords_source = UnlimitedCharField(blank=True, null=True)
    spat_toponim = UnlimitedCharField(blank=True, null=True)
    inf_type = UnlimitedCharField( blank=True, null=True)
    inf_media = UnlimitedCharField(blank=True, null=True)
    path_others = UnlimitedCharField( blank=True, null=True)#all null 
    obj_main_group = UnlimitedCharField( blank=True, null=True)
    obj_sub_group = UnlimitedCharField( blank=True, null=True)
    path_local = UnlimitedCharField( blank=True, null=True)
    path_cloud =UnlimitedCharField( blank=True, null=True)
    status = UnlimitedCharField( blank=True, null=True)#all null
    timecode = UnlimitedCharField( blank=True, null=True)#all null


    class Meta:
        managed = False
        db_table = 'uds_meta_grr_accom'