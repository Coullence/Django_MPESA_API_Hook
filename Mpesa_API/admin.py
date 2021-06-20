from django.contrib import admin
from .models import MpesaPayment, STKPayment


admin.site.register(MpesaPayment)
admin.site.register(STKPayment)