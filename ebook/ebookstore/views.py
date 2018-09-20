from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.template import loader, Context
from django.db.models import Q, QuerySet
from ebookstore.models import User, Book, Notice, BookType, Admin, Comment, Order, Order_item
import json, socket, time
from PIL import Image
from itertools import chain

# Create your views here.
def index(request):
    name = request.COOKIES.get('name')
    if not name:
        return render(request, "ebookstore/index.html")
    return render(request, "ebookstore/index.html",context={'name':name})

def login(request):
    name = request.COOKIES.get('name')
    if name:
        return render(request,'ebookstore/index.html',context={'name':name})
    if request.method == "POST":
        user = User.objects.filter(user_name=request.POST['name']).first()
        if user.user_password == request.POST['password']:
            if user.user_status == -1:
                return HttpResponse(-1)
            res = HttpResponse(1)
            res.set_cookie('name', value=user.user_name)
            return res
        else:
            return HttpResponse(0)
        print(request.POST)

    return render(request, template_name="ebookstore/Login.html")

def register(request):
    if request.method == "POST":
        print(request.POST)
        if len(User.objects.filter(user_name=request.POST['name'])) > 0:
            return HttpResponse(0)
        else:
            user = User(user_name=request.POST['name'],
                        user_password=request.POST['password'],
                        user_email=request.POST['mail'],
                        user_address=request.POST['address'],
                        user_phone=request.POST['telephone'])
            try:
                user.save()
                res = HttpResponse(1)
                res.set_cookie('name', value=request.POST['name'])
                return res
            except Exception as e:
                print(e)
                return HttpResponse(-1)
    else:
        return render(request,template_name="ebookstore/Register.html")

def book_manage(request):
    return render(request, template_name="ebookstore/Book-manage.html")

def logout(request):
    res = render(request, template_name="ebookstore/Login.html")
    res.delete_cookie('name')
    return res

def getbook(request):
    if request.method == "GET":
        subject = request.GET.get('subject', '')
        if subject:
            print("para")
            data = []
            booktype = BookType.objects.filter(booktype_name=subject).first()
            booktype = booktype.booktype_id
            books = Book.objects.filter(book_type_id=booktype)
            for book in books:
                data.append({"id": book.book_id, "url": book.book_photo, "name": book.book_name})
            return HttpResponse(json.dumps(data))
        else:
            print('no para')
            books = Book.objects.all()
            data = []
            for book in books:
                data.append({"id": book.book_id, "url": book.book_photo, "name": book.book_name})
            return HttpResponse(json.dumps(data))
def getNotice(request):
    if request.method == "GET":
        notices = Notice.objects.filter(notice_status=1)
        data = []
        for notice in notices:
            try:
                admin = notice.notice_admin_id
                data.append({"time": str(notice.notice_time), "content": notice.notice_content
                                 , "id": str(notice.notice_id), "author": admin.admin_name})
            except Exception as err:
                print(err)
        return HttpResponse(json.dumps(data))

def getRankList(request):
    if request.method == "GET":
        if request.GET['subject'] == "english":
            books = Book.objects.filter(book_type_id=2).order_by("-book_sale_number")[0:10]
        elif request.GET['subject'] == "computer":
            books = Book.objects.filter(book_type_id=1).order_by("-book_sale_number")[0:10]
        else:
            books = Book.objects.all().order_by("-book_sale_number")[0:10]
        items = []
        for book in books:
            items.append({"id": book.book_id, "name": book.book_name})

        return HttpResponse(content=json.dumps(items))

def myinfo(request):
    
    name = request.COOKIES.get('name')
    if request.method =="GET":
        if not name:
            render(request,template_name="ebookstore/Register.html")
        else:
            user = User.objects.filter(user_name=name).first()
            context = {
                "name":name,
                "phone":user.user_phone,
                "address":user.user_address,
                "password":user.user_password
            }
            return render(request,template_name="ebookstore/MyInoformation.html",context=context)
    elif request.method =="POST" :
        if not name:
            render(request,template_name="ebookstore/Register.html")
        else:
            user = User.objects.filter(user_name=name).first()
            user.user_address = request.POST['address']
            user.user_password = request.POST['password']
            user.save()
            return HttpResponse(1)
    else:
        return HttpResponse(1)

def adminLogin(request):
    if request.method == "POST":
        try:
            name = request.POST["name"]
            password = request.POST["password"]
            admin = Admin.objects.filter(admin_name=name).first()
            if password == admin.admin_password:
                print("debug0", admin.admin_status)
                if admin.admin_status != 0:
                    return HttpResponse(-1)
                res = HttpResponse(1)
                res.set_cookie("admin_name", name)
                return res
            else:
                return HttpResponse(0)
        except Exception as err:
            print(err)
            return 0
    return render(request, template_name='ebookstore/Administrator-Login.html')

