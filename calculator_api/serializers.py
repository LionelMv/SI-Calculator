from rest_framework import serializers
from .constants import INSTRUMENTS


class CalculatorInputSerializer(serializers.Serializer):
    instrument = serializers.ChoiceField(choices=list(INSTRUMENTS.keys()))
    account_balance = serializers.FloatField(min_value=0.01)
    entry_price = serializers.FloatField(min_value=0.0001)
    stop_price = serializers.FloatField(min_value=0.0001)
    risk_percent = serializers.FloatField(min_value=0.01, max_value=100)

    lowest_lot = serializers.FloatField(read_only=True)

    def validate(self, data):
        if data['entry_price'] == data['stop_price']:
            raise serializers.ValidationError({
                "stop_price": "Stop price must be different from entry price."
            })

        data['lowest_lot'] = INSTRUMENTS[data['instrument']]
        return data
