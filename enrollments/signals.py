from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Enrollment

@receiver(post_delete, sender=Enrollment)
def restore_seats_on_delete(sender, instance, **kwargs):
    course = instance.course

   
    course.available_seats += 1
    course.save()
