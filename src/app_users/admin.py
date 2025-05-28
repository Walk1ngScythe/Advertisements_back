from django.contrib import admin
from .models import CustomUser, Role, Company, SellerApplication

admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Company)
admin.site.register(SellerApplication)