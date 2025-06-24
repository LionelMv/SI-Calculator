from rest_framework import serializers

# Your instrument-to-lot map
INSTRUMENTS = {
    'b1000': 0.2, 'b300': 0.1, 'b500': 0.2, 'c1000': 0.2, 'c300': 0.5,
    'c500': 0.2, 'j10': 0.01, 'j100': 0.01, 'j25': 0.01, 'j50': 0.01,
    'j75': 0.01, 'r100': 0.01, 'r200': 0.01, 'si': 0.1,
    'v10(1s)': 0.2, 'v10': 0.3, 'v100(1s)': 0.1, 'v100': 0.2,
    'v200(1s)': 0.02, 'v25(1s)': 0.005, 'v25': 0.5, 'v300(1s)': 1,
    'v50(1s)': 0.005, 'v50': 3, 'v75(1s)': 0.005, 'v75': 0.001,
    'v150(1s)': 0.001, 'v250(1s)': 0.001
}


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
