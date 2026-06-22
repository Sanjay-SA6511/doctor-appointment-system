from django.shortcuts import render


# ══════════════════════════════════════════════════════════════════════════════
#  SYMPTOM → SPECIALIST MAPPING
#  Future-ready: this dict can be replaced by a Gemini API call
#  without changing any template or URL structure.
# ══════════════════════════════════════════════════════════════════════════════

SYMPTOM_MAP = {
    # Cardiology
    'chest pain':          ('Cardiologist',      'Chest pain can indicate heart problems. Please consult a Cardiologist immediately. If severe, visit an emergency room.'),
    'heart':               ('Cardiologist',      'Heart-related symptoms require evaluation by a Cardiologist.'),
    'palpitation':         ('Cardiologist',      'Heart palpitations can be caused by arrhythmia or stress. A Cardiologist can help.'),
    'shortness of breath': ('Cardiologist',      'Difficulty breathing with chest discomfort may indicate a cardiac issue. Consult a Cardiologist urgently.'),
    'high bp':             ('Cardiologist',      'High blood pressure (hypertension) should be monitored by a Cardiologist.'),
    'hypertension':        ('Cardiologist',      'Hypertension needs regular monitoring. A Cardiologist can guide your treatment.'),

    # Neurology
    'headache':            ('Neurologist',       'Persistent or severe headaches may be related to neurological conditions. A Neurologist can evaluate this.'),
    'migraine':            ('Neurologist',       'Migraines are neurological events. A Neurologist can prescribe effective treatment plans.'),
    'blurred vision':      ('Neurologist',       'Blurred vision with headache may indicate neurological issues. See a Neurologist.'),
    'dizziness':           ('Neurologist',       'Frequent dizziness or vertigo may have neurological causes. Consult a Neurologist.'),
    'memory loss':         ('Neurologist',       'Memory issues or confusion may indicate neurological conditions. A Neurologist should evaluate you.'),
    'seizure':             ('Neurologist',       'Seizures are serious neurological events. Please consult a Neurologist urgently.'),
    'numbness':            ('Neurologist',       'Numbness or tingling in limbs may indicate nerve damage. A Neurologist can help.'),
    'paralysis':           ('Neurologist',       'Any paralysis or loss of motor function is a neurological emergency. Seek immediate help.'),

    # Dermatology
    'skin rash':           ('Dermatologist',     'Skin rashes can have various causes. A Dermatologist can diagnose and treat skin conditions.'),
    'acne':                ('Dermatologist',     'Persistent acne or skin breakouts should be evaluated by a Dermatologist.'),
    'itching':             ('Dermatologist',     'Chronic itching may indicate skin allergies or eczema. A Dermatologist can help.'),
    'hair loss':           ('Dermatologist',     'Hair loss (alopecia) can have medical causes. A Dermatologist or Trichologist can evaluate this.'),
    'psoriasis':           ('Dermatologist',     'Psoriasis is a chronic skin condition best managed by a Dermatologist.'),

    # Orthopedics
    'joint pain':          ('Orthopedic',        'Joint pain may indicate arthritis or injury. An Orthopedic specialist can diagnose and treat this.'),
    'bone pain':           ('Orthopedic',        'Bone pain should be evaluated by an Orthopedic specialist, especially if persistent.'),
    'back pain':           ('Orthopedic',        'Chronic back pain often has musculoskeletal causes. An Orthopedic doctor can help.'),
    'knee pain':           ('Orthopedic',        'Knee pain may be due to ligament injury or arthritis. An Orthopedic specialist can assess this.'),
    'fracture':            ('Orthopedic',        'Suspected fractures need immediate evaluation by an Orthopedic doctor.'),
    'swollen joint':       ('Orthopedic',        'Swollen joints may indicate inflammation or injury. See an Orthopedic specialist.'),

    # Pediatrics
    'child':               ('Pediatrician',      'For health concerns in children, a Pediatrician is the right specialist.'),
    'infant':              ('Pediatrician',      'Infant health concerns should be addressed by a Pediatrician promptly.'),
    'baby':                ('Pediatrician',      'Baby health and development is best monitored by a Pediatrician.'),
    'vaccination':         ('Pediatrician',      'Child vaccinations and immunizations are managed by Pediatricians.'),

    # Psychiatry / Mental Health
    'anxiety':             ('Psychiatrist',      'Anxiety disorders can significantly affect quality of life. A Psychiatrist can provide effective treatment.'),
    'depression':          ('Psychiatrist',      'Depression is a serious mental health condition. A Psychiatrist can help with therapy and medication.'),
    'stress':              ('Psychiatrist',      'Chronic stress and burnout benefit from professional support. Consider consulting a Psychiatrist.'),
    'insomnia':            ('Psychiatrist',      'Sleep disorders like insomnia can have psychological causes. A Psychiatrist or Sleep Specialist can help.'),
    'panic attack':        ('Psychiatrist',      'Panic attacks are treatable with proper psychiatric care.'),
    'mental':              ('Psychiatrist',      'Mental health concerns should be addressed by a qualified Psychiatrist.'),

    # Dentistry
    'toothache':           ('Dentist',           'Toothache can indicate dental decay or infection. See a Dentist as soon as possible.'),
    'tooth':               ('Dentist',           'Any tooth-related issue should be evaluated by a qualified Dentist.'),
    'gum':                 ('Dentist',           'Gum pain or bleeding can indicate gum disease. A Dentist can treat this.'),
    'cavity':              ('Dentist',           'Dental cavities require treatment from a Dentist to prevent further damage.'),
    'bleeding gums':       ('Dentist',           'Bleeding gums may indicate gingivitis. Visit a Dentist for evaluation.'),

    # ENT
    'ear pain':            ('ENT',               'Ear pain may indicate infection or wax buildup. An ENT specialist can treat ear conditions.'),
    'hearing loss':        ('ENT',               'Hearing loss needs evaluation by an ENT (Ear, Nose & Throat) specialist.'),
    'sore throat':         ('ENT',               'Persistent sore throat may indicate tonsillitis or other ENT issues.'),
    'nasal':               ('ENT',               'Nasal congestion, polyps, or sinusitis are treated by ENT specialists.'),
    'sinusitis':           ('ENT',               'Sinus infections and sinusitis are effectively treated by ENT doctors.'),
    'tonsil':              ('ENT',               'Tonsil-related issues like recurrent tonsillitis should be evaluated by an ENT specialist.'),

    # Gynecology
    'menstrual':           ('Gynecologist',      'Menstrual irregularities should be evaluated by a Gynecologist.'),
    'pregnancy':           ('Gynecologist',      'Pregnancy care and prenatal checkups are managed by Gynecologists/Obstetricians.'),
    'pcos':                ('Gynecologist',      'PCOS (Polycystic Ovarian Syndrome) is a condition treated by Gynecologists.'),
    'ovarian':             ('Gynecologist',      'Ovarian cysts or related issues need evaluation by a Gynecologist.'),
    'vaginal':             ('Gynecologist',      'Vaginal health concerns should be discussed with a Gynecologist.'),

    # General
    'fever':               ('General Physician', 'Fever can indicate infection. A General Physician can evaluate and treat it.'),
    'cold':                ('General Physician', 'Common cold symptoms can be treated by a General Physician.'),
    'cough':               ('General Physician', 'Persistent cough should be evaluated by a General Physician. Could be respiratory or allergy related.'),
    'vomiting':            ('General Physician', 'Vomiting may be caused by infection, food poisoning, or other conditions. A General Physician can help.'),
    'diarrhea':            ('General Physician', 'Diarrhea lasting more than 2 days should be evaluated by a General Physician.'),
    'stomach pain':        ('General Physician', 'Abdominal pain has many causes. A General Physician can examine and refer you to a specialist.'),
    'abdominal':           ('General Physician', 'Abdominal issues should be evaluated by a General Physician first.'),
    'fatigue':             ('General Physician', 'Persistent fatigue may indicate anemia, thyroid issues, or other conditions. See a General Physician.'),
    'weight loss':         ('General Physician', 'Unexplained weight loss should be investigated by a General Physician.'),
    'diabetes':            ('General Physician', 'Diabetes management and blood sugar control are handled by General Physicians and Endocrinologists.'),
}

