from calculator import (
    CartItem,
    Currency,
    DiscountCalculator,
    FixedDiscount,
    Money,
    PercentageDiscount,
    VolumeDiscount,
)


def main() -> None:
    discounts = [
        FixedDiscount(
            amount=Money(10, Currency.EUR),
            applicable_codes={"MILK"},
        ),
        PercentageDiscount(
            percentage=50,
            applicable_codes={"BUTTER"},
        ),
        VolumeDiscount(
            threshold=5,
            amount=Money(20, Currency.EUR),
            applicable_codes={"BREAD"},
        ),
    ]

    cart = [
        CartItem(code="BREAD", price=Money(10, Currency.EUR), quantity=1),
        CartItem(code="BUTTER", price=Money(20, Currency.EUR), quantity=2),
        CartItem(code="EGGS", price=Money(30, Currency.EUR), quantity=3),
        CartItem(code="MILK", price=Money(40, Currency.EUR), quantity=4),
    ]

    calculator = DiscountCalculator(discounts)
    total = calculator.calculate_total(cart)

    print("Cart:")
    for item in cart:
        line = item.price.amount * item.quantity
        print(
            f"  {item.code} x{item.quantity} @ {item.price.amount} = {line} {item.price.currency.value}"
        )

    print(f"\nTotal after discounts: {total.amount} {total.currency.value}")


if __name__ == "__main__":
    main()