def newBook(request):
    if request.method == "GET":
        books = Book.objects.all().order_by("-book_id")[0:5]
        items = []
        for book in books:
            items.append({"id": book.book_id, "name": book.book_name,"url":book.book_photo})
        return HttpResponse(content=json.dumps(items))

def book_detail(request):
    id = request.GET.get('id', 0)
    book = Book.objects.filter(book_id=id).first()
    if not book:
        return HttpResponse("are you a robot?")
    context = {
        "book_id": id,
        "book_name": book.book_name,
        "book_press": book.book_press,
        "book_auth_name": book.book_auth_name,
        "book_price": book.book_price,
        "book_publish_date": book.book_publish_date,
        "book_info": book.book_introduce,
        "book_left_number": book.book_left_number,
        "book_photo_url": book.book_photo,
        "book_ISBN": book.book_ISBN,
    }
    return render(request, 'ebookstore/BookDetail.html', context)

def base(request):
    return render(request, 'ebookstore/base.html')

def test(request):
    return render(request, 'ebookstore/test.html')

def book_manage(request):
    if request.method == "GET":
        books = Book.objects.all().order_by("-book_id")
        content = []
        for book in books:
            dic = {}
            dic["id"]=book.book_id
            dic["isbn"] = book.book_ISBN
            dic["name"] = book.book_name
            dic["press"] = book.book_press
            dic["author"] = book.book_auth_name
            dic["count"] = book.book_left_number
            content.append(dic)
        return HttpResponse(content)
def BookManageHTML(request):
    return render(request, 'ebookstore/Book-manage.html')
def UserManage(request):
    return render(request, 'ebookstore/user-manage.html')
def OrderManage(request):
    return render(request, 'ebookstore/order-manage.html')
def NoticeManage(request):
    return render(request, 'ebookstore/Notice-manage.html')
def AccountManage(request):
    return render(request, 'ebookstore/account-manage.html')
def ConmentManage(request):
    return render(request, 'ebookstore/comment-manage.html')
def manage_base(request):
    return render(request, 'ebookstore/manage_base.html')
def add_book(request):
    # print(request.FILES)
    if request.method == 'POST':
        try:
            name = request.POST['name']
            isbn = request.POST['isbn']
            author = request.POST['author']
            press = request.POST['press']
            time = request.POST['timeOfPress']
            (month, day, year) = time.split('/')
            time = year + '-' + month + '-' + day
            category = request.POST['category']
            category = 'English' if category == r"英语类" else 'Computer'
            category = BookType.objects.filter(booktype_name=category).first()
            quantity = request.POST['quantity']
            price = request.POST['price']
            cost = request.POST['cost']
            cover = request.FILES['cover']
            introduce = request.POST['introduce']
            url = '/static/ebookstore/img/计算机类/default.jpg'
            admin = Admin.objects.filter(admin_id=1).first()
            if cover:
                img_name = name
                img = Image.open(cover)
                img_type = str(cover).split('.')[-1]
                url = img_name + '.' + img_type
                url = '/static/ebookstore/img/' + request.POST['category'] + '/' + url
                img.save('ebookstore' + url)
            book = Book(book_ISBN=isbn, book_name=name, book_auth_name=author, book_publish_date=time,
                        book_publisher=admin, book_type_id=category, book_introduce=introduce, book_price=price,
                        book_photo=url, book_left_number=quantity, book_cost=cost, book_press=press)
            book.save()
        except Exception as err:
            print(err)
    return render(request, 'ebookstore/AddBook.html')
def order_content(request):
    return render(request, 'ebookstore/OrderContent.html')
def cart(request):
    return render(request, 'ebookstore/Cart.html')
def order(request):
    return render(request, 'ebookstore/order.html')
def deleteNotice(request):
    # print(request.POST)
    if request.method == "POST":
        id = request.POST['id']
        try:
            notice = Notice.objects.filter(notice_id=id).first()
            notice.notice_status = 0
            notice.save()
            return HttpResponse(1)
        except Exception as err:
            return HttpResponse(0)
def addNotice(request):
    print(request.POST)
    if request.method == "POST":
        author = request.POST['author']
        content = request.POST['content']
        try:
            admin = Admin.objects.filter(admin_name=author).first()
            timeTuple = time.localtime()
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", timeTuple)
            notice = Notice(notice_admin_id=admin, notice_content=content, notice_time=time_str)
            notice.save()
            data = {}
            data["time"] = time_str
            data["id"] = notice.notice_id
            return HttpResponse(json.dumps(data))
        except Exception as err:
            return HttpResponse(0)
