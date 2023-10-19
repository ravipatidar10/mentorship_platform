from django.db import models
from mentee.models import Mentee
from mentor.models import Mentor, ResearchDetails

# Create your models here.

PENDING = 1
ACCEPTED = 2
REJECTED = 3

MENTORSHIP_STATUSES = (
    (PENDING, "pending"),
    (ACCEPTED, "accepted"),
    (REJECTED, "rejected"),
)

COMPLETED = 1
NOT_STARTED = 2
RUNNING = 3

TASK_STATUSES = (
    (COMPLETED, "completed"),
    (NOT_STARTED, "not_started"),
    (RUNNING, "running")
)

class Mentorship(models.Model):
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    status = models.IntegerField(choices=MENTORSHIP_STATUSES, default=PENDING)
    research = models.ForeignKey(ResearchDetails, on_delete=models.CASCADE)


class Tasks(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    detail = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.IntegerField(choices=TASK_STATUSES, default=NOT_STARTED)


class Meeting(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    link = models.URLField()
    time = models.DateTimeField()
