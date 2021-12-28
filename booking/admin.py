from django.contrib import admin

from .models import *

admin.site.register(Room)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(TicketType)
admin.site.register(Discount)