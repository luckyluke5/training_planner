from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission

from health_tracker.models import Date, Value, Rating

admin.site.register(Date)
admin.site.register(Value)
admin.site.register(Rating)

#admin.site.register(Permission)