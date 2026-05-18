from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('home/',views.home,name='home'),
    path('member/',views.member_list,name='member_list'),
    path('login/',views.login_view,name='login'),
]