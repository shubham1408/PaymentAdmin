import datetime
from django.contrib import admin, messages
from django.db.models import Sum, F, Q
from paynow.models import Wallet, Transaction
from .models import CREDIT, WITHDRAW, SEND, REQUEST
from .forms import PayUserWalletForm


class WalletAdmin(admin.ModelAdmin):
    
    fields = ['user','wallet_address','balance']
    list_display = ('id', 'user', 'total_money_addition', 'balance', 
        'total_money_paid', 'total_money_recieved')
    search_fields = ['id', 'user','wallet_address', 'balance']
    current_month_range = datetime.datetime.now()

    
    """
    Total money addition, Total Money paid, 
    Total money recieved functions implemented in
    queryset function to reduces numbber of queries
    for each object
    """
    def get_queryset(self, request):
        queryset = super(WalletAdmin, self).get_queryset(request)
        
        total_money_addition = Transaction.objects.values('user_id').annotate(
            txn_amount_addition=Sum('txn_amount')).filter(
            txn_type=CREDIT, 
            added_on__month=self.current_month_range.month)
        self.total_money_addition_dict = {}
        for obj_add in total_money_addition:
            self.total_money_addition_dict.update({
                obj_add.get('user_id'):  obj_add.get('txn_amount_addition')})

        
        total_money_paid = Transaction.objects.values('user_id').annotate(
            txn_amount_paid=Sum('txn_amount')).filter(
            ~Q(reciever=F('user')),
            added_on__month=self.current_month_range.month,
            txn_type=SEND)
        self.total_money_paid_dict = {}
        for obj_paid in total_money_paid:
            self.total_money_paid_dict.update({
                obj_paid.get('user_id'):  obj_paid.get(
                    'txn_amount_paid')})

        
        total_money_recieved = Transaction.objects.values(
            'reciever_id').annotate(
            txn_amount_recieved=Sum('txn_amount')).filter(
            ~Q(reciever=F('user')),
            added_on__month=self.current_month_range.month,
            txn_type=SEND)
        self.total_money_recieved_dict = {}
        for obj_recieved in total_money_recieved:
            self.total_money_recieved_dict.update({
                obj_recieved.get('reciever_id'): obj_recieved.get(
                    'txn_amount_recieved')})
       
        return queryset

    
    """
    Function to return total money added in current month
    """
    def total_money_addition(self, obj):
        return self.total_money_addition_dict.get(obj.user.id)
        # return obj._total_money_addition
    total_money_addition.allow_tags = True
    total_money_addition.short_description = (
        'Total money added in current month')


    """
    Function to return total money paid in current month
    """
    def total_money_paid(self, obj):
        return self.total_money_paid_dict.get(obj.user.id)
    total_money_paid.allow_tags = True
    total_money_paid.short_description = (
        'Total money paid to other users for current month')


    """
    Function to return total money recieved in current month
    """
    def total_money_recieved(self, obj):
        return self.total_money_recieved_dict.get(obj.user.id)
        return obj._total_money_recieved
    total_money_recieved.allow_tags = True
    total_money_recieved.short_description = (
        'Total money recieved from other users for current month')


    """
    Delete Permission not allowed
    """
    def has_delete_permission(self, request, obj=None):
        return False

    
    """
    Transaction related logic implemented here
    """
    def save_model(self, request, obj, form, change):
        if 'balance' in form.changed_data:
            object_present = self.model.objects.filter(id=obj.id)
            if change:
                txn_amount = obj.balance - object_present.first().balance
                object_present.first().balance = obj.balance
                object_present.first().save()
            else:
                txn_amount = obj.balance  
            txn_data = {
                'user': form.cleaned_data['user'], 'txn_type': CREDIT,
                'txn_amount': txn_amount, 'reciever': form.cleaned_data['user']
            }
            Transaction.objects.create(**txn_data)
            messages.info(request, "Transaction Intiated")
        super(WalletAdmin, self).save_model(request, obj, form, change)



"""
This is a proxy model for Wallet
which is used for ppaying money 
from onse user to another
"""
class PayAnotherUserWallet(Wallet):
    class Meta:
        proxy = True



"""
Admin Class used for paying money 
from one user to another
"""
class PayUserWalletAdmin(WalletAdmin):

    fields = ['user', 'send_amount', 'send_to']
    form = PayUserWalletForm

    def save_model(self, request, obj, form, change):
        send_user_wallet = Wallet.objects.get(user=form.cleaned_data['user'])
        if send_user_wallet.balance < form.cleaned_data['send_amount']:
            messages.info(request, "Not Enough Balance")
            return
        reciever_wallet = Wallet.objects.get(
            user=form.cleaned_data['send_to'])
        reciever_wallet.balance = reciever_wallet.balance + form.cleaned_data['send_amount']
        send_user_wallet.balance = send_user_wallet.balance - form.cleaned_data['send_amount']
        reciever_wallet.save()
        send_user_wallet.save()
        txn_data = {
            'user': form.cleaned_data['user'],
            'txn_type': SEND,
            'txn_amount': form.cleaned_data['send_amount'], 
            'reciever': form.cleaned_data['send_to']
        }
        Transaction.objects.create(**txn_data)
        messages.info(request, "Transaction Successfull")
    
    def get_queryset(self, request):
        return self.model.objects.filter(~Q(user = request.user))

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



"""
Transaction logs maintained here
"""
class TransactionAdmin(admin.ModelAdmin):

    fields = ['user','txn_type','txn_amount','reciever']
    list_display = ('user','txn_type','txn_amount','reciever')
    search_fields = ['user','txn_type','txn_amount','reciever']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Wallet, WalletAdmin)
admin.site.register(PayAnotherUserWallet, PayUserWalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
