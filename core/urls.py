from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewSet, AuctionViewSet

app_name = 'core'

router = DefaultRouter()

router.register('users', UserViewSet, basename='core_users')
router.register('auctions', AuctionViewSet, basename='core_auctions')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
