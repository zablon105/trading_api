from rest_framework import serializers
from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_ticket(self, value):
        if value < 0:
            raise serializers.ValidationError("Ticket number cannot be negative.")
        return value

    def validate_lot_size(self, value):
        if value <= 0:
            raise serializers.ValidationError("Lot size must be greater than 0.")
        return value

    def validate_open_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Open price must be greater than 0.")
        return value

from .models import AccountSnapshot


class AccountSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSnapshot
        fields = '__all__'