def queryBook(request):
    try:
        key = request.GET.get('key', '')
        data = []
        if key:
            books = Book.objects.filter(Q(book_name=key))
        else:
            books = Book.objects.all()
        for book in books:
            data.append({"id": book.book_id, "isbn":book.book_ISBN, "author": book.book_auth_name,
                        "count": book.book_left_number, "press": book.book_press, "name": book.book_name})
        return HttpResponse(json.dumps(data))
    except Exception as err:
        print(0)
        return HttpResponse(0)
def modifyBook(request):

    id = request.GET.get("id", '1')
    book = Book.objects.filter(book_id=id).first()
    book_type = book.book_type_id
    type = book_type.booktype_name
    # print(book.book_publish_date, type)
    context = {"name": book.book_name,
               "isbn": book.book_ISBN,
               "author": book.book_auth_name,
               "press": book.book_press,
               "date": str(book.book_publish_date),
               "type":type,
               "count": book.book_left_number,
               "price": book.book_price,
               "cost": book.book_cost,
               "introduce": book.book_introduce,
               }
    return render(request, 'ebookstore/ModifyBook.html', context)
def queryUser(request):
    key = request.GET.get('key', '')
    data = []
    if key:
        users = User.objects.filter(Q(user_name=key))
    else:
        users = User.objects.all()
    data = []
    for user in users:
        data.append(
            {"id": user.user_id, "name": user.user_name, "phone": user.user_phone, "freeze": user.user_status})
    return HttpResponse(json.dumps(data))

def queryComment(request):
    key = request.GET.get("key", '')
    if key:
        user = User.objects.filter(user_name=key).first()
        book = Book.objects.filter(book_name=key).first()
        query_set1 = Comment.objects.filter(comment_book=book)
        query_set2 = Comment.objects.filter(comment_user=user)
        comments = chain(query_set1, query_set2)
    else:
        comments = Comment.objects.filter(comment_status=1)
    data = []
    for comment in comments:
        book = comment.comment_book
        user = comment.comment_user
        data.append({"id": comment.comment_id, "name": book.book_name, "author": user.user_name,
                     "content": comment.comment_content, "time": str(comment.comment_time)})
    return HttpResponse(json.dumps(data))
def deleteComment(request):
    if request.method == "POST":
        id = request.POST['id']
        comment = Comment.objects.filter(comment_id=id).first()
        comment.comment_status = -1
        comment.save()
def changeUserFreezeState(request):
    if request.method == "POST":
        try:
            id = request.POST['id']
            status = request.POST['state']
            user = User.objects.filter(user_id=id).first()
            user.user_status = status
            user.save()
            return HttpResponse(1)
        except Exception as err:
            return HttpResponse(0)
def queryOrder(request):
    key = request.GET.get('key', '')
    data = []
    if key:
        user = User.objects.get(Q(user_name__contains=key) | Q(user_phone__contains=key))
        orders = Order.objects.filter(Q(order_user_id=user), ~Q(order_status=0))
    else:
        orders = Order.objects.filter(~Q(order_status=0))
    for order in orders:
        user = order.order_user_id
        # state=>1：未支付，2：未发货(提交了)，3：已发货，4：关闭，5：已完成
        data.append({"id": order.order_id, "phone": user.user_phone, "name": user.user_name,
                     "state": order.order_status})
    return HttpResponse(json.dumps(data))
def deleteOrder(request):
    if request.method == "POST":
        try:
            id = request.POST['id']
            order = Order.objects.filter(order_id=id).first()
            order.order_status = 0
            order.save()
            return HttpResponse(1)
        except Exception as err:
            return HttpResponse(0)
def deliverGoods(request):
    if request.method == "POST":
        try:
            id = request.POST['id']
            order = Order.objects.filter(order_id=id).first()
            order.order_status = 3
            order.save()
            return HttpResponse(1)
        except Exception as err:
            return HttpResponse(0)
        # queryAccount: get
        # [{"isbn": "", "name": "", "press": "", "author": "", "cost":, "price":, "quantity":}, ...]
# def accountManage(request):
#     if request.method == "GET":
#         start = request.get('start', '')
#         end = request.GET('end', '')
#         data = []
#         if start and end:
#             (month, day, year) = start.split('/')
#             start = year + '-' + month + '-' + day
#             (month, day, year) = end.split('/')
#             end = year + '-' + month + '-' + day
#             orders = Order.objects.filter(order_complete_time__range=(start, end))
#             for order in orders:
#                 order_items = Order_item.objects.filter(order_id=order)
#                 for item in order_items:
#                     book = Book.objects.filter(book_id=item.book_id).first()
#
#         else:
#             books = Book.objects.all()
#             for book in books:
#                 data.append({"isbn": book.book_ISBN, "name": book.book_name, "press": book.book_press,
#                              "author": book.book_auth_name, "cost": book.book_cost, "price": book.book_price,
#                              "quantity": book.book_sale_number})
#         return HttpResponse(json.dumps(data))



