from django.db import models
from django.contrib.auth.models import User
from resources.models import Course
from django.apps import apps


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    enrollment_date = models.DateTimeField(auto_now_add=True)

    PAYMENT_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default='Pending'
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            # Seat check
            if self.course.available_seats <= 0:
                raise ValueError("No seats Available")

           
            super().save(*args, **kwargs)

            # Decrease seat
            self.course.available_seats -= 1
            self.course.save()

            # Invoice create
            Invoice = apps.get_model('billing', 'Invoice')

            gst = (self.course.price * 18) / 100
            total = self.course.price + gst

            Invoice.objects.create(
                enrollment=self,
                base_amount=self.course.price,
                gst_amount=gst,
                total_amount=total
            )

        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
