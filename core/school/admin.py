from django.contrib import admin
from .models import (
    Matriculation, MatriculationDetail, PsychologicalOrientation
)

admin.site.register([
    Matriculation, MatriculationDetail, PsychologicalOrientation
])
