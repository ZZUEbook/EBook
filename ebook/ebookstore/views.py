from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, template_name="ebookstore/index.html")

def login(request):
    return render(request, template_name="ebookstore/Login.html")

def register(request):
    return render(request,template_name="ebookstore/Register.html")

def administrator(request):
    return render(request, template_name="ebookstore/Administrator.html")

def administrator_Login(request):
    return render(request, template_name="ebookstore/Administrator-Login.html")