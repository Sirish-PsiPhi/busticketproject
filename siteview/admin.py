from django.contrib import admin
from .models import Bus, Route, AvailableBusRoute

# Register your models here.
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(AvailableBusRoute)