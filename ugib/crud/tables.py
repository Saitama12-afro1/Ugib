import django_tables2
from django_tables2 import tables, TemplateColumn

from .models import UdsMeta

class UdsMetaTable(tables.Table):
    acciones = TemplateColumn(template_code='<a href="/" class="btn btn-success">Ver{{record.oid}}</a>')
    test = TemplateColumn(template_name = "crud/form.html")#вставить t.html
    class Meta:
        model = UdsMeta
        template_name = "crud/index/index_htmx.html"# вынести в отдельную
        sequence = ('acciones','test', )
        