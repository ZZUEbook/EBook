# Generated by Django 2.2.dev20180903084355 on 2018-09-19 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebookstore', '0006_admin_admin_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_status',
            field=models.IntegerField(default=1),
        ),
    ]
