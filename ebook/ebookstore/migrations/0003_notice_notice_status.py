# Generated by Django 2.2.dev20180903084355 on 2018-09-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebookstore', '0002_auto_20180910_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='notice_status',
            field=models.IntegerField(default=1),
        ),
    ]
