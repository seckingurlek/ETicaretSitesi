from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name ='index'), #atilsamancioglu.com/tweetapp/
    #path('<int:question_id>/',views.detail,name='detail'), #atilsamancioglu.com/tweetapp/addtweet

]