from abc import ABC, abstractmethod

from .models import CartItem, Money


class Discount(ABC):
    @abstractmethod
    def is_applicable(self, item: CartItem) -> bool: ...

    @abstractmethod
    def calculate(self, item: CartItem) -> Money: ...


class FixedDiscount(Discount):
    def __init__(self, amount: Money, applicable_codes: set[str] | None = None):
        if amount.amount < 0:
            raise ValueError(
                f"Fixed discount amount cannot be negative: {amount.amount}"
            )
        self.amount = amount
        self.applicable_codes = applicable_codes

    def is_applicable(self, item: CartItem) -> bool:
        if item.price.currency != self.amount.currency:
            return False
        if self.applicable_codes is None:
            return True
        return item.code in self.applicable_codes

    def calculate(self, item: CartItem) -> Money:
        total_price = item.price * item.quantity
        discount = self.amount * item.quantity
        if discount > total_price:
            return total_price
        return discount


class PercentageDiscount(Discount):
    def __init__(self, percentage: int, applicable_codes: set[str] | None = None):
        if not 0 <= percentage <= 100:
            raise ValueError(f"Percentage must be between 0 and 100: {percentage}")
        self.percentage = percentage
        self.applicable_codes = applicable_codes

    def is_applicable(self, item: CartItem) -> bool:
        if self.applicable_codes is None:
            return True
        return item.code in self.applicable_codes

    def calculate(self, item: CartItem) -> Money:
        per_product = item.price.amount * self.percentage // 100
        return Money(per_product * item.quantity, item.price.currency)


class VolumeDiscount(Discount):
    def __init__(
        self,
        threshold: int,
        amount: Money,
        applicable_codes: set[str] | None = None,
    ):
        if threshold < 0:
            raise ValueError(
                f"Volume discount threshold cannot be negative: {threshold}"
            )
        if amount.amount < 0:
            raise ValueError(
                f"Volume discount amount cannot be negative: {amount.amount}"
            )
        self.threshold = threshold
        self.amount = amount
        self.applicable_codes = applicable_codes

    def is_applicable(self, item: CartItem) -> bool:
        if item.price.currency != self.amount.currency:
            return False
        if self.applicable_codes is not None and item.code not in self.applicable_codes:
            return False
        return item.quantity >= self.threshold

    def calculate(self, item: CartItem) -> Money:
        line_total = item.price * item.quantity
        if self.amount > line_total:
            return line_total
        return self.amount
