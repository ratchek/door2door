from django.contrib.auth.models import User
from django.db import models


class VisitedAddress(models.Model):
    """
    Represents an address visited by a real estate agent.

    Attributes:
        house_number (CharField): The house number of the visited address.
        street_name (CharField): The street name of the visited address.
        visiting_agent (ForeignKey): Reference to the User model, representing the agent who visited.
        date_of_visit (DateField): The date on which the visit took place.
        knocked (BooleanField): Indicates whether the agent knocked on the door.
        door_opened (BooleanField): Indicates whether someone opened the door.
        owners_available (BooleanField): Indicates whether the owners were available during the visit.
        owners_not_interested (BooleanField): Indicates that the owners were not interested in selling.
        notes (TextField): Additional notes about the visit, can be blank.
    """

    house_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=50)
    visiting_agent = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_visit = models.DateField()
    knocked = models.BooleanField()
    door_opened = models.BooleanField()
    owners_available = models.BooleanField()
    owners_not_interested = models.BooleanField()
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the VisitedAddress instance,
        including house number, street name, visiting agent's username, and date of visit.

        Returns:
            str: A string representation of the visited address.
        """

        return (
            self.house_number
            + " "
            + self.street_name
            + " - "
            + self.visiting_agent.username
            + " - "
            + str(self.date_of_visit)
        )

    def save(self, *args, **kwargs):
        """
        Overridden save method to ensure house number and street name are saved in uppercase.
        """
        # Make sure these get saved as upper case
        self.house_number = self.house_number.upper()
        self.street_name = self.street_name.upper()

        # call the save() method of the parent
        super().save(*args, **kwargs)
