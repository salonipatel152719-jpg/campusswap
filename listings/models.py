from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 0 = free
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="listings/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("listing_detail", kwargs={"pk": self.pk})
