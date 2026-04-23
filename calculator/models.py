from enum import Enum


class Currency(str, Enum):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"


class Money:
    def __init__(self, amount: int, currency: Currency):
        if amount < 0:
            raise ValueError(f"Money amount cannot be negative: {amount}")
        self.amount = amount
        self.currency = currency

    def __add__(self, other: "Money") -> "Money":
        self._validate_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._validate_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: int) -> "Money":
        return Money(self.amount * factor, self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __gt__(self, other: "Money") -> bool:
        self._validate_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        self._validate_currency(other)
        return self.amount >= other.amount

    def _validate_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch {self.currency} != {other.currency}")

    @classmethod
    def zero(cls, currency: Currency) -> "Money":
        return cls(0, currency)


class CartItem:
    def __init__(self, code: str, price: Money, quantity: int):
        if not code:
            raise ValueError("CartItem code cannot be empty")
        if quantity <= 0:
            raise ValueError(f"CartItem quantity must be positive: {quantity}")
        self.code = code
        self.price = price
        self.quantity = quantity
