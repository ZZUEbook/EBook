# Generated by Django 2.2.dev20180903084355 on 2018-09-16 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebookstore', '0005_auto_20180914_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='admin_status',
            field=models.IntegerField(default=0),
        ),
    ]
