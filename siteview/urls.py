from django.contrib import admin
from django.urls import path
from .import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.homePage),
    path('home/', views.homePage,name='home'),
    path('bookticket/', views.bookTicket, name='booktic'),
    path('book/',views.bookbus, name='book'),
    path('seeroutes/', views.seeRoutes),
    path('signup/', views.signUp, name='signUp'),
    path('login/', views.signin, name='login'),
    path('signout/', views.signOut, name='signout'),
    path('history/',views.history),
    path('cancel/',views.cancel,name='cancel')
    
]