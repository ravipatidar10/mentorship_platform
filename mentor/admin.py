from django.contrib import admin
from .models import Mentor, Research, ResearchDetails
# Register your models here.

admin.site.register(Mentor)
admin.site.register(Research)
admin.site.register(ResearchDetails)
