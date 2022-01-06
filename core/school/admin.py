from django.contrib import admin
from .models import (
    Matriculation, MatriculationDetail, PsychologicalOrientation, NoteDetails
)

admin.site.register([
    Matriculation, MatriculationDetail, PsychologicalOrientation, NoteDetails
])
