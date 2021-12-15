from django.contrib import admin
from django.urls import path,re_path
from .views import *
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static


urlpatterns = [
    path('' , login_user  , name="login_user"),
    path('register_user' , register_user  , name="register_user"),
    path('verify' , verify  , name="verify"),
    path('logout', LogoutView.as_view(template_name='login.html'), name='logout'),
    path('instagram' , instagram  , name="instagram"),
    path('task' , task  , name="task"),
    path('ig_reply' , ig_reply  , name="ig_reply"),
    path('chunk/<int:pk>', chunk , name="chunk"),
    path('chunk/<int:pk>', chunk , name="chunk"),
    path('task_delete/<int:pk>' , task_delete , name="task_delete"),
    path('chunk_delete/<int:pk>' , chunk_delete , name="chunk_delete"),
]
