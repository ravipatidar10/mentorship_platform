from django.urls import path
from .views import (
    request_mentorship, 
    pending_requests, 
    cancel_request,
    accept_request,
    get_mentees,
    get_mentors
)

urlpatterns = [
    path('request_mentorship/', request_mentorship, name="request_mentorship"),
    path('pending_requests/', pending_requests, name="pending_requests"),
    path('cancel_request/', cancel_request, name="cancel_request"),
    path('accept_request/', accept_request, name="accept_request"),
    path('get_mentees/', get_mentees, name="get_mentees"),
    path('get_mentors/', get_mentors, name="get_mentors"),
]