from django.db import models
from accounts.models import User
from django.utils.timezone import now

class AntenatalCard(models.Model):
    """
    This model represents the main antenatal card record created once per pregnancy.
    It contains personal details, pregnancy history, medical history, and social information.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the registered patient
    health_unit = models.CharField(max_length=255)  # Health facility name
    reg_no = models.CharField(max_length=100, unique=True)  # Unique registration number
    name = models.CharField(max_length=255)  # Patient's full name
    nin = models.CharField(max_length=20, unique=True, null=True, blank=True)  # National ID Number
    phone_no = models.CharField(max_length=15)  
    age = models.IntegerField()  
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

    # Next of Kin
    next_of_kin_name = models.CharField(max_length=255)  
    next_of_kin_phone = models.CharField(max_length=15)  
    next_of_kin_relationship = models.CharField(max_length=100)  
    next_of_kin_address = models.TextField()  

    # Pregnancy History
    gravida = models.IntegerField()  # Number of pregnancies
    para = models.IntegerField()  # Number of deliveries after 28 weeks
    abortions = models.IntegerField()  # Number of pregnancy losses before 28 weeks

    # Present Pregnancy
    presenting_complaints = models.TextField(null=True, blank=True)  
    first_day_of_lnmp = models.DateField()  # Last Normal Menstrual Period
    edd = models.DateField()  # Estimated Due Date
    weeks_of_amenorrhea = models.IntegerField()  # Number of weeks since last period
    complications_of_pregnancy = models.TextField(null=True, blank=True)  
    hospitalization = models.BooleanField(default=False)  
    hospitalization_reason = models.TextField(null=True, blank=True)  

    # Created At Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updates when modified

    def __str__(self):
        return f"Antenatal Card for {self.name} ({self.reg_no})"

# ----------------------- SEPARATE TABLES FOR TABULAR DATA -----------------------

class PreviousObstetricHistory(models.Model):
    """
    Stores the details of previous pregnancies, linked to the antenatal card.
    Multiple records can be added over time.
    """
    antenatal_card = models.ForeignKey(AntenatalCard, on_delete=models.CASCADE, related_name="previous_obstetric_history")
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Who entered the record
    pregnancy_year = models.IntegerField()
    abortions_below_12_weeks = models.IntegerField()
    abortions_above_12_weeks = models.IntegerField()
    premature_births = models.IntegerField()
    full_term_deliveries = models.IntegerField()
    delivery_type = models.CharField(max_length=255)  # e.g. Normal, C-section
    place_of_delivery = models.CharField(max_length=255)
    third_stage_complications = models.TextField(null=True, blank=True)
    puerperium = models.TextField(null=True, blank=True)
    baby_alive = models.BooleanField(default=True)
    stillbirth_or_nnd = models.BooleanField(default=False)
    baby_sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    birth_weight = models.FloatField()
    immunization_status = models.CharField(max_length=255)
    baby_health_condition = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=now)  # Timestamp when entry was made

    def __str__(self):
        return f"Previous Pregnancy Record ({self.pregnancy_year}) for {self.antenatal_card.name}"


class AntenatalProgressExamination(models.Model):
    """
    Stores antenatal progress examination data per visit.
    A patient may have multiple examination records.
    """
    antenatal_card = models.ForeignKey(AntenatalCard, on_delete=models.CASCADE, related_name="progress_examinations")
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Who entered the record
    visit_date = models.DateField(default=now)  # Date of the visit
    fundal_height = models.FloatField()
    presentation = models.CharField(max_length=255)
    fetal_heart_rate = models.IntegerField()
    varicose_or_oedema = models.CharField(max_length=255, null=True, blank=True)
    urine_test_results = models.TextField(null=True, blank=True)
    iron_folic_acid_pills = models.IntegerField(null=True, blank=True)
    complaints_and_remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=now)  # Timestamp when entry was made

    def __str__(self):
        return f"Antenatal Progress for {self.antenatal_card.name} on {self.visit_date}"


class UltrasoundReport(models.Model):
    """
    Stores ultrasound reports per visit.
    A patient may have multiple ultrasound reports during pregnancy.
    """
    antenatal_card = models.ForeignKey(AntenatalCard, on_delete=models.CASCADE, related_name="ultrasound_reports")
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Who entered the record
    ultrasound_date = models.DateField(default=now)
    gestational_age = models.IntegerField(null=True, blank=True)
    placenta_details = models.TextField(null=True, blank=True)
    amniotic_fluid = models.TextField(null=True, blank=True)
    complications = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=now)  # Timestamp when entry was made

    def __str__(self):
        return f"Ultrasound Report for {self.antenatal_card.name} on {self.ultrasound_date}"
