from decimal import Decimal


def calculate_lot_risk(account_balance, entry_price, stop_price,
                       risk_percent, lowest_allowable_lot):
    # Calculate pip difference
    num_pips = abs(Decimal(str(entry_price)) - Decimal(str(stop_price)))

    risk_allowed_amount = \
        Decimal(str(account_balance)) * (Decimal(str(risk_percent)) / 100)
    lot = risk_allowed_amount / num_pips

    lowest_allowable_lot = Decimal(str(lowest_allowable_lot))
    if lot <= lowest_allowable_lot:
        lot = lowest_allowable_lot
        total_risk = num_pips * lowest_allowable_lot
    else:
        total_risk = num_pips * lot

    lot = lot.quantize(Decimal('0.003'))
    total_risk = total_risk.quantize(Decimal('0.02'))

    return lot, num_pips, total_risk
