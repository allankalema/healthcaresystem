# Generated by Django 5.1.6 on 2025-03-14 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_patient_admitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='admitted',
        ),
    ]
