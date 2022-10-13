import re

from django.db.models import QuerySet

from .models import UdsMeta


class HelperUdsMet:
    _all_columns = ['oid','uniq_id','stor_folder', 'stor_phys', 
        'stor_reason', 'stor_date', 'stor_dept', 'stor_person', 'stor_desc', 
        'stor_fmts', 'stor_units', 'obj_name', 'type_of_work', 'obj_synopsis', 'obj_type', 
        'obj_sub_type', 'obj_assoc_inv_nums', 'obj_date', 'obj_year', 'obj_authors', 'obj_orgs', 
        'obj_restrict', 'obj_rights', 'obj_rdoc_name', 'obj_rdoc_num', 'obj_terms', 'obj_sources', 'obj_supl_info', 
        'obj_main_min', 'obj_supl_min', 'obj_group_min', 'obj_assoc_geol', 'spat_atd_ate', 'spat_loc', 'spat_num_grid', 
        'spat_coords_source', 'spat_toponim', 'inf_type', 'inf_media', 'path_others', 'obj_main_group', 'obj_sub_group', 'path_local', 
        'path_cloud', 'status', 'timecode', 'obj_sub_group_ref', 'path_local_ref', 'path_cloud_ref']
    
    
    
    @classmethod
    def create_dict_from_query_set(cls, obj:QuerySet) -> dict:
        dict_query_set = {}
        for i in HelperUdsMet._all_columns:
            dict_query_set[i] = obj[i]
        return dict_query_set
    
    
    @classmethod
    def create_dict_from_query_set_without_oid(cls, obj:QuerySet) -> dict:
        dict_query_set = {}
        for i in HelperUdsMet._all_columns[1:]:
            dict_query_set[i] = obj[i]
        return dict_query_set
    
    @classmethod
    def credte_dict_from_js_dict(cls, js_dict:dict) -> dict:
 
        d = {}
        for i in js_dict:
            if i != "csrfmiddlewaretoken" and i != "create" and i != "update" and  i != 'data[csrfmiddlewaretoken]':
                d[i[5:len(i)-1]] = js_dict[i]
        return d
        
            
            
    
    
    
    


