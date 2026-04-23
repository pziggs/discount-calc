from calculator.discounts import FixedDiscount, PercentageDiscount, VolumeDiscount
from calculator.models import Currency, Money
from calculator.resolver import CartItemMaxDiscountResolver

from .test_data import BREAD_1, BUTTER_2, EGGS_3, MILK_4


class TestCartItemMaxDiscountResolver:
    def test_resolve_no_discounts(self):
        resolver = CartItemMaxDiscountResolver()
        result = resolver.resolve(EGGS_3)

        assert result.base_price == Money(90, Currency.EUR)
        assert result.discount_amount == Money(0, Currency.EUR)
        assert result.final_price == Money(90, Currency.EUR)
        assert result.applied_discount is None

    def test_resolve_no_applicable_discounts(self):
        discounts = [FixedDiscount(Money(10, Currency.EUR), applicable_codes={"MILK"})]
        resolver = CartItemMaxDiscountResolver(discounts)
        result = resolver.resolve(BUTTER_2)

        assert result.base_price == Money(40, Currency.EUR)
        assert result.discount_amount == Money(0, Currency.EUR)
        assert result.final_price == Money(40, Currency.EUR)
        assert result.applied_discount is None

    def test_resolve_single_applicable_discount(self):
        d = FixedDiscount(Money(10, Currency.EUR), applicable_codes={"MILK"})
        resolver = CartItemMaxDiscountResolver([d])
        result = resolver.resolve(MILK_4)

        assert result.base_price == Money(160, Currency.EUR)
        assert result.discount_amount == Money(40, Currency.EUR)
        assert result.final_price == Money(120, Currency.EUR)
        assert result.applied_discount == d

    def test_resolve_picks_best_discount(self):
        d1 = FixedDiscount(Money(10, Currency.EUR))
        d2 = PercentageDiscount(50)
        resolver = CartItemMaxDiscountResolver([d1, d2])
        result = resolver.resolve(MILK_4)

        assert result.base_price == Money(160, Currency.EUR)
        assert result.discount_amount == Money(80, Currency.EUR)
        assert result.final_price == Money(80, Currency.EUR)
        assert result.applied_discount == d2

    def test_resolve_not_applicable_discount_excluded(self):
        d1 = VolumeDiscount(5, Money(100, Currency.EUR))
        d2 = FixedDiscount(Money(5, Currency.EUR))
        resolver = CartItemMaxDiscountResolver([d1, d2])
        result = resolver.resolve(BREAD_1)

        assert result.base_price == Money(10, Currency.EUR)
        assert result.discount_amount == Money(5, Currency.EUR)
        assert result.final_price == Money(5, Currency.EUR)
        assert result.applied_discount == d2
