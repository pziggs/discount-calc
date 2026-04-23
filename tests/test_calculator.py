import pytest

from calculator.calculator import DiscountCalculator
from calculator.discounts import FixedDiscount, PercentageDiscount, VolumeDiscount
from calculator.models import Currency, Money

from .test_data import BREAD_1, BUTTER_2, EGGS_3, MILK_4, CHOCOLATE_5


class TestDiscountCalculator:
    def test_calculate_total_empty_cart_raises(self):
        calc = DiscountCalculator([])
        with pytest.raises(ValueError, match="The cart is empty"):
            calc.calculate_total([])

    def test_calculate_total_currency_mismatch_raises(self):
        calc = DiscountCalculator([])
        with pytest.raises(ValueError, match="Multiple currencies"):
            calc.calculate_total(
                [
                    BUTTER_2,
                    CHOCOLATE_5,
                ]
            )

    def test_calculate_total_no_discounts(self):
        calc = DiscountCalculator([])
        assert calc.calculate_total([EGGS_3, MILK_4]) == Money(250, Currency.EUR)

    def test_calculate_total_fixed_discount_applied(self):
        discounts = [FixedDiscount(Money(5, Currency.EUR), applicable_codes={"BREAD"})]
        calc = DiscountCalculator(discounts)

        assert calc.calculate_total([BREAD_1]) == Money(5, Currency.EUR)

    def test_calculate_total_percentage_discount_applied(self):
        discounts = [PercentageDiscount(10, applicable_codes={"BUTTER", "MILK"})]
        calc = DiscountCalculator(discounts)
        assert calc.calculate_total([BUTTER_2, MILK_4]) == Money(
            18 * 2 + 36 * 4, Currency.EUR
        )

    def test_calculate_total_volume_discount_applied(self):
        discounts = [
            VolumeDiscount(
                2, Money(10, Currency.EUR), applicable_codes={"BREAD", "EGGS", "MILK"}
            )
        ]
        calc = DiscountCalculator(discounts)
        cart = [BREAD_1, BUTTER_2, EGGS_3, MILK_4]

        assert calc.calculate_total(cart) == Money(10 + 40 + 80 + 150, Currency.EUR)

    def test_calculate_total_best_discount_per_line(self):
        discounts = [
            FixedDiscount(Money(10, Currency.EUR), applicable_codes={"BUTTER"}),
            PercentageDiscount(10, applicable_codes={"BUTTER"}),
            FixedDiscount(Money(10, Currency.EUR), applicable_codes={"MILK"}),
            PercentageDiscount(50, applicable_codes={"MILK"}),
        ]
        calc = DiscountCalculator(discounts)
        cart = [BUTTER_2, MILK_4]

        assert calc.calculate_total(cart) == Money(20 + 80, Currency.EUR)

    def test_calculate_total_best_discount_to_all_products(self):
        discounts = [PercentageDiscount(50), FixedDiscount(Money(15, Currency.EUR))]
        calc = DiscountCalculator(discounts)
        cart = [BREAD_1, BUTTER_2, EGGS_3, MILK_4]

        assert calc.calculate_total(cart) == Money(0 + 10 + 45 + 80, Currency.EUR)
