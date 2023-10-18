from django.db import models
from mentee.models import Mentee
from mentor.models import Mentor, ResearchDetails

# Create your models here.

MENTORSHIP_STATUSES = (
    (1, "pending"),
    (2, "accepted"),
    (3, "rejected"),
)

TASK_STATUSES = (
    (1, "completed"),
    (2, "not_started"),
    (3, "running")
)

class Mentorship(models.Model):
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    status = models.IntegerField(choices=MENTORSHIP_STATUSES)
    research = models.ForeignKey(ResearchDetails, on_delete=models.CASCADE)


class Tasks(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    detail = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.IntegerField(choices=TASK_STATUSES)


class Meeting(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    link = models.URLField()
    time = models.DateTimeField()
