from django.contrib import admin
from .models import Account, Destination


class AccountAdmin(admin.ModelAdmin):
    list_display = ('emailid', 'accountid', 'account_name', 'app_secret_token', 'website')
admin.site.register(Account,AccountAdmin)


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('account', 'url', 'http_method', 'headers')
admin.site.register(Destination,DestinationAdmin)