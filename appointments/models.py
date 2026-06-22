from django.db import models
from accounts.models import User


# ─── STATUS CHOICES ───────────────────────────────────────────────────────────
STATUS_CHOICES = [
    ('Pending',   'Pending'),
    ('Approved',  'Approved'),
    ('Rejected',  'Rejected'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]


# ─── APPOINTMENT ──────────────────────────────────────────────────────────────
class Appointment(models.Model):
    """
    Represents a patient booking with a doctor.
    Status flow: Pending → Approved / Rejected → Completed
    """
    patient    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')

    date       = models.DateField()
    time       = models.TimeField()

    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Doctor can write notes visible to the patient
    notes      = models.TextField(blank=True, help_text="Doctor's notes for the patient")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Appointment"

    def __str__(self):
        return f"{self.patient.username} → Dr. {self.doctor.username} ({self.date} {self.time}) [{self.status}]"


# ─── MESSAGE (Patient–Doctor Chat) ────────────────────────────────────────────
class Message(models.Model):
    """
    Secure messaging between patient and doctor.
    Each message is linked to an appointment for context.
    Future-ready: can be upgraded to WebSocket or Gemini-powered replies.
    """
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE,
        related_name='messages',
        null=True, blank=True
    )
    sender      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    is_read     = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Message"

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:40]}"