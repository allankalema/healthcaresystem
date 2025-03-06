from django.db import models
from accounts.models import User
from django.utils.timezone import now

class AntenatalCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='antenatal_patients')  # Links to the registered patient
    Doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='antenatal_doctors', default=1)  # Links to the assigned doctor
    
    health_unit = models.CharField(max_length=255, blank=True, null=True )  # Health facility name
    reg_no = models.CharField(max_length=100, blank=True, null=True, unique=True)  # Unique registration number
    name = models.CharField(max_length=255)  # Patient's full name
    nin = models.CharField(max_length=20, unique=True, null=True, blank=True)  # National ID Number
    phone_no = models.CharField(max_length=15)  
    age = models.IntegerField(blank=True, null=True)  
    village = models.CharField(max_length=255)  
    parish = models.CharField(max_length=255)  
    sub_county = models.CharField(max_length=255)  
    district = models.CharField(max_length=255)  
    occupation = models.CharField(max_length=255)  
    religion = models.CharField(max_length=100, null=True, blank=True)  
    education_level = models.CharField(max_length=100, null=True, blank=True)  
    tribe = models.CharField(max_length=100, null=True, blank=True)  
    marital_status = models.CharField(
        max_length=20, choices=[('Single', 'Single'), ('Married', 'Married')]
    )

    next_of_kin_name = models.CharField(max_length=255,blank=True, null=True)  
    next_of_kin_phone = models.CharField(max_length=15, blank=True, null=True)  
    next_of_kin_relationship = models.CharField(max_length=100, blank=True, null=True)  
    next_of_kin_address = models.TextField(blank=True, null=True)  

    gravida = models.IntegerField(blank=True, null=True)  # Number of pregnancies
    para = models.IntegerField(blank=True, null=True)  # Number of deliveries after 28 weeks
    abortions = models.IntegerField(blank=True, null=True)  # Number of pregnancy losses before 28 weeks

    presenting_complaints = models.TextField(null=True, blank=True)  
    first_day_of_lnmp = models.DateField(blank=True, null=True)  # Last Normal Menstrual Period
    edd = models.DateField(blank=True, null=True)  # Estimated Due Date
    weeks_of_amenorrhea = models.IntegerField(blank=True, null=True)  # Number of weeks since last period
    complications_of_pregnancy = models.TextField(null=True, blank=True)  
    hospitalization = models.BooleanField(default=False ,blank=True, null=True)  
    hospitalization_reason = models.TextField(null=True, blank=True)
    Doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    
    next_visit = models.DateTimeField(null=True, blank=True)  # Date and time of the next visit
  

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Antenatal Card for {self.name} ({self.reg_no})"

# ----------------------- SEPARATE TABLES FOR TABULAR DATA -----------------------

class PreviousObstetricHistory(models.Model):
    antenatal_card = models.ForeignKey(AntenatalCard, on_delete=models.CASCADE, related_name="previous_obstetric_history")
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pregnancy_year = models.IntegerField()
    abortions_below_12_weeks = models.IntegerField()
    abortions_above_12_weeks = models.IntegerField()
    premature_births = models.IntegerField()
    full_term_deliveries = models.IntegerField()
    delivery_type = models.CharField(max_length=255)
    place_of_delivery = models.CharField(max_length=255)
    third_stage_complications = models.TextField(null=True, blank=True)
    puerperium = models.TextField(null=True, blank=True)
    baby_alive = models.BooleanField(default=True)
    stillbirth_or_nnd = models.BooleanField(default=False)
    baby_sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    birth_weight = models.FloatField()
    immunization_status = models.CharField(max_length=255)
    baby_health_condition = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Previous Pregnancy Record ({self.pregnancy_year}) for {self.antenatal_card.name}"


class AntenatalProgressExamination(models.Model):
    antenatal_card = models.ForeignKey(AntenatalCard, on_delete=models.CASCADE, related_name="progress_examinations")
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateField(default=now)
    fundal_height = models.FloatField()
    presentation = models.CharField(max_length=255)
    fetal_heart_rate = models.IntegerField()
    varicose_or_oedema = models.CharField(max_length=255, null=True, blank=True)
    urine_test_results = models.TextField(null=True, blank=True)
    iron_folic_acid_pills = models.IntegerField(null=True, blank=True)
    complaints_and_remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Antenatal Progress for {self.antenatal_card.name} on {self.visit_date}"


class UltrasoundReport(models.Model):
    antenatal_card = models.ForeignKey(AntenatalCard, on_delete=models.CASCADE, related_name="ultrasound_reports")
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ultrasound_date = models.DateField(default=now)
    gestational_age = models.IntegerField(null=True, blank=True)
    placenta_details = models.TextField(null=True, blank=True)
    amniotic_fluid = models.TextField(null=True, blank=True)
    complications = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Ultrasound Report for {self.antenatal_card.name} on {self.ultrasound_date}"


class Prescription(models.Model):
    patient = models.ForeignKey(User, related_name='prescriptions', on_delete=models.CASCADE)  # Links to the registered patient
    doctor = models.ForeignKey(User, related_name='prescribed_by', on_delete=models.CASCADE)  # Links to the doctor who prescribed
    disease_condition = models.CharField(max_length=255)  # Disease or condition the patient is being treated for
    prescription_date = models.DateField(default=now)  # Date the prescription was made   
    follow_up_date = models.DateField(null=True, blank=True)  # Latest date when the patient should have this checked    
    extra_information = models.TextField(null=True, blank=True)  # Any additional information about the prescription
    cleared = models.BooleanField(default=False)  # Whether the prescription has been cleared or not
    cleared_date = models.DateTimeField(null=True, blank=True)  # Date when the prescription was cleared

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.patient.username} prescribed by {self.doctor.username} for {self.disease_condition}"

class Medication(models.Model):
    """
    Model to handle the medications within a prescription.
    Links to a Prescription and stores dosage, medication name, and prescription date.
    """
    prescription = models.ForeignKey(Prescription, related_name='medications', on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=255)  # Medication prescribed
    dosage = models.TextField()  # Dosage instructions
    prescription_date = models.DateField(default=now)  # Date the medication was prescribed

    def __str__(self):
        return f"{self.medication_name} prescribed on {self.prescription_date}"

 
class Emergency(models.Model):
    antenatal_card = models.ForeignKey(
        AntenatalCard, on_delete=models.CASCADE, related_name='emergencies'
    )  # Links to the patient’s antenatal card
    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='reported_emergencies'
    )
    emergency_type = models.TextField(null=True, blank=True)  # Open text field for emergency type
    description = models.TextField(null=True, blank=True)  # Additional details about the emergency
    reported_at = models.DateTimeField(default=now)  # Time the emergency was reported
    action_taken = models.TextField(null=True, blank=True)  # What was done in response to the emergency
    resolved = models.BooleanField(default=False)  # Whether the emergency has been resolved
    resolved_at = models.DateTimeField(null=True, blank=True)  # When the emergency was resolved

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Emergency for {self.antenatal_card.name} reported on {self.reported_at.strftime('%Y-%m-%d %H:%M')}"
