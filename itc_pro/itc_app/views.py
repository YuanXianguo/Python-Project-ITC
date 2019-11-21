from django.shortcuts import render
from django.http import HttpResponse
from itc_app.models import TestResults
# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')


def index(request):
    if request.method == "GET":
        return render(request, 'index.html')


def work_pos_list(request):
    if request.method == "GET":
        return render(request, 'work_pos_list.html')

def test(request):
    return HttpResponse(TestResults.objects.using("itc").all())
