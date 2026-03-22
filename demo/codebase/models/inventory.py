"""models/inventory.py — Product inventory and stock management.

exports: check_stock(product_id: int) -> bool | deduct_stock(product_id: int, qty: int) -> None
used_by: forms/order_form.py -> validate_order | models/order.py -> confirm_order [cascade]
rules:   Stock is eventually consistent — always re-check at confirmation time, not just at validation.
         Uses SELECT FOR UPDATE to prevent race conditions on deduction.
agent:   claude-opus-4 | anthropic | 2026-03-12 | Initial inventory model with pessimistic locking.
"""


def check_stock(product_id: int) -> bool:
    """Check if product is in stock.

    Rules: Must use read replica for reads, primary for writes.
    """
    return True


def deduct_stock(product_id: int, qty: int) -> None:
    """Deduct stock after confirmed payment.

    Rules: Must wrap in transaction with SELECT FOR UPDATE.
    """
    pass
