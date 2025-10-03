from argparse import Action
from datetime import timezone
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from company_auction.models import *
from company_auction.serializer import AuctionListSerializer, OfferCreateSerializer, OfferListSerializer, \
    AuctionWinSerializer


class AuctionListView(ListCreateAPIView):
    queryset = Auction.objects.all().order_by('-start_time')
    serializer_class = AuctionListSerializer


class OfferCreateView(CreateAPIView):
    queryset = Offer.objects.all().order_by('-created_at')
    serializer_class = OfferCreateSerializer


class OfferListView(ListAPIView):
    queryset = Offer.objects.all().order_by('-created_at')
    serializer_class = OfferListSerializer


class AuctionWinView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionWinSerializer

    def get_queryset(self):
        user = self.request.user
        active_auctions = Auction.objects.filter(winner__isnull=True, end_time__lte=timezone.now())
        for auction in active_auctions:
            auction.check_winner()

        return Auction.objects.filter(winner=user)
