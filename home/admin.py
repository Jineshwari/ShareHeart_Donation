from django.contrib import admin
from .models import User, NGO, DonorInfo, Voucher



admin.site.register(User)
admin.site.register(NGO)
admin.site.register(DonorInfo)
admin.site.register(Voucher)


