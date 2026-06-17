from django.db import models


class Trade(models.Model):

    DIRECTION_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    ]

    # Identity
    ticket        = models.BigIntegerField(unique=True, help_text="MT5 trade ticket number")
    symbol        = models.CharField(max_length=20, help_text="e.g. EURUSD, XAUUSD")

    # Trade details
    direction     = models.CharField(max_length=4, choices=DIRECTION_CHOICES)
    lot_size      = models.DecimalField(max_digits=10, decimal_places=2)
    open_price    = models.DecimalField(max_digits=20, decimal_places=5)
    close_price   = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    stop_loss     = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    take_profit   = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)

    # Result
    profit        = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    status        = models.CharField(max_length=6, choices=STATUS_CHOICES, default='OPEN')

    # Timestamps
    open_time     = models.DateTimeField()
    close_time    = models.DateTimeField(null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-open_time']
        verbose_name = 'Trade'
        verbose_name_plural = 'Trades'

    def __str__(self):
        return f"{self.direction} {self.symbol} | Ticket #{self.ticket} | {self.status}"