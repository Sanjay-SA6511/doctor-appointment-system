from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import User, DoctorProfile, PatientProfile, SPECIALIZATION_CHOICES
from appointments.models import Appointment, Message


# ══════════════════════════════════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════════════════════════════════

def home(request):
    """Public landing page."""
    # Count stats for the hero section
    doctor_count      = DoctorProfile.objects.filter(is_verified=True).count()
    patient_count     = PatientProfile.objects.count()
    appointment_count = Appointment.objects.count()
    return render(request, 'home.html', {
        'doctor_count':      doctor_count,
        'patient_count':     patient_count,
        'appointment_count': appointment_count,
    })


# ══════════════════════════════════════════════════════════════════════════════
#  PATIENT REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════

def user_register(request):
    """Patient self-registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password  = request.POST.get('password', '').strip()
        password2 = request.POST.get('password2', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        phone     = request.POST.get('phone', '').strip()
        age       = request.POST.get('age', 0)
        gender    = request.POST.get('gender', 'Male')
        address   = request.POST.get('address', '').strip()

        # ── Validation ──────────────────────────────────────────────────────
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose another.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'register.html')

        # ── Create User ─────────────────────────────────────────────────────
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='patient'
        )

        # ── Create Patient Profile ──────────────────────────────────────────
        PatientProfile.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            phone=phone,
            age=age,
            gender=gender,
            address=address,
        )

        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')

    return render(request, 'register.html')


# ══════════════════════════════════════════════════════════════════════════════
#  DOCTOR REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════

def doctor_register(request):
    """Doctor self-registration — account stays pending until Admin approves."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username           = request.POST.get('username', '').strip()
        email              = request.POST.get('email', '').strip()
        password           = request.POST.get('password', '').strip()
        password2          = request.POST.get('password2', '').strip()
        full_name          = request.POST.get('full_name', '').strip()
        phone              = request.POST.get('phone', '').strip()
        specialization     = request.POST.get('specialization', '')
        qualification      = request.POST.get('qualification', '').strip()
        experience         = request.POST.get('experience', 0)
        hospital_name      = request.POST.get('hospital_name', '').strip()
        doctor_id          = request.POST.get('doctor_id', '').strip()
        medical_council_reg = request.POST.get('medical_council_reg', '').strip()
        profile_picture    = request.FILES.get('profile_picture')
        id_proof           = request.FILES.get('id_proof')

        # ── Validation ──────────────────────────────────────────────────────
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'doctor_register.html', {'specializations': SPECIALIZATION_CHOICES})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'doctor_register.html', {'specializations': SPECIALIZATION_CHOICES})

        if DoctorProfile.objects.filter(doctor_id=doctor_id).exists():
            messages.error(request, 'This Doctor ID is already registered.')
            return render(request, 'doctor_register.html', {'specializations': SPECIALIZATION_CHOICES})

        # ── Create User ─────────────────────────────────────────────────────
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='doctor',
            is_active=True   # Account is active but NOT verified — blocked at login
        )

        # ── Create Doctor Profile ───────────────────────────────────────────
        DoctorProfile.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            phone=phone,
            specialization=specialization,
            qualification=qualification,
            experience=experience,
            hospital_name=hospital_name,
            doctor_id=doctor_id,
            medical_council_reg=medical_council_reg,
            profile_picture=profile_picture,
            id_proof=id_proof,
            is_verified=False   # Must be approved by admin
        )

        messages.success(
            request,
            'Registration submitted! Your account is under review. '
            'You will be able to log in once the Admin approves your profile.'
        )
        return redirect('login')

    return render(request, 'doctor_register.html', {'specializations': SPECIALIZATION_CHOICES})


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════════════════════════════════════

def user_login(request):
    """Unified login for all roles (admin/doctor/patient)."""
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

        # ── Doctor approval gate ─────────────────────────────────────────────
        if user.role == 'doctor':
            try:
                profile = DoctorProfile.objects.get(user=user)
                if not profile.is_verified:
                    messages.warning(
                        request,
                        'Your doctor account is pending Admin approval. '
                        'Please wait for verification.'
                    )
                    return render(request, 'login.html')
            except DoctorProfile.DoesNotExist:
                messages.error(request, 'Doctor profile not found. Contact admin.')
                return render(request, 'login.html')

        login(request, user)
        messages.success(request, f'Welcome back, {user.username}!')
        return _redirect_by_role(user)

    return render(request, 'login.html')


def _redirect_by_role(user):
    """Helper: redirect a logged-in user to their correct dashboard."""
    if user.is_superuser or user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'doctor':
        return redirect('doctor_home')
    else:
        return redirect('patient_home')


