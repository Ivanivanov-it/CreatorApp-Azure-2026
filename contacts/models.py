from django.db import models

from common.models import TimeStampModel


# Create your models here.

class Contact(TimeStampModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11,null=True,blank=True)
    email = models.EmailField(unique=False,null=False)
    content = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"