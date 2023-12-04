
from os import path
from django import views


urlpatterns = [
    path('', views.index, name='index'),
    path('addtocart/<int:id>', views.addtocart, name='addtocart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
]