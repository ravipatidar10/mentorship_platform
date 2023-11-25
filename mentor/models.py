# 3rd Party Import
from django.db import models
from django.contrib.auth.models import User


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    researches = models.ManyToManyField("Research", through="ResearchDetails")

    def __str__(self):
        return self.user.username + " (mentor)"


class Research(models.Model):
    research_area = models.CharField(max_length=500, default=None, blank=True, null=True)

    def __str__(self):
        return self.research_area
    

class ResearchDetails(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return self.mentor.user.username + "-" + self.research.research_area