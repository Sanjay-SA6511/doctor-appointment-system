from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DoctorProfile, PatientProfile


# ─── CUSTOM USER ADMIN ────────────────────────────────────────────────────────
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('username', 'email', 'role', 'is_active', 'is_superuser', 'date_joined')
    list_filter   = ('role', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('MedCare Role', {'fields': ('role',)}),
    )


# ─── DOCTOR PROFILE ADMIN ─────────────────────────────────────────────────────
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'specialization', 'experience', 'hospital_name', 'is_verified', 'created_at')
    list_filter   = ('is_verified', 'specialization')
    search_fields = ('full_name', 'doctor_id', 'medical_council_reg')
    list_editable = ('is_verified',)
    readonly_fields = ('created_at',)


# ─── PATIENT PROFILE ADMIN ────────────────────────────────────────────────────
@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'phone', 'age', 'gender', 'created_at')
    list_filter   = ('gender',)
    search_fields = ('full_name', 'phone')
    readonly_fields = ('created_at',)