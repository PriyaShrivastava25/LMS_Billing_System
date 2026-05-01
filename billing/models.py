from django.db import models
from enrollments.models import Enrollment

class Invoice(models.Model):
    enrollment = models.ForeignKey(
    'enrollments.Enrollment',
    on_delete=models.CASCADE,
    related_name='invoice'
)
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    PAYMENT_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Pending')

    def __str__(self):
        return f"Invoice {self.id}"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id}"
