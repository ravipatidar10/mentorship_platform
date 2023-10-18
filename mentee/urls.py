from django.urls import path
from .views import dashboard, find_mentor

urlpatterns = [
    path('dashboard/', dashboard, name="mentee_dashboard"),
    path('find_mentor/', find_mentor, name="find_mentor"),
]