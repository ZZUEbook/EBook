from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.template import loader, Context
from ebookstore.models import User, Book, Notice, BookType, Admin
import json, socket

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

def administrator_Login(request):
    return render(request, template_name="ebookstore/Administrator-Login.html")

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
            data.append({"time": str(notice.notice_time), "content":notice.notice_content})
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
                if admin.admin_status != 0:
                    return -1
                return 1
            else:
                return 0
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

def admin(request):
    return render(request, 'ebookstore/Book-manage.html')

def addBook(request):
    return render(request, 'ebookstore/AddBook.html')
def UserManage(request):
    return render(request, 'ebookstore/user-manage.html')
def OrderManage(request):
    return render(request, 'ebookstore/OrderDetail.html')
def NoticeManage(request):
    return render(request, 'ebookstore/Notice-manage.html')
def AccountManage(request):
    return render(request, 'ebookstore/account-manage.html')
