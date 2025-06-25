from rest_framework import serializers
from .constants import INSTRUMENTS


class CalculatorInputSerializer(serializers.Serializer):
    instrument = serializers.ChoiceField(choices=list(INSTRUMENTS.keys()))
    account_balance = serializers.FloatField(min_value=0.01)
    entry_price = serializers.FloatField(min_value=0.0001)
    stop_price = serializers.FloatField(min_value=0.0001)
    risk_percent = serializers.FloatField(min_value=0.01, max_value=100)

    def validate(self, data):
        instrument = data['instrument']
        if instrument not in INSTRUMENTS:
            raise serializers.ValidationError("Unknown instrument.")
        data['lowest_lot'] = INSTRUMENTS[instrument]
        return data
