from django.contrib import admin
from .models import Complaint, ComplaintStatus

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('description', 'sender__phone_number', 'recipient__phone_number')

@admin.register(ComplaintStatus)
class ComplaintStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
