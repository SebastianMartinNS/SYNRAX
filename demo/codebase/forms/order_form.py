"""forms/order_form.py — Order validation and cart-to-order transformation.

exports: validate_order(cart_data: dict) -> Order | build_line_items(cart: list) -> list
used_by: views/checkout.py -> checkout_view [cascade] | notifications/email.py -> send_confirmation
rules:   Totals in cents, never float. Must call models.inventory.check_stock() before confirming.
         Discount codes capped at 50% of total — enforce BEFORE creating order.
agent:   deepseek-v3 | deepseek | 2026-03-10 | Initial order form.
         gemini-2.5-flash | google | 2026-03-15 | Added discount validation, missed stock check integration.
"""


def validate_order(cart_data: dict):
    """Validate and transform a cart into an order.

    Rules: MUST check inventory before confirming. Reject if any item out of stock.
    """
    pass


def build_line_items(cart: list) -> list:
    """Build line items from a shopping cart.

    Rules: Each line item must include unit_price_cents and quantity.
    """
    return []
