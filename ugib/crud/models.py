from email.policy import default
import os 
import binascii
from pyexpat import model
from statistics import mode


from django.db import models
from django.contrib.auth.models import User, AbstractUser
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


def auto_incr_oid_apr():#функция для осздания нового уникального oid
    largest = UdsMetaApr.objects.all().order_by("oid").last()
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

    
    def __str__(self) -> str:
        return (self.uniq_id)
        
    class Meta:
        db_table = 'uds_meta'


    
# class User(AbstractUser):
#     username = None
#     email = models.EmailField(
#         max_length=255,
#         unique=True,
#     )
#     
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     class Meta(AbstractUser.Meta):
#         swappable = 'AUTH_USER_MODEL'
#     class Meta:
#         db_table = "auth_user"

class UserInfo(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,        
        primary_key = True,
    )
    departament = models.CharField(max_length = 200)
    position = models.CharField(max_length = 200)
    
    class Meta: 
        db_table = "user_info"
        
# class SuperUser(models.Model):
    


class Bascet(models.Model):
    udsMeta = models.ManyToManyField(
        UdsMeta,
        related_name = "bascets",
        related_query_name = "bascet"
    )
    my_user = models.OneToOneField(
        User, 
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = "bascet"


class Order(models.Model):
    udsMeta = models.ForeignKey(
            UdsMeta, 
            on_delete = models.CASCADE
        )
    my_user = models.ManyToManyField(
            User,
            related_name = "orders",
            related_query_name = "order" 
            )
    datetimeAppend = models.DateTimeField()
    status = models.BooleanField()
    
    class Meta:
        db_table = "order"


class History(models.Model):
    date = models.DateField()
    typeAction = models.CharField(max_length = 100)
    
    my_user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "histories"
    )
    udsMeta = models.TextField()
    order = models.BooleanField()
    fond = models.CharField(max_length=50, default="01found")
    
    class Meta:
        db_table = 'history'

    def __str__(self) -> str:
        return str(self.my_user)


class Test(models.Model):
    arr = models.CharField(max_length = 100, default = "")
    class Meta:
        db_table = "test"

        
class UdsMetaApr(models.Model):
    oid = models.BigIntegerField(default=auto_incr_oid_apr, null = True, blank = True)
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
        db_table = 'uds_meta_apr'