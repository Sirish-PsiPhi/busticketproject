from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from siteview.models import AvailableBusRoute, Route, Bus, BookedTicket
# Create your views here.
@login_required(login_url='login')
def siteAdmin(request):
    admin = {}
    if(request.user.is_superuser):
        return render(request, 'foradmin/siteadmin.html')
    else:
        admin['error'] = "You are not Authorized to view this page"
        return render(request, 'foradmin/siteadmin.html',{'admin':admin})



def adminBus(request):
    buss = Bus.objects.all()
    return render(request, 'foradmin/adminbus.html',{'buss':buss})



def adminRoute(request):
    routes = Route.objects.all()
    return render(request, 'foradmin/adminroute.html',{'routes':routes})



def adminUser(request):
    users = User.objects.all()
    return render(request, 'foradmin/adminuser.html',{'users':users})



def adminTicket(request):
    tickets = BookedTicket.objects.all()
    return render(request, 'foradmin/adminticket.html',{'tickets':tickets})



def adminAvailable(request):
    availables = AvailableBusRoute.objects.all()
    return render(request, 'foradmin/adminavailable.html',{'availables':availables})



def addARoute(request):
    if request.method == 'POST':
        rid = request.POST.get('rid')
        bid = request.POST.get('bid')
        date = request.POST.get('date')
        time = request.POST.get('time')
        added = {}
        if rid and bid and date and time:
            rrid = Route.objects.filter(rID=rid)
            bbid = Bus.objects.filter(bID=bid)
            if rrid and bbid:
                newroute = AvailableBusRoute.objects.create(bID=bbid[0],rID=rrid[0],jDate=date,jTime=time)
            #route = AvailableBusRoute.objects.filter(rID=rrid[0].rID,bID=bbid[0].bID)
                added['all'] = "A new available Route with Rid "+str(rid) + ' Bid ' + str(bid) + ' date ' + str(date) + ' and time' + str(time) + ' has been created'
                return render(request, 'foradmin/addaroute.html',{'route':added})
            else:
                added['error'] = "That Bid or Rid does not exists"
                return render(request, 'foradmin/addaroute.html',{'route':added})
        else:
            addaroute = {}
            addaroute['error'] = "All Fields are compulsory"
            return render(request, 'foradmin/addaroute.html',{'addaroute':addaroute})
    return render(request, 'foradmin/addaroute.html')




