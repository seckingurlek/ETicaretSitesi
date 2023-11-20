from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from eticaret.eticaret.forms import SearchForm

# Create your views here.
from home.models import Setting, ContactFormMessage, ContactForm
from django.contrib import messages
from product.models import Product, Category




def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category = Category.objects.all()
    dayproducts=Product.objects.all()[:4]
    lastproducts=Product.objects.all().order_by('-id')[:4]
    randomproduct=Product.objects.all().order_by('?')[:4]
    

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
    context = {'setting': setting}
    return render(request, 'hakkimizda.html',context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'referanslarimiz.html',context)


def iletisim(request): #formu kaydetme
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
    context={'setting':setting,'form':form }
    return render(request, 'iletisim.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.all(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'categorydata':categorydata,
                }
    return render(request,'products.html',context)

def product_search (request):
    if request.method == 'POST': # form post edildiyse I
        form = SearchForm(request.POST)
        if form.is_valid ():
                category= Category.objects.all()
                query = form.cleaned_data[ 'query'] #formdan bilgiyi al
                products = Product.objects.filter (title__icontains=query) # Select * from product where title like %query%
                    #return HttpResponse (products)
                context = {'products': products,
                            'category': category,
                            }
                return render (request, 'products_search.html', context)
    return HttpResponseRedirect('/')

