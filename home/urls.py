from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name ='index'), #atilsamancioglu.com/tweetapp/
    path('mail/', views.mail, name='mail'),
]