# ══════════════════════════════════════════════════════════════════════════════
#  LOGOUT
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARDS
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def doctor_home(request):
    """Doctor's main dashboard."""
    if request.user.role != 'doctor':
        return redirect('home')

    try:
        profile = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('home')

    from datetime import date
    today = date.today()

    all_appointments    = Appointment.objects.filter(doctor=request.user)
    today_appointments  = all_appointments.filter(date=today)
    upcoming_appointments = all_appointments.filter(date__gt=today, status='Approved')
    pending_appointments  = all_appointments.filter(status='Pending')

    return render(request, 'doctor_home.html', {
        'profile':              profile,
        'all_appointments':     all_appointments,
        'today_appointments':   today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_appointments': pending_appointments,
        'total_patients':       all_appointments.values('patient').distinct().count(),
        'completed_count':      all_appointments.filter(status='Completed').count(),
    })


@login_required
def patient_home(request):
    """Patient's main dashboard."""
    if request.user.role not in ('patient', 'admin') and not request.user.is_superuser:
        # If a doctor accidentally hits patient_home, redirect them
        if request.user.role == 'doctor':
            return redirect('doctor_home')

    try:
        profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        profile = None

    recent_appointments = Appointment.objects.filter(patient=request.user).order_by('-created_at')[:5]
    approved_doctors    = DoctorProfile.objects.filter(is_verified=True)[:6]

    return render(request, 'patient_home.html', {
        'profile':             profile,
        'recent_appointments': recent_appointments,
        'approved_doctors':    approved_doctors,
        'total_appointments':  Appointment.objects.filter(patient=request.user).count(),
        'pending_count':       Appointment.objects.filter(patient=request.user, status='Pending').count(),
    })


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def admin_dashboard(request):
    """Full admin control panel."""
    if not (request.user.is_superuser or request.user.role == 'admin'):
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')

    doctors         = DoctorProfile.objects.all().select_related('user')
    patients        = PatientProfile.objects.all().select_related('user')
    appointments    = Appointment.objects.all().select_related('patient', 'doctor')

    return render(request, 'admin_dashboard.html', {
        'pending_doctors':  doctors.filter(is_verified=False),
        'approved_doctors': doctors.filter(is_verified=True),
        'doctor_count':     doctors.count(),
        'patient_count':    patients.count(),
        'all_patients':     patients,
        'all_appointments': appointments,
        'appointment_count': appointments.count(),
        'pending_count':    appointments.filter(status='Pending').count(),
    })


def approve_doctor(request, doctor_id):
    """Admin approves a doctor."""
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('home')
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    doctor.is_verified = True
    doctor.save()
    messages.success(request, f'Dr. {doctor.full_name} has been approved.')
    return redirect('admin_dashboard')


def reject_doctor(request, doctor_id):
    """Admin rejects (and deletes) a pending doctor account."""
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('home')
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    name = doctor.full_name
    doctor.user.delete()   # Cascades to DoctorProfile
    messages.warning(request, f'Dr. {name}\'s account has been rejected and removed.')
    return redirect('admin_dashboard')


def delete_user(request, user_id):
    """Admin deletes any user."""
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('home')
    user = get_object_or_404(User, id=user_id)
    name = user.username
    user.delete()
    messages.warning(request, f'User "{name}" has been deleted.')
    return redirect('admin_dashboard')


# ══════════════════════════════════════════════════════════════════════════════
#  DOCTOR LIST & SEARCH
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def doctor_list(request):
    """List of approved doctors with search & specialization filter."""
    specialization = request.GET.get('specialization', '')
    search         = request.GET.get('search', '')

    doctors = DoctorProfile.objects.filter(is_verified=True).select_related('user')

    if specialization:
        doctors = doctors.filter(specialization=specialization)

    if search:
        doctors = doctors.filter(
            Q(full_name__icontains=search) |
            Q(hospital_name__icontains=search) |
            Q(specialization__icontains=search)
        )

    return render(request, 'doctor_list.html', {
        'doctors':          doctors,
        'specializations':  SPECIALIZATION_CHOICES,
        'selected_spec':    specialization,
        'search_query':     search,
    })


@login_required
def doctor_profile(request, doctor_id):
    """View of a single doctor's profile."""
    doctor = get_object_or_404(DoctorProfile, id=doctor_id, is_verified=True)
    return render(request, 'doctor_profile.html', {'doctor': doctor})


# ══════════════════════════════════════════════════════════════════════════════
#  APPOINTMENTS
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def book_appointment(request, doctor_id):
    """Patient books an appointment with a specific doctor."""
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('home')

    doctor_profile_obj = get_object_or_404(DoctorProfile, id=doctor_id, is_verified=True)
    doctor_user = doctor_profile_obj.user

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not date or not time:
            messages.error(request, 'Please select both date and time.')
            return render(request, 'book_appointment.html', {'doctor': doctor_profile_obj})

        # Check for duplicate booking
        existing = Appointment.objects.filter(
            patient=request.user,
            doctor=doctor_user,
            date=date,
            status__in=['Pending', 'Approved']
        ).exists()

        if existing:
            messages.warning(request, 'You already have an active appointment with this doctor.')
            return render(request, 'book_appointment.html', {'doctor': doctor_profile_obj})

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor_user,
            date=date,
            time=time,
            status='Pending'
        )
        messages.success(request, f'Appointment booked with Dr. {doctor_profile_obj.full_name}! Awaiting approval.')
        return redirect('patient_appointments')

    return render(request, 'book_appointment.html', {'doctor': doctor_profile_obj})


