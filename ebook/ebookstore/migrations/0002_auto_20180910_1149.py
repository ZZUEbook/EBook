# Generated by Django 2.2.dev20180903084355 on 2018-09-10 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebookstore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_photo',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
