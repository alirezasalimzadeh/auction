from rest_framework.serializers import ModelSerializer, StringRelatedField
from company_auction.models import Company, Auction, Offer


class AuctionListSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'


class OfferCreateSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = ['auction', 'offer_price']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OfferListSerializer(ModelSerializer):
    user = StringRelatedField()
    auction = StringRelatedField()

    class Meta:
        model = Offer
        fields = ['user', 'auction', 'offer_price']


class AuctionWinSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = "__all__"
