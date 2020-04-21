from django.contrib.auth.models import User
from django.db.models import Q
from django import forms
from .models import Wallet


class PayUserWalletForm(forms.ModelForm):

    from_user = forms.ModelChoiceField(queryset=User.objects.all())
    send_to = forms.ModelChoiceField(queryset=User.objects.all())
    send_amount = forms.IntegerField()

    class Meta:
        model = Wallet
        exclude = ['added_on', 'modified_on']
    