def changeAroute(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        #rid = request.POST.get('rid')
        bid = request.POST.get('bid')
        date = request.POST.get('jdate')
        time = request.POST.get('time')
        changed = {}
        if id:
            toChange = AvailableBusRoute.objects.filter(id=id)
            changed['message'] = "The following this have been Updated"
            if bid and time:
                changed['bid'] = bid
                changed['time'] = time
                toChange.update(bID=bid,jTime=time)
                return render(request, 'foradmin/adminavailable.html',{'changed':changed})
            elif bid and date:
                changed['bid'] = bid
                changed['date'] = date
                toChange.update(bID=bid,jDate=date)
                return render(request, 'foradmin/adminavailable.html',{'changed':changed})
            elif date and time:
                changed['date'] = date
                changed['time'] = time
                toChange.update(jDate=date,jTime=time)
                return render(request, 'foradmin/adminavailable.html',{'changed':changed})
            elif bid:
                changed['bid'] = bid
                toChange.update(bID=bid)
                return render(request, 'foradmin/adminavailable.html',{'changed':changed})
            elif date:
                changed['date'] = date
                toChange.update(jDate=date)
                return render(request, 'foradmin/adminavailable.html',{'changed':changed})
            elif time:
                changed['time'] = time
                toChange.update(jTime=time)
                return render(request, 'foradmin/adminavailable.html',{'changed':changed})
            else:
                changed['error'] = "One of the fields is necessary to change"
                return render(request, 'foradmin/adminavailable.html',{'changedaroute':changed})
        else:
            changedaroute = {}
            changedaroute['error'] = "ID is compulsory"
            return render(request, 'foradmin/adminavailable.html',{'changedaroute':changedaroute})



def deleteAroute(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        deleted = {}
        if id:
            deleted['message'] = 'The following available Route has been deleted'
            AvailableBusRoute.objects.filter(id=id).delete()
            deleted['del'] = str(id) + "Has been deleted"
            return render(request, 'foradmin/adminavailable.html',{'deleted':deleted})
        else:
            deletedaroute = {}
            deletedaroute['error'] = "ID is compulsory"
            return render(request, 'foradmin/adminavailable.html',{'deletedaroute':deletedaroute})



def addBus(request):
    if request.method == 'POST':
        bid = request.POST.get('bid')
        bustype = request.POST.get('bustype')
        seats = request.POST.get('seats')
        cost = request.POST.get('cost')
        added = {}
        if bid and bustype and seats and cost:
            if not Bus.objects.filter(bID=bid).exists():
                added['message'] = "The following Bus has beed added with"
                addBus = Bus.objects.create(bID=bid,busType=bustype,seats=seats,costpseat=cost)
                added['add'] = "bid "+str(bid) + " bustype " + str(bustype) + " seats " + str(seats) + " cost " + str(cost) + " "
                return render(request, 'foradmin/addbus.html',{'added':added})
            else:
                added['error'] = "That Bid already exists"
                return render(request, 'foradmin/addbus.html',{'added':added})
        else:
            addbus = {}
            addbus['error'] = "All fields are necessary"
            return render(request, 'foradmin/addbus.html',{'added':addbus})
    return render(request, 'foradmin/addbus.html')



def deleteBus(request):
    if request.method == 'POST':
        bid = request.POST.get('bid')
        deleted = {}
        if bid:
            if Bus.objects.filter(bID=bid).exists():
                Bus.objects.filter(bID=bid).delete()
                deleted['del'] = str(bid) + "Has been deleted"
                return render(request, 'foradmin/adminbus.html',{'deleted':deleted})
            else:
                deleted['error'] = "That bus does not exists"
                return render(request, 'foradmin/adminbus.html',{'deleted':deleted})
        else:
            deletedabus = {}
            deletedabus['error'] = "BID is compulsory"
            return render(request, 'foradmin/adminbus.html',{'deletedabus':deletedabus})



def changeBus(request):
    if request.method == 'POST':
        bid = request.POST.get('bid')
        bustype = request.POST.get('bustype')
        seats = request.POST.get('seats')
        cost = request.POST.get('cost')
        changed = {}
        if bid:
            if Bus.objects.filter(bID=bid).exists():
                changeBus = Bus.objects.filter(bID=bid)
                changed['message'] = "That following things have been Updated"
                if bustype and cost and seats:
                    changed['bustype'] = "Bus Type"+str(bustype)
                    changed['seats'] = "Seats"+str(seats)
                    changed['cost'] = "Cost"+str(cost)
                    changeBus.update(busType=bustype,seats=seats,costpseat=cost)
                    return render(request, 'foradmin/adminbus.html',{'changed':changed})
                elif bustype and seats:
                    changed['bustype'] = "Bus Type"+str(bustype)
                    changed['seats'] = "Seats"+str(seats)
                    changeBus.update(busType=bustype,seats=seats)
                    return render(request, 'foradmin/adminbus.html',{'changed':changed})
                elif seats and cost:
                    changed['seats'] = "Seats"+str(seats)
                    changed['cost'] = "Cost"+str(cost)
                    changeBus.update(seats=seats,costpseat=cost)
                    return render(request, 'foradmin/adminbus.html',{'changed':changed})
                elif bustype and cost:
                    changed['cost'] = "Cost"+str(cost)
                    changed['bustype'] = "Bus Type"+str(bustype)
                    changeBus.update(busType=bustype,costpseat=cost)
                    return render(request, 'foradmin/adminbus.html',{'changed':changed})
                elif seats:
                    changed['seats'] = "Seats"+str(seats)
                    changeBus.update(seats=seats)
                    return render(request, 'foradmin/adminbus.html',{'changed':changed})
                elif bustype:
                    changed['bustype'] = "Bus Type"+str(bustype)
                    changeBus.update(busType=bustype)
                    return render(request, 'foradmin/adminbus.html',{'changed':changed})
                elif cost:
                    changed['cost'] = "Cost"+str(cost)
                    changeBus.update(costpseat=cost)
                    return render(request, 'foradmin/adminbus.html',{'changed':changed})
                else:
                    changed['error'] = "One of the Filed is necessasry to change"
                    return render(request, 'foradmin/adminbus.html',{'changed':changed})
            else:
                changed['error'] = "That Bus does not exists"
                return render(request, 'foradmin/adminbus.html',{'changed':changed})
        else:
            changedabus = {}
            changedabus['error'] = "Bid is compulsory"
            return render(request, 'foradmin/adminbus.html',{'changedabus':changedabus})



def changeTicket(request):
    if request.method == 'POST':
        tid = request.POST.get('tid')
        status = request.POST.get('status')
        changed = {}
        if tid:
            if BookedTicket.objects.filter(tId=tid).exists():
                changeTicket = BookedTicket.objects.filter(tID=tid)
                if status:
                    changed['status'] = "Status Has beed Changed"
                    changeTicket.update(status=status)
                    return render(request,'foradmin/adminticket.html',{'changed':changed})
                else:
                    changed['error'] = "Status is necessary"
                    return render(request,'foradmin/adminticket.html',{'changed':changed})
            else:
                changed['error'] = "That Ticket ID does not exists"
                return render(request,'foradmin/adminticket.html',{'changed':changed})
        else:
            changed['error'] = "Tid is necessary"
            return render(request,'foradmin/adminticket.html',{'changed':changed})



def deleteUser(request):
    if request.method == 'POST':
        uid = request.POST.get('id')
        deleted = {}
        if uid:
            if User.objects.filter(id=uid).exists():
                delUser = User.objects.filter(id=uid)
                delUser.delete()
                deleted['uid'] = "User ID"+str(uid) + " has been deleted"
                return render(request, 'foradmin/adminuser.html',{'deleted':deleted})
            else:
                deleted['error'] = "That User Id does not exists"
                return render(request, 'foradmin/adminuser.html',{'deleted':deleted})
        else:
            deleted['error'] = "Uid is compulsory"
            return render(request, 'foradmin/adminuser.html',{'deleted':deleted})



def addRoute(request):
    if request.method == 'POST':
        rid = request.POST.get('rid')
        source = request.POST.get('source')
        dest = request.POST.get('destination')
        added = {}
        if rid and source and dest:
            if not Route.objects.filter(rID=rid).exists():
                added['message'] = 'The following Route has been added'
                add = Route.objects.create(rID=rid,source=source,destination=dest)
                added['all'] = "rID"+str(rid) + " source " + str(source) + " destination" + str(dest)
                return render(request, 'foradmin/addroute.html',{'added':added})
            else:
                added['error'] = 'That Rid already exists'
                return render(request, 'foradmin/addroute.html',{'added':added})
        else:
            addroute = {}
            addroute['error'] = "All fields are compulsory"
            return render(request, 'foradmin/addroute.html',{'addroute':addroute})
    return render(request, 'foradmin/addroute.html')



def changeRoute(request):
    if request.method == 'POST':
        rid = request.POST.get('rid')
        source = request.POST.get('source')
        dest = request.POST.get('destination')
        changed = {}
        if rid:
            if Route.objects.filter(rID=rid).exists():
                changed['message'] = "The following has been changed"
                changeR = Route.objects.filter(rID=rid)
                if source and dest:
                    changed['source'] = "Source"+str(source)
                    changed['dest'] = "Destination"+str(dest)
                    changeR.update(source=source,destination=dest)
                    return render(request,'foradmin/adminroute.html',{'changed':changed})
                elif source:
                    changed['source'] = "Source"+str(source)
                    changeR.update(source=source)
                    return render(request,'foradmin/adminroute.html',{'changed':changed})
                elif dest:
                    changed['dest'] = "Destination"+str(dest)
                    changeR.update(destination=dest)
                    return render(request,'foradmin/adminroute.html',{'changed':changed})
                else:
                    changed['error'] = "One of the field is necessary to change"
                    return render(request,'foradmin/adminroute.html',{'changed':changed})
            else:
                changed['error'] = 'That Rid does not exsists'
                return render(request,'foradmin/adminroute.html',{'changed':changed})
        else:
            changedaroute = {}
            changedaroute['error'] = "Rid is compulsory"
            return render(request,'foradmin/adminroute.html',{'changedaroute':changedaroute})



def deleteRoute(request):
    if request.method == 'POST':
        rid = request.POST.get('rid')
        deleted = {}
        if rid:
            if Route.objects.filter(rID=rid).exists():
                Route.objects.filter(rID=rid).delete()
                deleted['rid'] = "This"+str(rid)+" Has been deleted"
                return render(request,'foradmin/adminroute.html',{'deleted':deleted})
            else:
                deleted['error'] = "That Rid does not exsists"
                return render(request,'foradmin/adminroute.html',{'deleted':deleted})
        else:
            deletedaroute = {}
            deletedaroute['error'] = 'RId is compulsory'
            return render(request,'foradmin/adminroute.html',{'deletedaroute':deletedaroute})
