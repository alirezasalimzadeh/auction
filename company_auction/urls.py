from django.urls import path

from company_auction.views import AuctionListView, OfferCreateView, OfferListView, AuctionWinView

urlpatterns = [
    path('auctions-list/', AuctionListView.as_view()),
    path('offer-create/', OfferCreateView.as_view()),
    path('offer-list/', OfferListView.as_view()),
    path('win-list/', AuctionWinView.as_view()),

]
