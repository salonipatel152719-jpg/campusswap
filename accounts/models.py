from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "listing")

    def __str__(self):
        return f"{self.user} likes {self.listing}"
