from abc import ABC, abstractmethod
from dataclasses import dataclass

from .discounts import Discount
from .models import CartItem, Money


@dataclass(frozen=True)
class DiscountResult:
    base_price: Money
    discount_amount: Money
    final_price: Money
    applied_discount: Discount | None


class CartItemDiscountResolver(ABC):
    def __init__(self, discounts: list[Discount] | None = None):
        self.discounts = discounts or []

    @abstractmethod
    def resolve(self, item: CartItem) -> DiscountResult:
        pass


class CartItemMaxDiscountResolver(CartItemDiscountResolver):
    def resolve(self, item: CartItem) -> DiscountResult:
        max_amount: Money = Money.zero(item.price.currency)
        best_discount: Discount | None = None

        for discount in self.discounts:
            if not discount.is_applicable(item):
                continue
            amount = discount.calculate(item)
            if amount > max_amount:
                max_amount = amount
                best_discount = discount

        total_price = item.price * item.quantity
        return DiscountResult(
            base_price=total_price,
            discount_amount=max_amount,
            final_price=total_price - max_amount,
            applied_discount=best_discount,
        )
