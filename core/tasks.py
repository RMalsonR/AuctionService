from celery import shared_task
from .flows import SendEmailFlow, CloseAuction


@shared_task
def auction_usages(subject: str, message: str, from_email: str, to_emails: list):
    flow = SendEmailFlow(subject, message, from_email, to_emails)
    flow.run()
    return None


@shared_task
def close_auction(auction_id: int):
    flow = CloseAuction(auction_id)
    flow.run()
    return None
