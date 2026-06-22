from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as a
from ai_assistant import views as ai

urlpatterns = [

    # ── Django admin (superuser panel) ────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ── AUTH ──────────────────────────────────────────────────────────────────
    path('',          a.home,          name='home'),
    path('register/', a.user_register, name='register'),
    path('login/',    a.user_login,    name='login'),
    path('logout/',   a.user_logout,   name='logout'),

    # ── DASHBOARDS ────────────────────────────────────────────────────────────
    path('doctor-home/',  a.doctor_home,  name='doctor_home'),
    path('patient-home/', a.patient_home, name='patient_home'),

    # ── DOCTOR REGISTRATION ───────────────────────────────────────────────────
    path('doctor-register/', a.doctor_register, name='doctor_register'),

    # ── DOCTOR LIST & SEARCH ──────────────────────────────────────────────────
    path('doctors/',                  a.doctor_list,    name='doctor_list'),
    path('doctor/<int:doctor_id>/',   a.doctor_profile, name='doctor_profile'),

    # ── APPOINTMENTS ──────────────────────────────────────────────────────────
    path('book/<int:doctor_id>/',                        a.book_appointment,    name='book_appointment'),
    path('doctor-appointments/',                         a.doctor_appointments, name='doctor_appointments'),
    path('patient-appointments/',                        a.patient_appointments, name='patient_appointments'),
    path('appointment-status/<int:appointment_id>/<str:status>/',
         a.update_appointment_status, name='update_appointment_status'),
    path('appointment-cancel/<int:appointment_id>/',
         a.cancel_appointment, name='cancel_appointment'),

    # ── CHAT ──────────────────────────────────────────────────────────────────
    path('chat/<int:appointment_id>/', a.chat_view, name='chat'),

    # ── PROFILE MANAGEMENT ────────────────────────────────────────────────────
    path('patient-profile/',  a.patient_profile,    name='patient_profile'),
    path('doctor-profile/',   a.doctor_profile_edit, name='doctor_profile_edit'),

    # ── ADMIN DASHBOARD ───────────────────────────────────────────────────────
    path('admin-dashboard/',                   a.admin_dashboard, name='admin_dashboard'),
    path('approve-doctor/<int:doctor_id>/',    a.approve_doctor,  name='approve_doctor'),
    path('reject-doctor/<int:doctor_id>/',     a.reject_doctor,   name='reject_doctor'),
    path('delete-user/<int:user_id>/',         a.delete_user,     name='delete_user'),

    # ── AI MODULE ─────────────────────────────────────────────────────────────
    path('ai/', ai.ai_home, name='ai_home'),

]

# Serve media files during development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)