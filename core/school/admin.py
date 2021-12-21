from django.contrib import admin
from .models import (
    StudentMedicalRecord, LegalRepresentative, Student, Family, FamilyGroup,
    Teacher
)

admin.site.register([
    StudentMedicalRecord,
    LegalRepresentative,
    Student,
    Family,
    FamilyGroup,
    Teacher,
])
