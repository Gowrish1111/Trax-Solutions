from django.contrib import admin

from .models import Student,Course,Enrollment,Assessment,Grade

# Register your models here.
admin.site.register([Student,Course,Enrollment,Assessment,Grade])