from django.contrib import admin
from django.urls import path
from .import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.homePage),
    path('home/', views.homePage),
    path('bookticket/', views.bookTicket),
    path('seeroutes/', views.seeRoutes),
    path('signup/', views.signUp, name='signUp'),
    path('login/', views.signin, name='login'),
    
]