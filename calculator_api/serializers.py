from rest_framework import serializers
from .constants import INSTRUMENTS
from decimal import Decimal


class CalculatorInputSerializer(serializers.Serializer):
    instrument = serializers.ChoiceField(choices=list(INSTRUMENTS.keys()))
    account_balance = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.01"))
    entry_price = serializers.DecimalField(
        max_digits=16, decimal_places=5, min_value=Decimal("0.0001"))
    stop_price = serializers.DecimalField(
        max_digits=16, decimal_places=5, min_value=Decimal("0.0001"))
    risk_percent = serializers.DecimalField(
        max_digits=5, decimal_places=2, min_value=Decimal("0.01"),
        max_value=Decimal("100.00"))
    lowest_lot = serializers.DecimalField(
        max_digits=10, decimal_places=3, read_only=True)

    def validate(self, data: dict) -> dict:
        if data["entry_price"] == data["stop_price"]:
            raise serializers.ValidationError({
                "stop_price": "Stop price must be different from entry price."
            })

        instrument = data["instrument"]
        data["lowest_lot"] = Decimal(str(INSTRUMENTS[instrument]))

        return data
