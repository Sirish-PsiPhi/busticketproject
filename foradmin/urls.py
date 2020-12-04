from django.contrib import admin
from django.urls import path
from .import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.siteAdmin),
    path('users/',views.adminUser,name='user'),
    path('users/delete',views.deleteUser,name='userdelete'),
    path('bus/',views.adminBus,name='bus'),
    path('bus/add/',views.addBus,name='busadd'),
    path('bus/change/',views.changeBus,name='buschange'),
    path('bus/delete/',views.deleteBus,name='busdelete'),
    path('route/',views.adminRoute,name='route'),
    path('route/add/',views.addRoute,name='routeadd'),
    path('route/change/',views.changeRoute,name='routechange'),
    path('route/delete/',views.deleteRoute,name='routedelete'),
    path('ticket/',views.adminTicket,name='ticket'),
    path('ticket/change',views.changeTicket,name='ticchange'),
    path('available/',views.adminAvailable,name='avail'),
    path('available/add/',views.addARoute,name='add'),
    path('available/change/',views.changeAroute,name='change'),
    path('available/delete/',views.deleteAroute,name='delete'),
]