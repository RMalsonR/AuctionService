from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import User, Auction, Bet


class UserSerializer(ModelSerializer):
    initials = serializers.SerializerMethodField()

    def get_initials(self, obj):
        return str(obj)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'sur_name', 'email', 'initials')


class PureUserSerializer(ModelSerializer):
    initials = serializers.SerializerMethodField()

    def get_initials(self, obj):
        return str(obj)

    class Meta:
        model = User
        fields = ('id', 'email', 'initials')


class BetSerializer(serializers.ModelSerializer):
    user = PureUserSerializer(many=False)

    class Meta:
        model = Bet
        fields = ('id', 'user', 'size', 'created_at')


class AuctionDetailSerializer(ModelSerializer):
    owner = UserSerializer(many=False)
    bets = BetSerializer(source='all_bets', many=True)

    class Meta:
        model = Auction
        fields = '__all__'
        read_only_fields = ['actual_price']


class AuctionListSerializer(ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, many=False)

    def create(self, validated_data):
        owner_id = validated_data.pop('owner_id')
        validated_data['owner'] = owner_id
        validated_data['actual_price'] = validated_data['start_price']
        return super(AuctionListSerializer, self).create(validated_data)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if datetime.now() > attrs['expire_at']:
            raise ValidationError('`expire_at` attribute must be greater than now datetime')
        return attrs

    class Meta:
        model = Auction
        fields = ('id', 'owner', 'owner_id', 'name', 'description', 'start_price',
                  'price_step', 'actual_price', 'created_at', 'expire_at', 'is_active')
        read_only_fields = ['actual_price']


class PlaceBetSerializer(serializers.Serializer):
    bet_owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text='Bet owner id'
    )
    auction_id = serializers.PrimaryKeyRelatedField(
        queryset=Auction.objects.filter(is_active=True),
        help_text='Auction id'
    )
    size = serializers.IntegerField(
        min_value=1,
        help_text='Bet size'
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        auction = attrs['auction_id']
        bet_size_minimum = auction.actual_price + auction.price_step
        if bet_size_minimum > attrs['size']:
            raise ValidationError('Bet size must be greater than {0}'.format(bet_size_minimum))
        return attrs



