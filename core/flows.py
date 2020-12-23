from django.core.mail import send_mail

from .models import Auction
from AuctionService.settings import EMAIL_HOST


class SendEmailFlow(object):
    def __init__(self, subject: str, message: str, from_email: str, to_emails: list):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.to_emails = to_emails

    def run(self):
        send_mail(self.subject, self.message, self.from_email, self.to_emails)


class CloseAuction(object):
    def __init__(self, auction_id: int):
        self.auction_id = auction_id

    def run(self):
        auction = Auction.objects.get(id=self.auction_id)
        auction.is_active = False
        auction.save()
        to_emails = list(set(auction.all_bet.values_list('user__email', flat=True)))
        if to_emails:
            subject = 'Auction is end'
            winner = str(auction.all_bets.last().user)
            message = 'Hi!\nYou received this email, because auction that you interested in CLOSED!\n' \
                      'The winner is {0}.\n We will wait for you for another auctions'.format(winner)
            from_email = EMAIL_HOST
            send_flow = SendEmailFlow(subject, message, from_email, to_emails)
            send_flow.run()
