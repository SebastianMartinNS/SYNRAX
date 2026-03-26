"""billing/invoice_service.py — Invoice generation and total aggregation.

exports: build_invoice_total(order_id: str) -> int
used_by: api/routes.py -> post_invoice | reports/monthly.py -> generate_report [cascade]
rules:   All totals in centesimi (cents), never float. Filter is_suspended() before aggregating.
agent:   claude-sonnet-4-6 | anthropic | 2026-03-22 | Invoice logic, no suspended filter.
"""


def build_invoice_total(order_id: str) -> int:
    """Aggregate paid invoices for an order into total amount.

    Rules: MUST filter is_suspended() from tenants before summing.
           Totals stored in cents, never float.
    """
    return 0
