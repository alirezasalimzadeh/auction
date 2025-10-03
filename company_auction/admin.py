from django.contrib import admin
from company_auction.models import Company, Auction, Offer

# admin.site.register(User)
admin.site.register(Offer)
admin.site.register(Company)
admin.site.register(Auction)
