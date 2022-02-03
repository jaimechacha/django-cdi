from django.contrib import admin
from .models import (
     Assistance, CVitae, Teacher, Student, LegalRepresentative, StudentMedicalRecord
)

admin.site.register([
    Assistance, CVitae, Teacher, Student, LegalRepresentative, StudentMedicalRecord
])
