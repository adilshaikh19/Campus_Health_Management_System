from django.db import models
from Crypto.Hash import SHA256
from codecs import encode,decode
from django.utils import timezone
from datetime import date
from datetime import timedelta
from django.utils import timezone

class Doctor(models.Model):
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 100)
    contactNumber = models.CharField(unique = True, max_length = 10)
    email = models.EmailField(unique = True, max_length = 255)
    specialization = models.CharField(max_length = 100)
    passwordHash = models.CharField(max_length = 64)
    emailHash = models.CharField(max_length = 64)

    def __str__(self):
        return "Name : " + self.name + " Address : " + self.address + " Contact : " + self.contactNumber + " Email : " + self.email + " Specialization : " + self.specialization


class Appointment(models.Model):
    appointment_date = models.DateField(default=date.today)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    timeslot = models.CharField(null=True, blank=True, max_length=100)
    reason = models.TextField(default="N/A")  # Set default value to "N/A"
    user_name = models.CharField(max_length=255, default='Unknown')
    user_email = models.EmailField(default="N/A")

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.appointment_date}"

class Patient(models.Model):
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 100)
    contactNumber = models.CharField(max_length = 10)
    email = models.EmailField(unique = True, max_length = 255)
    rollNumber = models.CharField(unique = True, max_length = 8)
    passwordHash = models.CharField(max_length = 64)
    emailHash = models.CharField(max_length = 64)

    def __str__(self):
        return "Name : " + self.name + " Address : " + self.address + " Contact : " + self.contactNumber + " Email : " + self.email

class Prescription(models.Model):
    prescriptionText = models.TextField(max_length = 2000, default = "")
    doctor = models.ForeignKey(Doctor, related_name = "doctorRecords", on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, related_name = "patientRecords", on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    isNew = models.BooleanField(default = True)
    isCompleted = models.BooleanField(default = False)
    symptoms = models.CharField(max_length = 2000)

    def __str__(self):
        return "\nDoctor :" + str(self.doctor) + "\n\nPatient :" + str(self.patient) + "\n\nPrescription : \n\n" + self.prescriptionText + "\n\n"


def passwordHasher(userPassword):
    """Function to return the hash of the password using SHA-256. Input is the password of the user in string."""
    userPassword = userPassword
    SHA256Engine = SHA256.new()
    userPassword = userPassword.encode()
    SHA256Engine.update(userPassword)
    passwordHash = SHA256Engine.digest()
    passwordHash = encode(passwordHash, 'hex')
    passwordHash = decode(passwordHash, 'utf-8')
    return passwordHash


def emailHasher(userEmail):
    """Function to return the hash of the email using SHA-256. Input is the email of the user in string."""
    userEmail = userEmail
    SHA256Engine = SHA256.new()
    userEmail = userEmail.encode()
    SHA256Engine.update(userEmail)
    emailHash = SHA256Engine.digest()
    emailHash = encode(emailHash, 'hex')
    emailHash = decode(emailHash, 'utf-8')
    return emailHash


