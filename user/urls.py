from django import views
from django.urls import path
from user import views



urlpatterns = [
    path('',views.index, name ='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('orders/',views.orders, name='orders'),
    path('orderdetail/<int:id>',views.orderdetail, name='orderdetail'),
    path('deletecomment/<int:id>',views.deletecomment, name='deletecomment'),
    path('commetns/',views.comments, name='comments'),
]
