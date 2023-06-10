from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=15)
    description = models.TextField()
    starting_bid = models.FloatField()
    categories = models.ManyToManyField("Category", related_name="listings")
    created_at = models.DateTimeField(auto_now_add = True)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.title}"

class Category(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="bid")
    amount = models.FloatField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
