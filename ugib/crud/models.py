from email.policy import default
import os 
import binascii


from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class UnlimitedCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        # for Django >= 3.2
        self.db_collation = kwargs.pop("db_collation", None)

        # not a typo: we want to skip CharField.__init__ because that adds the max_length validator
        super(models.CharField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        # likewise, want to skip CharField.__check__
        return super(models.CharField, self).check(**kwargs)

    def db_type(self, connection):
        return "varchar"
 
 
def auto_incr_oid():#функция для осздания нового уникального oid
    largest = UdsMeta.objects.all().order_by("oid").last()
    return largest.oid + 1


def autho_incr_uniq_id() -> str:# функция для создания нового уникального ключа
    while True:
        a = str(binascii.hexlify(os.urandom(10)).decode())
        try:
            UdsMeta.objects.get(uniq_id = a)
        except ObjectDoesNotExist:
            return a
            
 
    
        
class UdsMeta(models.Model):
    oid = models.BigIntegerField(default=auto_incr_oid, null = True, blank = True)
    uniq_id = UnlimitedCharField(primary_key = True)
    stor_folder = UnlimitedCharField( blank=True, null=True)
    stor_phys = UnlimitedCharField( blank=True, null=True)
    stor_reason = UnlimitedCharField( blank=True, null=True)
    stor_date = UnlimitedCharField( blank=True, null=True)
    stor_dept = UnlimitedCharField( blank=True, null=True)
    stor_person = UnlimitedCharField( blank=True, null=True)
    stor_desc = UnlimitedCharField( blank=True, null=True)
    stor_fmts = UnlimitedCharField( blank=True, null=True)
    stor_units = UnlimitedCharField( blank=True, null=True)
    obj_name = UnlimitedCharField( blank=True, null=True)
    type_of_work = UnlimitedCharField( blank=True, null=True)
    obj_synopsis = UnlimitedCharField( blank=True, null=True)#all null? Yes
    obj_type = UnlimitedCharField( blank=True, null=True)
    obj_sub_type = UnlimitedCharField( blank=True, null=True)
    obj_assoc_inv_nums = UnlimitedCharField( blank=True, null=True)
    obj_date = UnlimitedCharField( blank=True, null=True)#all null?
    obj_year = UnlimitedCharField( blank=True, null=True)
    obj_authors = UnlimitedCharField( blank=True, null=True)
    obj_orgs = UnlimitedCharField( blank=True, null=True)
    obj_restrict = UnlimitedCharField( blank=True, null=True)#all null?
    obj_rights = UnlimitedCharField( blank=True, null=True)
    obj_rdoc_name = UnlimitedCharField( blank=True, null=True)# тема повторятся дважды можно вынести в отдельный столбец
    obj_rdoc_num = UnlimitedCharField( blank=True, null=True)
    obj_terms = UnlimitedCharField( blank=True, null=True)
    obj_sources = UnlimitedCharField( blank=True, null=True)#all null?
    obj_supl_info = UnlimitedCharField( blank=True, null=True)#all null?
    obj_main_min = UnlimitedCharField( blank=True, null=True)
    obj_supl_min = UnlimitedCharField( blank=True, null=True)
    obj_group_min = UnlimitedCharField( blank=True, null=True)
    obj_assoc_geol = UnlimitedCharField( blank=True, null=True)
    spat_atd_ate = UnlimitedCharField( blank=True, null=True)
    spat_loc = UnlimitedCharField( blank=True, null=True)
    spat_num_grid = UnlimitedCharField( blank=True, null=True)
    spat_coords_source = UnlimitedCharField( blank=True, null=True)
    spat_toponim = UnlimitedCharField( blank=True, null=True)
    inf_type = UnlimitedCharField( blank=True, null=True)
    inf_media = UnlimitedCharField( blank=True, null=True)
    path_others = UnlimitedCharField( blank=True, null=True)#all null 
    obj_main_group = UnlimitedCharField(blank=True, null=True)
    obj_sub_group = UnlimitedCharField( blank=True, null=True)
    path_local = UnlimitedCharField( blank=True, null=True)
    path_cloud = UnlimitedCharField( blank=True, null=True)
    status = UnlimitedCharField( blank=True, null=True)#all null
    timecode = UnlimitedCharField( blank=True, null=True)#all null
    obj_sub_group_ref = UnlimitedCharField( blank=True, null=True)
    path_local_ref = UnlimitedCharField( blank=True, null=True)
    path_cloud_ref = UnlimitedCharField( blank=True, null=True)     
        
    class Meta:
        managed = False
        db_table = 'uds_meta'






# class UdsMetaApr(models.Model):
#     oid = models.BigAutoField(primary_key=True)
#     uniq_id = models.UnlimitedCharField(=100)
#     stor_folder = models.UnlimitedCharField(=50, blank=True, null=True)
#     stor_phys = models.UnlimitedCharField(=50, blank=True, null=True)
#     stor_reason = models.UnlimitedCharField(=300, blank=True, null=True)
#     stor_date = models.UnlimitedCharField(=10, blank=True, null=True)
#     stor_dept = models.UnlimitedCharField(=30, blank=True, null=True)
#     stor_person = models.UnlimitedCharField(=100, blank=True, null=True)
#     stor_desc = models.UnlimitedCharField(=100, blank=True, null=True)
#     stor_fmts = models.UnlimitedCharField(=50, blank=True, null=True)
#     stor_units = models.UnlimitedCharField(=50, blank=True, null=True)
#     obj_name = models.UnlimitedCharField(=300, blank=True, null=True)
#     type_of_work = models.UnlimitedCharField(=50, blank=True, null=True)
#     obj_synopsis = models.UnlimitedCharField(=100, blank=True, null=True)#all null?
#     obj_type = models.UnlimitedCharField(=50, blank=True, null=True)
#     obj_sub_type = models.UnlimitedCharField(=50, blank=True, null=True)
#     obj_assoc_inv_nums = models.UnlimitedCharField(=150, blank=True, null=True)
#     obj_date = models.UnlimitedCharField(=100, blank=True, null=True)#all null?
#     obj_year = models.UnlimitedCharField(=5, blank=True, null=True)
#     obj_authors = models.UnlimitedCharField(=100, blank=True, null=True)
#     obj_orgs = models.UnlimitedCharField(=150, blank=True, null=True)
#     obj_restrict = models.UnlimitedCharField(=100, blank=True, null=True)#all null?
#     obj_rights = models.UnlimitedCharField(=100, blank=True, null=True)# тема повторятся дважды можно вынести в отдельный столбец
#     obj_rdoc_name = models.UnlimitedCharField(=300, blank=True, null=True)
#     obj_rdoc_num = models.UnlimitedCharField(=300, blank=True, null=True)
#     obj_terms = models.UnlimitedCharField(=1000, blank=True, null=True)
#     obj_sources = models.UnlimitedCharField(=100, blank=True, null=True)#all null?
#     obj_supl_info = models.UnlimitedCharField(=100, blank=True, null=True)#all null?
#     obj_main_min = models.UnlimitedCharField(=200, blank=True, null=True)
#     obj_supl_min = models.UnlimitedCharField(=50, blank=True, null=True)
#     obj_group_min = models.UnlimitedCharField(=100, blank=True, null=True)
#     obj_assoc_geol = models.UnlimitedCharField(=1000, blank=True, null=True)
#     spat_atd_ate = models.UnlimitedCharField(=200, blank=True, null=True)
#     spat_loc = models.UnlimitedCharField(=200, blank=True, null=True)
#     spat_num_grid = models.UnlimitedCharField(=500, blank=True, null=True)
#     spat_coords_source = models.UnlimitedCharField(=100, blank=True, null=True)
#     spat_toponim = models.UnlimitedCharField(=100, blank=True, null=True)
#     inf_type = models.UnlimitedCharField(=100, blank=True, null=True)
#     inf_media = models.UnlimitedCharField(=100, blank=True, null=True)
#     path_others = models.UnlimitedCharField(=100, blank=True, null=True)#all null 
#     obj_main_group = models.UnlimitedCharField(=50, blank=True, null=True)
#     obj_sub_group = models.UnlimitedCharField(=100, blank=True, null=True)
#     path_local = models.UnlimitedCharField(=200, blank=True, null=True)
#     path_cloud = models.UnlimitedCharField(=1000, blank=True, null=True)
#     status = models.UnlimitedCharField(=100, blank=True, null=True)#all null
#     timecode = models.UnlimitedCharField(=100, blank=True, null=True)#all null

#     class Meta:
#         managed = False
#         db_table = 'uds_meta_apr'