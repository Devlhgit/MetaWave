from django.shortcuts import render


def mainPage(request):
    return render(request, "mainPage.html")


def information(request):
    return render(request, "information.html")
