# Generated by Django 4.1.1 on 2022-10-24 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0006_userinfo_remove_statistic_my_user_and_more'),
    ]

    operations = [
      
        migrations.AlterField(
            model_name='history',
            name='udsMeta',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='test',
            name='arr',
            field=models.CharField(default='', max_length=100),
        ),
      
    ]