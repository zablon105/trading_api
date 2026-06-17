from rest_framework import serializers
from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_ticket(self, value):
        """Ensure ticket number is positive"""
        if value <= 0:
            raise serializers.ValidationError("Ticket number must be positive.")
        return value

    def validate_lot_size(self, value):
        """Ensure lot size is positive"""
        if value <= 0:
            raise serializers.ValidationError("Lot size must be greater than 0.")
        return value