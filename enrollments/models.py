# from django.db import models
# from django.contrib.auth.models import User
# from resources.models import Course
# from django.apps import apps

# class Enrollment(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey('resources.Course', on_delete=models.CASCADE, null=True, blank=True)
#     enrolled_on = models.DateTimeField(auto_now_add=True)
#     payment_status = models.CharField(max_length=20, default="Pending")  

#     def save(self, *args, **kwargs):
#         is_new = self.pk is None
#         super().save(*args, **kwargs)

#         if is_new:
            
#             if self.course.available_seats > 0:
#                 self.course.available_seats -= 1
#                 self.course.save()

            
#             Invoice = apps.get_model('billing', 'Invoice')

#             gst = (self.course.price * 18) / 100
#             total = self.course.price + gst

            
#             Invoice.objects.create(
#                 enrollment=self,
#                 total_amount=total
#             )

#     def __str__(self):
#         return f"{self.student.username} - {self.course.title}"



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
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            if self.course.available_seats > 0:
                self.course.available_seats -= 1
                self.course.save()

            Invoice = apps.get_model('billing', 'Invoice')

            gst = (self.course.price * 18) / 100
            total = self.course.price + gst

            Invoice.objects.create(
                enrollment=self,
                base_amount=self.course.price,
                gst_amount=gst,
                total_amount=total
            )

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
