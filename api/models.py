from django.db import models
from django.db import models
from django.contrib.auth.models import User

class job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    apply_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank =True, related_name="applied_jobs")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name ="posted_jobs")

