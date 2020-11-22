from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import AvailableBusRoute
# Create your views here.
def homePage(request):
    return render(request, 'siteview/homePage.html')

@login_required(login_url='signUp')
def bookTicket(request):
    return render(request, 'siteview/bookTicket.html')

def seeRoutes(request):
    availbus = AvailableBusRoute.objects.all()
    return render(request, 'siteview/availableRoutes.html', {'avail': availbus})

def signUp(request):
    context = {}
    if request.method == 'POST':
        name_s = request.POST.get('uname')
        email_s = request.POST.get('email')
        password_s = request.POST.get('pass')
        user = User.objects.create_user(name_s, email_s, password_s,)
        if user:
            login(request, user)
            return render(request, 'siteview/homePage.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signUp.html', context)

    return render(request, 'siteview/signUp.html')

def signin(request):
    context = {}
    if request.method == 'POST':
        name_s = request.POST.get('uname')
        password_s = request.POST.get('password')
        user = authenticate(request, username=name_s, password=password_s)
        if user:
            login(request, user)
            # username = request.session['username'
            return render(request, 'siteview/homePage.html')
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'siteview/login.html')
    return render(request, 'siteview/login.html')

def signOut(request):
    logout(request)
    return render(request, 'siteview/homePage.html')