# Generated by Django 4.1.2 on 2022-12-09 12:02

import crud.models
from django.db import migrations, models
import grr.models


class Migration(migrations.Migration):

    dependencies = [
        ('grr', '0003_alter_udsmetagrrstage_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='UdsMetaProtocols',
            fields=[
                ('oid', models.BigIntegerField(blank=True, default=grr.models.auto_incr_oid_apr_accom, null=True)),
                ('uniq_id', crud.models.UnlimitedCharField(primary_key=True, serialize=False)),
                ('stor_folder', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('stor_phys', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('stor_reason', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('stor_date', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('stor_dept', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('stor_person', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('stor_desc', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('stor_fmts', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('stor_units', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_name', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('type_of_work', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_synopsis', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_type', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_sub_type', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_assoc_inv_nums', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_date', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_year', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_authors', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_orgs', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_restrict', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_rights', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_rdoc_name', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_rdoc_num', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_terms', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_sources', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_supl_info', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_main_min', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_supl_min', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_group_min', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_assoc_geol', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('spat_atd_ate', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('spat_loc', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('spat_num_grid', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('spat_coords_source', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('spat_toponim', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('inf_type', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('inf_media', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('path_others', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_main_group', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('obj_sub_group', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('path_local', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('path_cloud', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('status', crud.models.UnlimitedCharField(blank=True, null=True)),
                ('timecode', crud.models.UnlimitedCharField(blank=True, null=True)),
            ],
            options={
                'db_table': 'uds_meta_protocols',
                'managed': False,
            },
        ),
    ]