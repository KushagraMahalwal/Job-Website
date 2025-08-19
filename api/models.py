from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    apply_by = models.ManyToManyField("api.User", blank =True, related_name="applied_jobs")
    posted_by = models.ForeignKey("api.User", on_delete=models.CASCADE, null = True, blank = True, related_name ="posted_jobs")

    def __str__(self):
        return self.title