# 3rd Party Import
from django.db import models

# Local Import
from mentee.models import Mentee
from mentor.models import Mentor, ResearchDetails

# Create your models here.

PENDING = 1
ACCEPTED = 2
REJECTED = 3
CANCELLED = 4
WITHDRAW = 5
COMPLETED = 6

MENTORSHIP_STATUSES = (
    (PENDING, "pending"),
    (ACCEPTED, "accepted"),
    (REJECTED, "rejected"),
    (CANCELLED, "cancelled"),
    (WITHDRAW, "withdraw"),
    (COMPLETED, "completed")
)

COMPLETED = 1
NOT_STARTED = 2
RUNNING = 3
CANCELLED = 4

TASK_STATUSES = (
    (COMPLETED, "completed"),
    (NOT_STARTED, "not_started"),
    (RUNNING, "running"),
    (CANCELLED, "cancelled"),
)

class Mentorship(models.Model):
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    status = models.IntegerField(choices=MENTORSHIP_STATUSES, default=PENDING)
    research = models.ForeignKey(ResearchDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.mentor.user.username + "-" + self.mentee.user.username


class Tasks(models.Model):
    title = models.CharField(max_length=250)
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    detail = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.IntegerField(choices=TASK_STATUSES, default=NOT_STARTED)

    def __str__(self):
        return self.detail


class Meeting(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    is_cancelled = models.BooleanField(default=False)
    link = models.URLField()
    time = models.DateTimeField()
