# from django.db import models

# class Resource(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     total_seats = models.IntegerField()
#     available_seats = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return self.title


