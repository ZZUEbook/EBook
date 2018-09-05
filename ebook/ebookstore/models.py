from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30, unique=True)  # null=True, blank=True
    user_phone = models.IntegerField(unique=True)
    user_password = models.CharField(max_length=30)
    user_status = models.IntegerField(default=0)  # 0=>normal user
    user_address = models.CharField(max_length=100, blank=True)


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=50)
    admin_password = models.CharField(max_length=30)


class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    notice_content = models.CharField(max_length=800)
    notice_admin_id = models.ForeignKey(Admin, on_delete=models.DO_NOTHING)
    notice_time = models.DateTimeField()


class BookType(models.Model):
    booktype_id = models.AutoField(primary_key=True)
    booktype_name = models.CharField(max_length=10)


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_ISBN = models.CharField(max_length=20)
    book_name = models.CharField(max_length=100)
    book_auth_name = models.CharField(max_length=50)
    book_publish_date = models.DateField()
    book_publisher = models.ForeignKey(Admin, on_delete=models.DO_NOTHING)
    book_type_id = models.ForeignKey(BookType, models.DO_NOTHING)
    book_introduce = models.CharField(max_length=300, blank=True)
    book_price = models.DecimalField(max_digits=20, decimal_places=2)
    book_photo = models.ImageField(blank=True)
    book_left_number = models.IntegerField()
    book_sale_number = models.IntegerField(default=0)
    book_cost = models.IntegerField(blank=True)


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    cart_user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    cart_price = models.DecimalField(max_digits=20, decimal_places=2)


class Cart_item(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart_item_status = models.IntegerField(default=1)  # 0 no select, 1 yes
    cart_id = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    book_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    book_count = models.IntegerField(default=1)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_content = models.CharField(max_length=300)
    comment_time = models.DateTimeField()
    comment_book = models.ForeignKey(Book, models.DO_NOTHING)
    comment_user = models.ForeignKey(User, models.DO_NOTHING)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_create_time = models.DateTimeField()
    order_complete_time = models.DateTimeField()
    order_status = models.IntegerField(default=0)  # 0 haven't pay, -1 delete, 1 already pay
    order_user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order_receiver_phone = models.CharField(max_length=13)


class Order_item(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    book_count = models.IntegerField(default=1)


# notice cart_item order_item order cart comment book booktype admin user