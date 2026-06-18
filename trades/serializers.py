from rest_framework import serializers
from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_ticket(self, value):
        """Accept any positive ticket including large MT5 tickets"""
        if value < 0:
            raise serializers.ValidationError("Ticket number cannot be negative.")
        return value

    def validate_lot_size(self, value):
        """Ensure lot size is a valid trading volume"""
        if value <= 0:
            raise serializers.ValidationError("Lot size must be greater than 0.")
        if value > 100:
            raise serializers.ValidationError("Lot size cannot exceed 100.")
        return value

    def validate_open_price(self, value):
        """Ensure open price is valid"""
        if value <= 0:
            raise serializers.ValidationError("Open price must be greater than 0.")
        return value

    def validate_direction(self, value):
        """Ensure direction is BUY or SELL"""
        if value not in ['BUY', 'SELL']:
            raise serializers.ValidationError("Direction must be BUY or SELL.")
        return value.upper()

    def validate(self, data):
        """Cross-field validation"""
        # Close price must be set if status is CLOSED
        if data.get('status') == 'CLOSED' and not data.get('close_price'):
            raise serializers.ValidationError({
                'close_price': 'Close price is required when status is CLOSED.'
            })

        # Stop loss and take profit sanity check for BUY trades
        if data.get('direction') == 'BUY':
            sl = data.get('stop_loss')
            tp = data.get('take_profit')
            open_price = data.get('open_price')
            if sl and open_price and sl >= float(str(open_price)):
                raise serializers.ValidationError({
                    'stop_loss': 'Stop loss must be below open price for BUY trades.'
                })
            if tp and open_price and tp <= float(str(open_price)):
                raise serializers.ValidationError({
                    'take_profit': 'Take profit must be above open price for BUY trades.'
                })

        return data