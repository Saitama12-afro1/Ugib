# Generated by Django 4.1.1 on 2022-10-24 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0007_remove_statistic_my_user_remove_statistic_udsmeta_and_more'),
    ]

    operations = [


        migrations.RenameField(
            model_name='userinfo',
            old_name='user_id',
            new_name='user',
        ),

    ]
