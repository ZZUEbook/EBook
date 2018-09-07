from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from ebookstore.models import User
import json, socket

# Create your views here.
def index(request):
    return render(request, template_name="ebookstore/index.html")

def login(request):
    print(request.POST)
    if request.method == "POST":
        data = {'url': '', 'res': '0',}
        user = User.objects.filter(user_name=request.POST['name']).first()
        print(user.user_password, user.user_password == request.POST['password'])
        if user.user_password == request.POST['password']:
            data['res'] = 1
            data['url'] = 'index/'
        if user.user_status == -1:
            data['res'] = -1
        return HttpResponse(json.dumps(data), content_type='application/json')
    return render(request, template_name="ebookstore/Login.html")

def register(request):
    return render(request,template_name="ebookstore/Register.html")

def administrator(request):
    return render(request, template_name="ebookstore/Administrator.html")

def administrator_Login(request):
    return render(request, template_name="ebookstore/Administrator-Login.html")