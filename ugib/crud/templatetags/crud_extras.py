from django import template

register = template.Library()

all_columns = {'oid':'Номер','uniq_id':'Уникальный номер','stor_folder':'Папка хранения', 'stor_phys':'Физическое место хранения вещественного носителя', 
        'stor_reason':'Причина передачи', 'stor_date':'Дата передачи', 'stor_dept':'Подразделение, внесшее информацию', 'stor_person' :'Составитель', 
        'stor_desc':'Дополнительные сведения', 'stor_fmts':'Тип файлов', 'stor_units':'Единицы хранения документа', 'obj_name':'Название объекта', 'type_of_work':'Вид работ', 
        'obj_synopsis':'Синопсис', 'obj_type':'Вид объекта учета', 'obj_sub_type':'Условное название каталога учета', 'obj_assoc_inv_nums':'Инвентарные номера в каталогах учета',
        'obj_date':'Дата составления объекта учета', 'obj_year':'Год составления объекта учета', 'obj_authors':'Автор (авторы)', 'obj_orgs':'Организация', 
        'obj_restrict':'Сведения о наличии ограничений оборота передаваемых данных', 'obj_rights' :'Права на материалы объекта', 
        'obj_rdoc_name':'Наименование регламентирующего документа', 'obj_rdoc_num':'Номер регламентирующего документа', 'obj_terms':'Ключевые слова',
        'obj_sources':'Сведения об источниках и материалах', 'obj_supl_info':'Иные дополнительные сведения', 
        'obj_main_min':'Полезные ископаемые основные', 'obj_supl_min':'Полезные ископаемые попутные', 'obj_group_min':'Группа полезных ископаемых', 
        'obj_assoc_geol':'Геологические объекты', 'spat_atd_ate':'Сведения о привязке в рамках АТД и АТЕ', 'spat_loc':'Местоположение', 
        'spat_num_grid':'Номенклатуры листов НД', 'spat_coords_source':'Координаты контура материалов', 'spat_toponim':'Дополнительные сведения о местоположении',
        'inf_type':'Тип информации', 'inf_media':'Вид носителя информации', 'path_others':'Государственная регистрация', 'obj_main_group':'Формула', 
        'obj_sub_group':'obj_sub_group', 'path_local':'path_local', 'path_cloud':'path_cloud', 'status':'Cтатус', 'timecode':'Дата изменения', 
        'obj_sub_group_ref':'obj_sub_group_ref', 'path_local_ref':'path_local_ref', 'path_cloud_ref':'path_cloud_ref', 'delete':'Удалить','Exel':'Exel', 
        'update':'Изменить','Bascet':'В корзину'}

@register.filter
def addstr(arg1):#задает название класса  html в нужном формате 
    arg1 = str(arg1)
    new_attr = arg1.replace(" ", "_")
    new_attr = new_attr.lower()
    return str(new_attr)


@register.filter
def inizial(arg1):#создает иницалы для отобрадения в html
    iniz = arg1.split(" ")
    if len(iniz) <= 1:
        return arg1
    iniz = iniz[0][0] + "." + iniz[1][0] + "."
    return(str(iniz))

@register.filter
def translate_column_name(column):#переврдит названия 
    try:
        return all_columns[column]
    except KeyError:
        return column

@register.filter
def replace_none_on_str(cell):
    if cell == None:
        return ''
    return cell

@register.simple_tag
def create_href_for_history(uniq_id, fond):
    if fond == "01found":
        return f"http://gis311k1:8000/?query={uniq_id}"
    return f"http://gis311k1:8000/{fond}/?query={uniq_id}"


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()