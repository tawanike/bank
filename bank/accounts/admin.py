from django.contrib import admin
from bank.accounts.models import Account

class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)