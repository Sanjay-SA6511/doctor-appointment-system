from django.contrib import admin
from .models import Appointment, Message


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display  = ('patient', 'doctor', 'date', 'time', 'status', 'created_at')
    list_filter   = ('status', 'date')
    search_fields = ('patient__username', 'doctor__username')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ('sender', 'receiver', 'appointment', 'timestamp', 'is_read')
    list_filter   = ('is_read',)
    search_fields = ('sender__username', 'receiver__username')
    readonly_fields = ('timestamp',)