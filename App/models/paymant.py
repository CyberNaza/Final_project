from django.db import models
from ..models import Student, Group



class Month(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Payment(models.Model):
    pay_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.price} for {self.month}"
