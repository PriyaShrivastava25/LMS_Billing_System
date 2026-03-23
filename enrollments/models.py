from django.db import models
from django.contrib.auth.models import User
from resources.models import Course
from django.apps import apps

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    # Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Course = models.ForeignKey('resources.Course', on_delete=models.CASCADE, null=True, blank=True)

    # enrolled_at = models.DateTimeField(auto_now_add=True)
    # status = models.CharField(max_length=20, default='Active')

    enrolled_on = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default="Pending")


    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            # Reduce seats
            if self.Course.available_seats > 0:
                self.Course.available_seats -= 1
                self.Course.save()

            # Dynamically get Invoice model
            Invoice = apps.get_model('billing', 'Invoice')

            gst = (self.Course.price * 18) / 100
            total = self.Course.price + gst

            Invoice.objects.create(
                enrollment=self,
                total_amount=total
            )

    def __str__(self):
        return f"{self.student.username} - {self.Course.title}"
