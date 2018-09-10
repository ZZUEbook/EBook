from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.template import loader
from ebookstore.models import User
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
    return render(request,template_name="ebookstore/Register.html")

def administrator(request):
    return render(request, template_name="ebookstore/Administrator.html")

def administrator_Login(request):
    return render(request, template_name="ebookstore/Administrator-Login.html")

def logout(request):
    res = render(request, template_name="ebookstore/Login.html")
    res.delete_cookie('name')
    return res