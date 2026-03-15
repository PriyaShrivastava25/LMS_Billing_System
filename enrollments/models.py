from django.db import models
from django.contrib.auth.models import User
from resources.models import Resource
from django.apps import apps

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            # Reduce seats
            if self.resource.available_seats > 0:
                self.resource.available_seats -= 1
                self.resource.save()

            # Dynamically get Invoice model
            Invoice = apps.get_model('billing', 'Invoice')

            gst = (self.resource.price * 18) / 100
            total = self.resource.price + gst

            Invoice.objects.create(
                enrollment=self,
                total_amount=total
            )

    def __str__(self):
        return f"{self.student.username} - {self.resource.title}"
