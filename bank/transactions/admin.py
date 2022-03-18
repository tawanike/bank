from django.contrib import admin
from bank.transactions.models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transaction, TransactionAdmin)