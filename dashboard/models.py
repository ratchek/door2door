from django.contrib.auth.models import User
from django.db import models


class VisitedAddress(models.Model):
    house_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=50)
    visiting_agent = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.house_number + " " + self.street_name
