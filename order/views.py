from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from home.models import UserProfile
# Create your views here.
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct
from product.models import Category, Product
from django.utils.crypto import get_random_string


def index(request):
     return HttpResponse('Order App')

  
@login_required (login_url='/login') # Check Login  #checked
def addtocart (request, id):
    url= request.META.get('HTTP_REFERER') # get Last url
    current_user = request.user
    #******** ÜRÜRN SEPETTE VAR MI KONTROL****
    checkproduct = ShopCart.objects.filter(product_id=id) #varmı kontrol
    if checkproduct:
         control = 1
    else:
         control = 0
    
    if request.method == 'POST': # form post edildiyse ürün detay sayasından
        form = ShopCartForm (request. POST)
        if form.is_valid ():
            if control ==1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  #
            else:  #  ürün yoksa ekle
                data = ShopCart()  # model ile bağlantı kur
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()  #
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count() #count item on shopcart
        messages.success(request, "ürün sepete eklendi")
        return HttpResponseRedirect(url)
                    #return HttpResponse ("Kaydedildi")
    else: #ürün sepete ekle butonuna basıldıysa
        if control ==1: #ürün varsa güncelle
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()  #
        else:  #  ürün yoksa ekle
            data = ShopCart #model ile bağlantı4
            data.user_id = current_user.id
            data.product_id = id  
            data.quantity = 1
            data.save() #veritabanına kaydet
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count() 
        messages.success(request, "ürün sepete eklendi.")
        return HttpResponseRedirect(url) 
    
    messages.warning(request, "ürün eklenirken hata oluştu. kontrol edin")
    return HttpResponseRedirect(url)



@login_required(login_url='/login') #check again  #checked bat request session fazla 
def shopcart(request):
    category = Category.objects.all()   #checked
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    context = { 'shopcart':shopcart,
               'total':total,
               'category':category
               }    
    return render(request,'shopcart_product.html',context)

@login_required(login_url='/login')  #checked
def deletefromcart(request,id):
     ShopCart.objects.filter(id=id).delete()
     current_user = request.user
     request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count
     messages.success(request,"ürün silindi")
     return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')  #checked
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:       
        total += rs.product.price * rs.quantity
          
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............
            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
            data.save() #
            #sepetteki ürünleri ordera kaydetme
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id    = data.id # Order için oluşturulan id orders producta kaydediliyo
                detail.product_id  = rs.product_id
                detail.user_id     = current_user.id
                detail.quantity    = rs.quantity   
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
             
                # ***Reduce quantity of sold product from Amount of Product
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity #sepete eklenen ürün kadar productan düşürülüyor mevcut kalan belirlensin
                product.save()
                
            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html',{'ordercode':ordercode,'category':category,})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form= OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request, 'Order_Form.html', context)


        

  