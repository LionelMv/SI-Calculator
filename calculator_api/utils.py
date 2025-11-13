from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CalculatorContext:
    account_balance: Decimal
    entry_price: Decimal
    stop_price: Decimal
    risk_percent: Decimal
    lowest_allowable_lot: Decimal


def calculate_lot_risk(context: CalculatorContext) -> tuple[Decimal, Decimal, Decimal]:
    # Calculate pip difference
    num_pips = abs(context.entry_price - context.stop_price)

    risk_allowed_amount = context.account_balance * (context.risk_percent / 100)
    lot = risk_allowed_amount / num_pips

    lowest_allowable_lot = Decimal(str(context.lowest_allowable_lot))
    if lot <= lowest_allowable_lot:
        lot = lowest_allowable_lot
        total_risk = num_pips * lowest_allowable_lot
    else:
        total_risk = num_pips * lot

    lot = lot.quantize(Decimal('0.003'))
    total_risk = total_risk.quantize(Decimal('0.02'))

    return lot, num_pips, total_risk
