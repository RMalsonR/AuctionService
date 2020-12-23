from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# from core.tasks import auction_usages, close_auction

from AuctionService.settings import EMAIL_HOST_USER


class User(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name='First name')
    last_name = models.CharField(max_length=150, verbose_name='Last name')
    email = models.EmailField(verbose_name='Email address')
    sur_name = models.CharField(max_length=150, verbose_name='Sur name')

    def __str__(self):
        if self.last_name and self.first_name and self.sur_name:
            return f'{self.last_name} {self.first_name[0]}.{self.sur_name[0]}.'
        return super(User, self).__str__()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Auction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='auctions', verbose_name='Owner')
    name = models.CharField(max_length=256, verbose_name='Auction name')
    description = models.CharField(max_length=1024, verbose_name='Product description')
    start_price = models.PositiveIntegerField(verbose_name='Starting price')
    price_step = models.PositiveIntegerField(verbose_name='Price step')
    actual_price = models.PositiveIntegerField(verbose_name='Actual price')
    created_at = models.DateTimeField(blank=True, auto_created=True, auto_now_add=True,
                                      verbose_name='Date of auction creation')
    expire_at = models.DateTimeField(verbose_name='Expiration date')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='Is active?')

    bets = models.ManyToManyField(User, through='core.Bet')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='all_bets', verbose_name='Bet owner')
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT, related_name='all_bets', verbose_name='Auction')
    size = models.PositiveIntegerField(verbose_name='Bet size')
    created_at = models.DateTimeField(blank=True, auto_created=True, auto_now_add=True,
                                      verbose_name='Date of bet creation')

    class Meta:
        verbose_name = 'Bet'
        verbose_name_plural = 'Bets'


# @receiver(post_save, sender=Auction)
# def post_save_auction_handler(sender, instance, *args, **kwargs):
#     from_email = EMAIL_HOST_USER
#     if instance._state.adding is True:
#         all_emails = User.objects.exclude(id=instance.owner.id).values_list('email', flat=True)
#         subject = 'New Auction!'
#         message = 'Hi!\nYou received this email, because there is good news for you!\n' \
#                   'Someone opened the new auction!\nHurry up! You need to place a bet!'
#         to_emails = all_emails
#         close_auction.apply_async(instance.id, eta=instance.created_at - instance.expire_at)
#     else:
#         if not instance.is_active:
#             return
#         to_emails = list(set(instance.all_bet.values_list('user__email', flat=True)))
#         subject = 'New bet!'
#         message = 'Hi!\nYou received this email, because someone placed a new bet' \
#                   ' in auction that you interested in!\n' \
#                   'Hurry up! You need to place a bet!'
#     if to_emails:
#         auction_usages.delay(subject, message, from_email, to_emails)




