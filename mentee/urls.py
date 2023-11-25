# 3rd Party Import
from django.urls import path

# Local Import
from .views import dashboard, find_mentor

urlpatterns = [
    path('dashboard/', dashboard, name="mentee_dashboard"),
    path('find_mentor/', find_mentor, name="find_mentor"),
]