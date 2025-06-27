import pytest
from decimal import Decimal
from calculator_api.utils import calculate_lot_risk


def test_min_lot_used_when_risk_too_low():
    """
    When the ideal lot size is lower than the instrument's minimum lot size,
    the function should return the minimum lot and a higher than intended risk.
    """
    lot, pips, risk = calculate_lot_risk(
        account_balance=1000,
        entry_price=571734.33,
        stop_price=568355.52,
        risk_percent=1,
        lowest_allowable_lot=0.005
    )

    assert lot == Decimal('0.005')
    assert round(float(pips), 2) == 3378.81
    assert round(float(risk), 2) == round(float(pips) * float(lot), 2)
    assert risk > 10  # because 1% of 1000 is 10


def test_ideal_lot_used_when_risk_sufficient():
    """
    When the risk percent supports a lot size greater than the minimum,
    the ideal lot should be used and the risk should match the intended
    percentage.
    """
    lot, pips, risk = calculate_lot_risk(
        account_balance=2000,
        entry_price=571734.33,
        stop_price=568355.52,
        risk_percent=1,
        lowest_allowable_lot=0.005
    )

    assert round(float(pips), 2) == 3378.81
    expected_risk = 20.00  # 1% of 2000
    assert round(float(risk), 2) == expected_risk

    expected_risk = Decimal(str(expected_risk))
    expected_lot = (expected_risk / pips).quantize(Decimal('0.003'))
    assert lot == expected_lot
