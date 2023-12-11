import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect

from eticaret.forms import SearchForm, SignUpForm
#üstteki e ticaret yerine home.forms dene
# Create your views here.
from home.models import Setting, ContactFormMessage, ContactForm, UserProfile
from django.db.models import Count 
from django.contrib import messages
from product.models import Images, Product, Category, Comment
from django.contrib.auth import logout, authenticate, login
from order.models import ShopCart
from django.core.mail import send_mail
from django.http import JsonResponse
from home.forms import FileUploadForm


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category = Category.objects.all()
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproduct = Product.objects.all().order_by('?')[:4]
    
    # count fonksiyonunu çağırmak için parantez kullanılmalı
    cart_items_count = ShopCart.objects.filter(user_id=current_user.id).count()
    
    # request.session['cart_items'] değişkenine değeri atayın
    request.session['cart_items'] = cart_items_count
    

    context = {'setting': setting,
               'category' : category,
               'page':'home',
               'dayproducts':dayproducts,
               'sliderdata':sliderdata,
               'randomproducts':randomproduct,
               'lastproducts': lastproducts
               }   
    return render(request, 'index.html',context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'referanslarimiz.html',context)


def iletisim(request): #formu kaydetme
    category = Category.objects.all()
    if request.method == 'POST': # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.ip = request.META.get('REMOTE_ADDR')
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.save()  #save data to table
            messages.success(request,"Your message has ben sent.")
            return HttpResponseRedirect('/iletisim')
        
    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context={'setting':setting,'form':form, 'category':category }
    return render(request, 'iletisim.html', context)

def category_products(request,id,slug):  #checked
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'categorydata':categorydata,
                }
    return render(request,'products.html',context)

def product_search (request):  #checked
    if request.method == 'POST': # form post edildiyse I
        form = SearchForm(request.POST)
        if form.is_valid ():
                category= Category.objects.all()
                query = form.cleaned_data[ 'query']
                catid = form.cleaned_data[ 'catid'] #formdan bilgiyi al
                
                if catid ==0:
                    products = Product.objects.filter (title__icontains=query) # Select * from product where title like %query%
                else:
                    products = Product.objects.filter (title__icontains=query, category_id=catid)
                #return HttpResponse (products)    
                context = {'products': products,
                            'category': category,
                            }
                return render(request, 'products_search.html', context)
    return HttpResponseRedirect('/')

def product_detail(request,id,slug):  #checked
    category = Category.objects.all()   
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id= id )
    comments= Comment.objects.filter(product_id=id,status= 'True')
    context ={
        'category' : category ,
        'products' : product ,
        'images' : images ,
        'comments': comments,
        }
    return render(request,'product_detail.html',context)

def content_detail(request,id,slug):
    category = Category.objects.all()   
    product = Product.objects.filter(category_id=id) 
    link= '/product/'+str(product[0].id)+'/'+product[0].slug
    #return HttpResponse(link)
    return HttpResponseRedirect(link)


def product_search_auto(request):  #checked
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)    

def product_asearch(request):
    return render(request, 'asearch.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):  #checked ama 28/18 farklı
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:  
            messages.error(request,"Login hatası ! Kullanıcı adı ya da şifre yanlış.")
            return HttpResponseRedirect('/login') 

    category = Category.objects.all()
    context ={
        'category' : category ,
        }
    return render(request, 'login.html',context)

def signup_view(request): #checked
    if request.method == 'POST':
        form = SignUpForm(request.POST)  
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            #create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            return HttpResponseRedirect('/')
    
    form = SignUpForm()       
    category = Category.objects.all()
    context ={'category' : category ,
              'form':form,
            }
    return render(request, 'signup.html',context)

def mail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Form doğrulandıysa, e-posta gönder
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            send_mail(
                subject,
                message,
                email,
                ['destek@example.com'],  # Gönderilecek e-posta adresi
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'E-posta başarıyla gönderildi.'})
        else:
            return JsonResponse({'success': False, 'message': 'Form doğrulama hatası.'})
    else:
        form = ContactForm()

    return render(request, 'email.html', {'form': form})


# views.py

import csv  # CSV dosyalarını okumak için ekledik, ihtiyaca göre diğer modülleri ekleyebilirsiniz.
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import UploadedFile

def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Dosyayı kaydet

            # Dosyayı okuma ve işleme işlemleri
            file_content = uploaded_file.file.read().decode('utf-8')  # Dosyayı oku (örneğin UTF-8 kodlaması)

            # Örnek olarak bir CSV dosyasını işleme:
            csv_reader = csv.reader(file_content.splitlines())
            for row in csv_reader:   
                print(row)           
            return redirect('success_page')  # Başarılı bir şekilde işlendiyse başka bir sayfaya yönlendirin.
    else:
        form = FileUploadForm()

    return render(request, 'file_upload.html', {'form': form})
