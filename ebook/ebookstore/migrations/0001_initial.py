# Generated by Django 2.2.dev20180903084355 on 2018-09-06 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('admin_name', models.CharField(max_length=50)),
                ('admin_password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_ISBN', models.CharField(max_length=20)),
                ('book_name', models.CharField(max_length=100)),
                ('book_auth_name', models.CharField(max_length=50)),
                ('book_publish_date', models.DateField()),
                ('book_introduce', models.CharField(blank=True, max_length=300)),
                ('book_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('book_photo', models.ImageField(blank=True, upload_to='')),
                ('book_left_number', models.IntegerField()),
                ('book_sale_number', models.IntegerField(default=0)),
                ('book_cost', models.IntegerField(blank=True)),
                ('book_publisher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.Admin')),
            ],
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('booktype_id', models.AutoField(primary_key=True, serialize=False)),
                ('booktype_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('cart_price', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_create_time', models.DateTimeField()),
                ('order_complete_time', models.DateTimeField()),
                ('order_status', models.IntegerField(default=0)),
                ('order_receiver_phone', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('user_email', models.CharField(max_length=50, unique=True)),
                ('user_phone', models.IntegerField(unique=True)),
                ('user_password', models.CharField(max_length=30)),
                ('user_status', models.IntegerField(default=0)),
                ('user_address', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order_item',
            fields=[
                ('order_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_count', models.IntegerField(default=1)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.Book')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.Order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.User'),
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('notice_id', models.AutoField(primary_key=True, serialize=False)),
                ('notice_content', models.CharField(max_length=800)),
                ('notice_time', models.DateTimeField()),
                ('notice_admin_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.Admin')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_content', models.CharField(max_length=300)),
                ('comment_time', models.DateTimeField()),
                ('comment_book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.Book')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.User')),
            ],
        ),
        migrations.CreateModel(
            name='Cart_item',
            fields=[
                ('cart_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('cart_item_status', models.IntegerField(default=1)),
                ('book_count', models.IntegerField(default=1)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.Book')),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.Cart')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.User'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ebookstore.BookType'),
        ),
    ]
