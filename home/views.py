from django.http import HttpResponse
from django.shortcuts import render
from .models import Setting
# Create your views here.




def index(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'page':'home'}
    return render(request, 'index.html',context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'hakkimizda.html',context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'referanslarimiz.html',context)


def iletisim(request):
    setting= Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'iletisim.html',context)
