from django.db import models
from enrollments.models import Enrollment

class Invoice(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Invoice #{self.id}"

