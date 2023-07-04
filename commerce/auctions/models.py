from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    watchlist = models.OneToOneField("Watchlist", null=True, on_delete= models.SET_NULL, related_name="user")
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=15)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2) 
    categories = models.ManyToManyField("Category", related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True)
    closed = models.BooleanField(default=False, null=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

class Category(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content}"

class Watchlist(models.Model):
    listings = models.ManyToManyField(Listing)