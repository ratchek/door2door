from django.contrib.auth.models import User
from django.db import models


class VisitedAddress(models.Model):
    # house_number and street_name are used strictly for naming purposes
    house_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=50)
    visiting_agent = models.ForeignKey(User, on_delete=models.CASCADE)
    building_id = models.IntegerField()
    date_of_visit = models.DateField()
    knocked = models.BooleanField()
    door_opened = models.BooleanField()
    owners_available = models.BooleanField()
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return (
            self.house_number
            + " "
            + self.street_name
            + " - "
            + self.visiting_agent.username
            + " - "
            + str(self.date_of_visit)
        )
