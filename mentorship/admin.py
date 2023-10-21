from django.contrib import admin

from .models import Mentorship, Meeting, Tasks
# Register your models here.

admin.site.register(Mentorship)
admin.site.register(Meeting)
admin.site.register(Tasks)