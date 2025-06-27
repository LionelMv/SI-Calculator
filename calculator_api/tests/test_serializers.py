import pytest
from calculator_api.serializers import CalculatorInputSerializer


# Parametrized valid cases
@pytest.mark.parametrize("data,expected_lot", [
    (
        {
            "instrument": "v75",
            "account_balance": 1000.0,
            "entry_price": 500.0,
            "stop_price": 490.0,
            "risk_percent": 2
        },
        0.001
    ),
    (
        {
            "instrument": "v50",
            "account_balance": 2000,
            "entry_price": 1200,
            "stop_price": 1190,
            "risk_percent": 1
        },
        4
    )
])
def test_valid_inputs(data, expected_lot):
    serializer = CalculatorInputSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["lowest_lot"] == expected_lot


# Parametrized invalid numeric values
@pytest.mark.parametrize("field,value", [
    ("account_balance", -100),
    ("account_balance", 0),
    ("entry_price", 0),
    ("stop_price", 0),
    ("risk_percent", 0),
    ("risk_percent", 150),
])
def test_numeric_validation_errors(field, value):
    data = {
        "instrument": "v75",
        "account_balance": 1000,
        "entry_price": 500,
        "stop_price": 490,
        "risk_percent": 1
    }
    data[field] = value

    serializer = CalculatorInputSerializer(data=data)
    assert not serializer.is_valid()
    assert field in serializer.errors


# Invalid instrument check (one or more cases)
@pytest.mark.parametrize("instrument", ["", "invalid_code", "BTCUSD"])
def test_invalid_instrument_fails(instrument):
    data = {
        "instrument": instrument,
        "account_balance": 1000,
        "entry_price": 500,
        "stop_price": 490,
        "risk_percent": 1
    }
    serializer = CalculatorInputSerializer(data=data)
    assert not serializer.is_valid()
    # Could be either field error or validation error
    assert "instrument" in serializer.errors or "__all__" in serializer.errors


'''
# Alternative non-DRY Tests
def test_valid_input_passes():
    data = {
        "instrument": "v75",
        "account_balance": 1000.0,
        "entry_price": 500.0,
        "stop_price": 490.0,
        "risk_percent": 2.0
    }
    serializer = CalculatorInputSerializer(data=data)
    assert serializer.is_valid()
    validated = serializer.validated_data
    assert validated["lowest_lot"] == 0.001  # based on constants
    assert validated["instrument"] == "v75"


def test_invalid_instrument_fails():
    data = {
        "instrument": "invalid_index",
        "account_balance": 1000,
        "entry_price": 500,
        "stop_price": 490,
        "risk_percent": 1
    }
    serializer = CalculatorInputSerializer(data=data)
    assert not serializer.is_valid()
    assert "instrument" in serializer.errors or "__all__" in serializer.errors


def test_negative_account_balance_fails():
    data = {
        "instrument": "v75",
        "account_balance": -100,
        "entry_price": 500,
        "stop_price": 490,
        "risk_percent": 1
    }
    serializer = CalculatorInputSerializer(data=data)
    assert not serializer.is_valid()
    assert "account_balance" in serializer.errors


def test_risk_percent_too_high():
    data = {
        "instrument": "v75",
        "account_balance": 1000,
        "entry_price": 500,
        "stop_price": 490,
        "risk_percent": 150  # Invalid, max is 100
    }
    serializer = CalculatorInputSerializer(data=data)
    assert not serializer.is_valid()
    assert "risk_percent" in serializer.errors
'''
