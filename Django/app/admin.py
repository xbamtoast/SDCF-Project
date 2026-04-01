from django.contrib import admin
from .models import BaseSubmission, HopeGrantApplication, MidYearReport, EndYearReport

#testing something here
# Register your models here.

#admin.site.register(BaseSubmission)
admin.site.register(HopeGrantApplication)
admin.site.register(MidYearReport)
admin.site.register(EndYearReport)