from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, template_name="ebookstore/Login.html")
