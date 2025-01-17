from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import AvailableBusRoute, Route, Bus, BookedTicket
# Create your views here.
def homePage(request):
    return render(request, 'siteview/homePage.html')

@login_required(login_url='login')
def bookTicket(request):
    if request.method == 'POST':
        source_s = str(request.POST.get('source')).lower()
        destination_s = str(request.POST.get('dest')).lower()
        date_s = request.POST.get('date')
        routes = Route.objects.filter(source=source_s,destination=destination_s)
        if routes:
            avail = AvailableBusRoute.objects.none()
            for route in routes:
                avail |= AvailableBusRoute.objects.filter(rID=route.rID, jDate=date_s)
            if avail:
                return render(request, 'siteview/list.html', {'bus':avail})
            else:
                nobus = {}
                nobus['status'] = "No bus Available on that day"
                return render(request, 'siteview/list.html', {'no':nobus})
        else:
            avail = {}
            avail['status'] = "No Bus currently Available on that Route"
            return render(request, 'siteview/list.html', {'no':avail})
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
        if not User.objects.filter(username=name_s).exists():
            user = User.objects.create_user(name_s, email_s, password_s,)
            if user:
                login(request, user)
                return render(request, 'siteview/homePage.html')
            else:
                context["error"] = "Provide valid credentials"
                return render(request, 'siteview/signUp.html', {'error':context})
        else:
            context['error'] = 'Username Already Exsists'
            return render(request, 'siteview/signUp.html', {'error':context})

    return render(request, 'siteview/signUp.html')

def signin(request):
    context = {}
    if request.method == 'POST':
        name_s = request.POST.get('uname')
        password_s = request.POST.get('password')
        user = authenticate(request, username=name_s, password=password_s)
        if user:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('//127.0.0.1:8000/home')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'siteview/login.html',{'error':context})
    return render(request, 'siteview/login.html')

def signOut(request):
    logout(request)
    return redirect('//127.0.0.1:8000/home')
def bookbus(request):
    if request.method == 'POST':
        seats_booked = request.POST.get('seats')
        busid = request.POST.get('bid')
        id = AvailableBusRoute.objects.filter(id=busid)
        rid = Route.objects.filter(rID=id[0].rID)
        bus = Bus.objects.filter(bID=id[0].bID)
        rem = id[0].seats
        if id:
            if rem >= int(seats_booked):
               rem -= int(seats_booked)
               userid = request.user.id
               amount = bus[0].costpseat * int(seats_booked)
               done = BookedTicket.objects.create(bID=bus[0],rID=rid[0],uID=User.objects.filter(username=request.user.username)[0],booked=seats_booked,amount=amount,status='Booked') 
               id.update(seats=rem)
               return render(request, 'siteview/success.html',{'done':done})
            else:
                err = {}
                err['error'] = "That many seats are not available"
                return render(request, 'siteview/list.html',{'error':err})
        else:
            err = {}
            err['error'] = "That Route is not available"
            return render(request, 'siteview/bookTicket.html',{'error':err})

@login_required(login_url='login')
def history(request):
    booked = BookedTicket.objects.filter(uID=request.user.id)
    return render(request, 'siteview/history.html',{'books':booked})

@login_required(login_url='login')
def cancel(request):

    if request.method == 'POST':
        ticID = request.POST.get('bid')
        booked = BookedTicket.objects.filter(tID=ticID)
        if booked[0].status == 'Booked':
            booked.update(status='Canceled')
            seats = booked[0].booked
            bus = AvailableBusRoute.objects.filter(bID=booked[0].bID,rID=booked[0].rID)
            newseats = seats + bus[0].seats
            bus.update(seats=newseats)
            return render(request, 'siteview/cancel.html',{'book':booked})
        else:
            booked = {}
            booked['status'] = "Ticket has already been canceled"
            return render(request, 'siteview/cancel.html',{'done':booked})
    return render(request, 'siteview/cancel.html')
