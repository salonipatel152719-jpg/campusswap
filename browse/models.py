from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received", on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.listing}"
