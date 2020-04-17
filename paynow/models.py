from django.db import models
from django.conf import settings

CREDIT = 0
WITHDRAW = 1
SEND = 2
REQUEST = 3

TRANSACTION_CHOICES = (
    (CREDIT, 'Credit'),
    (WITHDRAW, 'Withdraw'),
    (SEND, 'Send'),
    (REQUEST, 'Request')
)

class Wallet(models.Model):
    """
    Wallet Table Respective to each User
    which represents all the information 
    regarding wallet of specifc user
    """
    user=models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, unique=True)
    wallet_address=models.CharField(
        null=False, unique=True, max_length=255)
    balance=models.PositiveIntegerField(default=0)
    added_on=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    """
    Transaction Table which maintains all
    logs respective to each user
    """
    user=models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, related_name='transation_intiated_by')
    txn_type=models.PositiveSmallIntegerField(
        choices=TRANSACTION_CHOICES)
    txn_amount=models.PositiveIntegerField(null=False)
    reciever=models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, related_name='transation_to')
    added_on = models.DateTimeField(auto_now_add=True)
