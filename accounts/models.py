from django.db import models
from django.contrib.auth.models import AbstractUser


# ─── ROLE CHOICES ─────────────────────────────────────────────────────────────
ROLE_CHOICES = [
    ('admin',   'Admin'),
    ('doctor',  'Doctor'),
    ('patient', 'Patient'),
]

SPECIALIZATION_CHOICES = [
    ('Cardiologist',      'Cardiologist'),
    ('Dermatologist',     'Dermatologist'),
    ('Neurologist',       'Neurologist'),
    ('Orthopedic',        'Orthopedic'),
    ('Pediatrician',      'Pediatrician'),
    ('Psychiatrist',      'Psychiatrist'),
    ('General Physician', 'General Physician'),
    ('Dentist',           'Dentist'),
    ('ENT',               'ENT'),
    ('Gynecologist',      'Gynecologist'),
]

GENDER_CHOICES = [
    ('Male',   'Male'),
    ('Female', 'Female'),
    ('Other',  'Other'),
]


# ─── CUSTOM USER ──────────────────────────────────────────────────────────────
class User(AbstractUser):
    """Extended user with a role field."""
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

    def __str__(self):
        return f"{self.username} ({self.role})"


# ─── DOCTOR PROFILE ───────────────────────────────────────────────────────────
class DoctorProfile(models.Model):
    """
    Stores all extra information for a doctor account.
    Created when a doctor registers. is_verified=False until admin approves.
    New fields have blank=True and default='' so existing rows are unaffected.
    """
    user               = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctorprofile')

    # Basic info
    full_name          = models.CharField(max_length=100)
    email              = models.EmailField(blank=True, default='')
    phone              = models.CharField(max_length=15)
    specialization     = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    qualification      = models.CharField(max_length=200, blank=True, default='', help_text="e.g. MBBS, MD, MS")
    experience         = models.IntegerField(default=0, help_text="Years of experience")
    hospital_name      = models.CharField(max_length=200, blank=True, default='')

    # Verification
    doctor_id          = models.CharField(max_length=50, unique=True)
    medical_council_reg = models.CharField(max_length=100, blank=True, default='', verbose_name="Medical Council Reg. No.")

    # Files (optional — doctor may not upload immediately)
    profile_picture    = models.ImageField(upload_to='doctors/profile/', blank=True, null=True)
    id_proof           = models.FileField(upload_to='doctors/id_proof/', blank=True, null=True)

    # Status
    is_verified        = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Doctor Profile"
        ordering = ['-created_at']

    def __str__(self):
        return f"Dr. {self.full_name} — {self.specialization}"


# ─── PATIENT PROFILE ──────────────────────────────────────────────────────────
class PatientProfile(models.Model):
    """
    Stores extra information for a patient account.
    Created automatically when a patient registers.
    """
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patientprofile')

    full_name       = models.CharField(max_length=100, blank=True, default='')
    email           = models.EmailField(blank=True, default='')
    phone           = models.CharField(max_length=15, blank=True, default='')
    age             = models.IntegerField(default=0)
    gender          = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    address         = models.TextField(blank=True, default='')
    profile_picture = models.ImageField(upload_to='patients/profile/', blank=True, null=True)

    created_at      = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Patient Profile"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} (Patient)"