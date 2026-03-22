"""notifications/email.py — Email dispatch for order confirmations and alerts.

exports: send_confirmation(order_id: int) -> None | send_alert(msg: str) -> None
used_by: views/checkout.py -> checkout_view
rules:   Emails are async — enqueue to job queue, never send synchronously in request.
         Must include unsubscribe link per CAN-SPAM compliance.
agent:   deepseek-v3 | deepseek | 2026-03-14 | Initial email templates.
"""


def send_confirmation(order_id: int) -> None:
    """Send order confirmation email.

    Rules: Must be async (enqueue). Include order total and line items.
    """
    pass
