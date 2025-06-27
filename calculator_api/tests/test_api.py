import pytest
from rest_framework.test import APIClient
from django.urls import reverse

client = APIClient()


@pytest.mark.parametrize("payload,expected_status,expected_fields", [
    # Valid case
    (
        {
            "instrument": "v75",
            "account_balance": 1000,
            "entry_price": 500.0,
            "stop_price": 495.0,
            "risk_percent": 1
        },
        200,
        {"lot", "pips", "risk"}  # expected keys in response
    ),

    # Invalid instrument
    (
        {
            "instrument": "invalid_code",
            "account_balance": 1000,
            "entry_price": 500.0,
            "stop_price": 495.0,
            "risk_percent": 1
        },
        400,
        {"instrument"}
    ),

    # Risk too high
    (
        {
            "instrument": "v75",
            "account_balance": 1000,
            "entry_price": 500.0,
            "stop_price": 495.0,
            "risk_percent": 150
        },
        400,
        {"risk_percent"}
    ),

    # Negative balance
    (
        {
            "instrument": "v75",
            "account_balance": -50,
            "entry_price": 500.0,
            "stop_price": 495.0,
            "risk_percent": 1
        },
        400,
        {"account_balance"}
    ),

    # Entry price equal to stop price
    (
        {
            "instrument": "v75",
            "account_balance": 1000,
            "entry_price": 500.0,
            "stop_price": 500.0,
            "risk_percent": 1
        },
        400,
        {"stop_price"}
    )
])
def test_calculate_parametrized(payload, expected_status, expected_fields):
    url = reverse('calculate')
    response = client.post(url, payload, format='json')

    assert response.status_code == expected_status

    if expected_status == 200:
        # Make sure all expected fields are in the response
        assert all(field in response.data for field in expected_fields)
    else:
        # Make sure at least one of the expected error fields is present
        assert any(field in response.data for field in expected_fields)


def test_get_instruments_list():
    url = reverse('instruments')
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) > 0

    instrument = response.data[0]
    assert "code" in instrument
    assert "name" in instrument
    assert "min_lot" in instrument