# FAQ responses for non-symptom queries
FAQ_MAP = {
    'doctor':       'You can find all verified doctors on the <a href="/doctors/">Doctors page</a>. Filter by specialization to find the right specialist.',
    'appointment':  'To book an appointment: 1) Go to Doctors list, 2) Select a doctor, 3) Choose date and time, 4) Click "Book Appointment".',
    'book':         'You can book an appointment from the <a href="/doctors/">Doctors page</a> after logging in as a patient.',
    'cancel':       'You can cancel a pending or approved appointment from your <a href="/patient-appointments/">My Appointments</a> page.',
    'status':       'Your appointment status can be: Pending (awaiting doctor approval), Approved, Rejected, Completed, or Cancelled.',
    'login':        'Use your username and password on the <a href="/login/">Login page</a>. Doctors need admin approval before logging in.',
    'register':     'Patients can register at <a href="/register/">Patient Registration</a>. Doctors register at <a href="/doctor-register/">Doctor Registration</a>.',
    'hello':        None,  # Handled separately
    'hi':           None,
    'hey':          None,
    'emergency':    None,  # Handled separately
}


def ai_home(request):
    """
    AI Medical Assistant view.
    Uses session-based chat history.
    Architecture is future-ready: swap SYMPTOM_MAP logic with Gemini API call
    without changing any URL or template code.
    """

    # Initialize session chat
    if 'chat' not in request.session:
        request.session['chat'] = []

    # Handle clear chat
    if request.GET.get('clear') or request.POST.get('clear'):
        request.session['chat'] = []
        request.session.modified = True

    if request.method == 'POST' and not request.POST.get('clear'):
        raw_input = request.POST.get('message', '').strip()
        user_input_lower = raw_input.lower()

        specialist   = None
        response     = None

        # ── GREETING ────────────────────────────────────────────────────────
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good evening']):
            response = (
                "Hello! 👋 I'm MedCare AI, your personal medical assistant. "
                "Please describe your symptoms and I'll suggest the right specialist. "
                "Remember: I provide guidance only, not medical diagnosis."
            )

        # ── EMERGENCY ───────────────────────────────────────────────────────
        elif any(word in user_input_lower for word in ['emergency', 'ambulance', 'dying', 'unconscious', 'stroke']):
            response = (
                "🚨 <strong>EMERGENCY:</strong> Please call <strong>112</strong> (emergency services) "
                "or go to the nearest hospital immediately. "
                "Do not wait for an appointment in a medical emergency."
            )

        # ── THANK YOU ───────────────────────────────────────────────────────
        elif any(word in user_input_lower for word in ['thank', 'thanks', 'ok', 'okay', 'great']):
            response = "You're welcome! 😊 Feel free to ask any other health questions. Stay healthy!"

        # ── FAQ / SYSTEM QUESTIONS ──────────────────────────────────────────
        else:
            for keyword, faq_response in FAQ_MAP.items():
                if keyword != 'hello' and keyword != 'hi' and keyword != 'hey' and keyword != 'emergency':
                    if keyword in user_input_lower and faq_response:
                        response = faq_response
                        break

        # ── SYMPTOM CHECK ───────────────────────────────────────────────────
        if response is None:
            for symptom, (spec, msg) in SYMPTOM_MAP.items():
                if symptom in user_input_lower:
                    specialist = spec
                    response   = msg
                    break

        # ── FALLBACK ─────────────────────────────────────────────────────────
        if response is None:
            response = (
                "I didn't quite understand your query. Could you describe your symptoms more clearly? "
                "For example: 'I have a headache', 'I have chest pain', or 'I have a skin rash'. "
                "Or ask about doctors, appointments, or how to book a slot."
            )

        # ── APPEND TO CHAT ───────────────────────────────────────────────────
        chat = request.session.get('chat', [])
        chat.append({
            'user':       raw_input,
            'bot':        response,
            'specialist': specialist,
        })
        # Keep last 30 messages only
        request.session['chat'] = chat[-30:]
        request.session.modified = True

    return render(request, 'ai_home.html', {
        'chat': request.session.get('chat', []),
    })