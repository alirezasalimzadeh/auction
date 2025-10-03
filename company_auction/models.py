from itertools import count

from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Offer(models.Model):
    OFFER_WINNER = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name='auction_offers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_offers')
    offer_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=OFFER_WINNER, default='pending', max_length=10)

    def __str__(self):
        return f'{self.user.username} offered {self.offer_price} on {self.auction.title}'


class Auction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="auctions")
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_price = models.PositiveIntegerField()
    current_price = models.PositiveIntegerField()
    final_price = models.PositiveIntegerField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_winner', null=True, blank=True)

    def __str__(self):
        return self.title
