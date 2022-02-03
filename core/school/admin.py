from django.contrib import admin
from .models import (
     Assistance, CVitae, Teacher, Student
)

admin.site.register([
    Assistance, CVitae, Teacher, Student
])
