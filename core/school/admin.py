from django.contrib import admin
from .models import StudentMedicalRecord, LegalRepresentative, Student, Family, FamilyGroup

# Register your models here.
admin.site.register([
    StudentMedicalRecord,
    LegalRepresentative,
    Student,
    Family,
    FamilyGroup
])
