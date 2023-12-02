from urllib import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from product.models import Comment, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def index():
    return HttpResponse("Product Page")

@login_required(login_url='/login') #check login
def addcomment(request,id):
    url = request.META.get('HTTP_REFERER') #get last url
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user=request.user

            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR') #client computer ip adress
            data.save()
            messages.success(request, "yorumunuz başarı ile gönderilmiştir")  
                    
            return HttpResponseRedirect(url)
    messages.error(request, "yorum kaydedilmedi")    
    return HttpResponseRedirect(url)    