@login_required
def doctor_appointments(request):
    """Doctor views all their appointments."""
    if request.user.role != 'doctor':
        return redirect('home')

    from datetime import date
    today = date.today()
    appointments = Appointment.objects.filter(doctor=request.user).select_related('patient')

    return render(request, 'doctor_appointments.html', {
        'appointments':          appointments,
        'today_appointments':    appointments.filter(date=today),
        'pending_appointments':  appointments.filter(status='Pending'),
    })


@login_required
def patient_appointments(request):
    """Patient views their own appointments."""
    appointments = Appointment.objects.filter(patient=request.user).select_related('doctor')
    return render(request, 'patient_appointments.html', {'appointments': appointments})


@login_required
def update_appointment_status(request, appointment_id, status):
    """Doctor updates appointment status (Approved/Rejected/Completed)."""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    allowed_statuses = ['Approved', 'Rejected', 'Completed', 'Cancelled']

    # Only the appointment's doctor can change status
    if request.user != appointment.doctor:
        messages.error(request, 'You are not authorized to update this appointment.')
        return redirect('doctor_appointments')

    if status not in allowed_statuses:
        messages.error(request, 'Invalid status.')
        return redirect('doctor_appointments')

    appointment.status = status
    appointment.save()
    messages.success(request, f'Appointment status updated to {status}.')
    return redirect('doctor_appointments')


@login_required
def cancel_appointment(request, appointment_id):
    """Patient cancels their appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if appointment.status in ('Pending', 'Approved'):
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
    else:
        messages.error(request, 'This appointment cannot be cancelled.')
    return redirect('patient_appointments')


# ══════════════════════════════════════════════════════════════════════════════
#  PATIENT–DOCTOR CHAT
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def chat_view(request, appointment_id):
    """
    Chat interface between patient and doctor for a specific appointment.
    Both patient and doctor can send messages.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Only the patient or doctor of this appointment can access
    if request.user not in (appointment.patient, appointment.doctor):
        messages.error(request, 'Access denied.')
        return redirect('home')

    # Determine who the other person is
    if request.user == appointment.patient:
        other_user = appointment.doctor
    else:
        other_user = appointment.patient

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                appointment=appointment,
                sender=request.user,
                receiver=other_user,
                content=content,
            )
            # Mark unread messages as read
            Message.objects.filter(
                appointment=appointment,
                receiver=request.user,
                is_read=False
            ).update(is_read=True)

    all_messages = Message.objects.filter(appointment=appointment)

    # Mark incoming messages as read on page load
    Message.objects.filter(
        appointment=appointment,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return render(request, 'chat.html', {
        'appointment': appointment,
        'messages':    all_messages,
        'other_user':  other_user,
    })


# ══════════════════════════════════════════════════════════════════════════════
#  PROFILE MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def patient_profile(request):
    """Patient views and edits their profile."""
    try:
        profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone     = request.POST.get('phone', '').strip()
        age       = request.POST.get('age', 0)
        gender    = request.POST.get('gender', 'Male')
        address   = request.POST.get('address', '').strip()
        picture   = request.FILES.get('profile_picture')

        if profile:
            profile.full_name = full_name
            profile.phone     = phone
            profile.age       = age
            profile.gender    = gender
            profile.address   = address
            if picture:
                profile.profile_picture = picture
            profile.save()
        else:
            PatientProfile.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                age=age,
                gender=gender,
                address=address,
                profile_picture=picture,
            )

        messages.success(request, 'Profile updated successfully.')
        return redirect('patient_profile')

    from .models import GENDER_CHOICES
    return render(request, 'patient_profile.html', {
        'profile':       profile,
        'gender_choices': GENDER_CHOICES,
    })


@login_required
def doctor_profile_edit(request):
    """Doctor edits their own profile info."""
    try:
        profile = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('doctor_home')

    if request.method == 'POST':
        profile.full_name     = request.POST.get('full_name', profile.full_name)
        profile.phone         = request.POST.get('phone', profile.phone)
        profile.hospital_name = request.POST.get('hospital_name', profile.hospital_name)
        profile.qualification = request.POST.get('qualification', profile.qualification)
        profile.experience    = request.POST.get('experience', profile.experience)

        picture = request.FILES.get('profile_picture')
        if picture:
            profile.profile_picture = picture

        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('doctor_home')

    return render(request, 'doctor_profile_edit.html', {
        'profile':        profile,
        'specializations': SPECIALIZATION_CHOICES,
    })