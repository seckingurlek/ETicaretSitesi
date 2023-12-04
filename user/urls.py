from django import views
from django.urls import path
from user import views

urlpatterns = [
    path('',views.index, name ='index'),
    path('addcomment/<int:id>',views.addcomment,name='addcomment'),
    path('<int:question_id>/',views.detail,name='detail'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='user_password'),

]