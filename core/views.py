from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins

from core.models import User, Auction, Bet
from .permissions import IsNotOwner

from .serializers import UserSerializer, AuctionDetailSerializer, AuctionListSerializer, PlaceBetSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )


class AuctionViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ['is_active', ]

    def get_permission_classes(self):
        """Not Allow owner to place a bet"""
        if self.action == 'place_a_bet':
            return permissions.AllowAny, IsNotOwner
        return (permissions.AllowAny, )

    def get_permissions(self):
        return [permission() for permission in self.get_permission_classes()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuctionDetailSerializer
        if self.action == 'place_a_bet':
            return PlaceBetSerializer
        return super(AuctionViewSet, self).get_serializer_class()

    @action(methods=['post'], detail=False)
    def place_a_bet(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        auction = data['auction_id']
        bet_owner = data['bet_owner_id']
        Bet.objects.create(user=bet_owner, auction=auction, size=data['size'])
        auction.actual_price = data['size']
        auction.save()
        return Response(data={'success': True}, status=status.HTTP_201_CREATED)

