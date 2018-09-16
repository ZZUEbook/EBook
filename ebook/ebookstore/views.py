from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.template import loader, Context
from ebookstore.models import User, Book, Notice, BookType
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

def administrator(request):
    return render(request, template_name="ebookstore/Administrator.html")

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
    return render(request, template_name='ebookstore/Administrator-Login.html')

def newBook(request):
    if request.method == "GET":
        books = Book.objects.all().order_by("-book_id")[0:5]
        items = []
        for book in books:
            items.append({"id": book.book_id, "name": book.book_name,"url":book.book_photo})
        return HttpResponse(content=json.dumps(items))