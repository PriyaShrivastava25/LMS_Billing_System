
from django.db import models
from django.contrib.auth.models import User
from resources.models import Resource

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.student.username} - {self.resource.title}"
