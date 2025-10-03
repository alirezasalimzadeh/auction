from itertools import count
from django.utils import timezone
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
    # offers = models.ManyToManyField(Offer, related_name='auctions')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="auctions")
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_price = models.PositiveIntegerField()
    current_price = models.PositiveIntegerField(null=True, blank=True)
    final_price = models.PositiveIntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_winner', null=True, blank=True)

    def __str__(self):
        return self.title

    def highest_offer(self):
        return self.auction_offers.order_by('-offer_price').first()

    def last_offer(self):
        return self.auction_offers.order_by('-created_at').first()


    def check_winner(self):
        now = timezone.now()
        last_offer = self.last_offer()
        highest = self.highest_offer()

        if highest and highest.offer_price >= self.final_price:
            self.winner = highest.user
            self.current_price = highest.offer_price
            self.end_time = now
            self.save()
            print("ok")
            return self.winner

        if now >= self.end_time and highest:
            self.winner = highest.user
            self.current_price = highest.offer_price
            self.save()
            print("ok 2")

            return self.winner

        if last_offer and now < self.end_time and (now - last_offer.created_at).total_seconds() >= 24 * 3600:
            self.winner = highest.user
            self.current_price = highest.offer_price
            self.end_time = now
            self.save()
            print("ok 3")

            return self.winner

        return None
