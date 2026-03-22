"""models/order.py — Order persistence and state machine.

exports: create_order(data: dict) -> Order | confirm_order(order_id: int) -> None
used_by: forms/order_form.py -> validate_order [cascade]
rules:   Order states: draft -> confirmed -> paid -> shipped. No state skipping.
         confirm_order MUST call inventory.deduct_stock() — never deduct at creation time.
agent:   claude-opus-4 | anthropic | 2026-03-12 | Initial order model.
         gemini-2.5-flash | google | 2026-03-18 | Added soft-delete for cancelled orders.
"""


def create_order(data: dict):
    """Create a draft order from validated data.

    Rules: Initial state must be 'draft'. Never deduct stock here.
    """
    pass


def confirm_order(order_id: int) -> None:
    """Confirm an order and deduct inventory.

    Rules: Must call deduct_stock AFTER payment confirmation, not before.
    """
    pass
