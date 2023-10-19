from django.urls import path
from .views import request_mentorship

urlpatterns = [
    path('request_mentorship/', request_mentorship, name="request_mentorship"),
]