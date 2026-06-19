from django.contrib import admin
from .models import Trade


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = [
        'ticket', 'symbol', 'direction',
        'lot_size', 'open_price', 'profit',
        'status', 'open_time'
    ]
    list_filter = ['status', 'direction', 'symbol']
    search_fields = ['ticket', 'symbol']
    ordering = ['-open_time']

from .models import AccountSnapshot

@admin.register(AccountSnapshot)
class AccountSnapshotAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'environment', 'balance', 'equity', 'updated_at']