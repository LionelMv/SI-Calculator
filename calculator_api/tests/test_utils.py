import pytest
from decimal import Decimal
from calculator_api.utils import calculate_lot_risk, CalculatorContext


@pytest.mark.parametrize(
    "account_balance, entry_price, stop_price, risk_percent,"
    "lowest_allowable_lot, expected_lot, expected_pips, expected_risk_check",
    [
        # Case 1: Risk too low → minimum lot should be used
        (
            1000,              # account_balance
            571734.33,         # entry_price
            568355.52,         # stop_price
            1,                 # risk_percent
            0.005,             # lowest_allowable_lot
            Decimal("0.005"),  # expected lot (min used)
            3378.81,           # expected pips (rounded)
            "greater_than_1_percent",  # check condition type
        ),
        # Case 2: Risk sufficient → ideal lot should be used
        (
            2000,
            571734.33,
            568355.52,
            1,
            0.005,
            None,              # expected lot is calculated dynamically
            3378.81,
            "matches_risk_percent",
        ),
    ],
)
def test_calculate_lot_risk(
    account_balance: float,
    entry_price: float,
    stop_price: float,
    risk_percent: float,
    lowest_allowable_lot: float,
    expected_lot: Decimal | None,
    expected_pips: float,
    expected_risk_check: str,
) -> None:
    """
    Parametrized test for calculate_lot_risk using CalculatorContext.
    Ensures:
    - when ideal lot < minimum allowable lot, minimum lot is used
    - when risk % supports a higher lot, ideal lot is used
    and risk matches percentage.
    """
    # Build CalculatorContext with Decimal values (avoid float imprecision)
    ctx = CalculatorContext(
        account_balance=Decimal(str(account_balance)),
        entry_price=Decimal(str(entry_price)),
        stop_price=Decimal(str(stop_price)),
        risk_percent=Decimal(str(risk_percent)),
        lowest_allowable_lot=Decimal(str(lowest_allowable_lot)),
    )

    lot, pips, risk = calculate_lot_risk(ctx)

    # pips is returned as Decimal; compare rounded floats
    assert round(float(pips), 2) == pytest.approx(expected_pips, rel=1e-3)

    if expected_lot is not None:
        # Case: minimum lot used
        assert lot == expected_lot
        # risk should be greater than the intended percent amount
        # (1% of account_balance)
        assert float(risk) > float(account_balance * (risk_percent / 100))
    else:
        # Case: ideal lot used, risk should equal the intended percentage
        expected_risk = account_balance * (risk_percent / 100)  # float
        assert round(float(risk), 2) == pytest.approx(expected_risk, rel=1e-3)

        # expected_lot computed using Decimal math and
        # same quantize used in utility
        expected_risk_dec = Decimal(str(expected_risk))
        expected_lot = (expected_risk_dec / pips).quantize(Decimal("0.003"))
        assert lot == expected_lot
