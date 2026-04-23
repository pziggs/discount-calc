from .discounts import Discount
from .models import CartItem, Money, Currency
from .resolver import CartItemDiscountResolver, CartItemMaxDiscountResolver


class DiscountCalculator:
    def __init__(
        self,
        discounts: list[Discount],
        resolver: CartItemDiscountResolver | None = None,
    ):
        self.resolver = resolver or CartItemMaxDiscountResolver(discounts)

    def calculate_total(self, items: list[CartItem]) -> Money:
        if not items:
            raise ValueError("The cart is empty")

        currency = self._validate_currency(items)

        total = Money.zero(currency)
        for item in items:
            result = self.resolver.resolve(item)
            total = total + result.final_price

        return total

    def _validate_currency(self, items: list[CartItem]) -> Currency:
        currencies = {item.price.currency for item in items}
        if len(currencies) > 1:
            raise ValueError(f"Multiple currencies in cart not allowed: {currencies}")
        return currencies.pop()
