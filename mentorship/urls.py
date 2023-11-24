# 3rd Party Imports
from django.urls import path

# Local imports
from .views import (
    request_mentorship, 
    pending_requests, 
    cancel_request,
    accept_request,
    get_mentees,
    get_mentors,
    get_mentorships,
    get_tasks,
    change_mentorship_status,
    change_task_status,
    create_task,
    cancel_meeting,
    create_meeting,
)

urlpatterns = [
    path('request_mentorship/', request_mentorship, name="request_mentorship"),
    path('pending_requests/', pending_requests, name="pending_requests"),
    path('cancel_request/', cancel_request, name="cancel_request"),
    path('accept_request/', accept_request, name="accept_request"),
    path('get_mentees/', get_mentees, name="get_mentees"),
    path('get_mentors/', get_mentors, name="get_mentors"),
    path('get_mentorships/', get_mentorships, name="get_mentorships"),
    path('change_mentorship_status/', change_mentorship_status, name="change_mentorship_status"),
    path('get_tasks/', get_tasks, name="get_tasks"),
    path('change_task_status/', change_task_status, name="change_task_status"),
    path('create_task/', create_task, name="create_task"),
    path('cancel_meeting/', cancel_meeting, name="cancel_meeting"),
    path('create_meeting/', create_meeting, name="create_meeting"),
]