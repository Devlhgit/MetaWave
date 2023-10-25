from django.shortcuts import render

# Create your views here.
# helloworld/views.py

from django.http import HttpResponse

def MainPage(request):
    return HttpResponse("MainPage")
