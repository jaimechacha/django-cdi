from django.contrib import admin
from .models import (
     Assistance, CVitae, Teacher
)

admin.site.register([
    Assistance, CVitae, Teacher
])
