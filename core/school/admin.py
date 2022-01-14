from django.contrib import admin
from .models import (
     Assistance, CVitae
)

admin.site.register([
    Assistance, CVitae
])
