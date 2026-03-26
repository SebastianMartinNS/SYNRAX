"""views/checkout.py — Checkout page handler for cart-to-payment flow.

exports: checkout_view(request) -> HttpResponse
used_by: urls.py -> urlpatterns
rules:   Must validate cart is non-empty before calling forms. Always check user.is_authenticated.
         Never call models directly — delegate to forms layer.
agent:   gemini-2.5-flash | google | 2026-03-15 | Added discount code support.
         claude-opus-4 | anthropic | 2026-03-18 | Fixed empty cart crash, no negative-total check.
"""


def checkout_view(request):
    """Handle checkout page GET/POST.

    Rules: Must verify cart.total > 0 after discount application.
    """
    pass
