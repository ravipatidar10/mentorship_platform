# 3rd Party Import
from django.contrib import admin

# Local Import
from .models import Mentor, Research, ResearchDetails
# Register your models here.

admin.site.register(Mentor)
admin.site.register(Research)
admin.site.register(ResearchDetails)
