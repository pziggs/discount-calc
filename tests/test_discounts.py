import pytest

from calculator.discounts import FixedDiscount, PercentageDiscount, VolumeDiscount
from calculator.models import Currency, Money

from .test_data import BREAD_1, BUTTER_2, EGGS_3, MILK_4, CHOCOLATE_5


class TestFixedDiscount:
    def test_init_negative_amount_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            FixedDiscount(Money(-5, Currency.EUR))

    def test_is_applicable_valid_code(self):
        d = FixedDiscount(Money(10, Currency.EUR), applicable_codes={"MILK"})
        assert d.is_applicable(MILK_4) is True

    def test_is_applicable_invalid_code(self):
        d = FixedDiscount(Money(10, Currency.EUR), applicable_codes={"MILK"})
        assert d.is_applicable(BUTTER_2) is False

    def test_is_applicable_valid_no_codes(self):
        d = FixedDiscount(Money(10, Currency.EUR))
        assert d.is_applicable(EGGS_3) is True

    def test_is_applicable_invalid_currency(self):
        d = FixedDiscount(Money(10, Currency.EUR))
        assert d.is_applicable(CHOCOLATE_5) is False

    def test_calculate_amount_times_quantity(self):
        d = FixedDiscount(Money(10, Currency.EUR))
        assert d.calculate(EGGS_3) == Money(30, Currency.EUR)

    def test_calculate_discount_higher_than_item_total(self):
        d = FixedDiscount(Money(100, Currency.EUR))
        assert d.calculate(MILK_4) == Money(160, Currency.EUR)


class TestPercentageDiscount:
    def test_init_negative_percentage_raises(self):
        with pytest.raises(ValueError, match="must be between"):
            PercentageDiscount(-10)

    def test_init_over_100_raises(self):
        with pytest.raises(ValueError, match="must be between"):
            PercentageDiscount(101)

    def test_is_applicable_valid_code(self):
        d = PercentageDiscount(10, applicable_codes={"BUTTER"})
        assert d.is_applicable(BUTTER_2) is True

    def test_is_applicable_invalid_code(self):
        d = PercentageDiscount(10, applicable_codes={"BUTTER"})
        assert d.is_applicable(MILK_4) is False

    def test_is_applicable_valid_no_codes(self):
        d = PercentageDiscount(10)
        assert d.is_applicable(BREAD_1) is True

    def test_calculate(self):
        d = PercentageDiscount(10)
        assert d.calculate(BUTTER_2) == Money(4, Currency.EUR)

    def test_calculate_rounds_down(self):
        d = PercentageDiscount(33)
        assert d.calculate(MILK_4) == Money(52, Currency.EUR)

    def test_calculate_0_percent(self):
        d = PercentageDiscount(0)
        assert d.calculate(BREAD_1) == Money(0, Currency.EUR)

    def test_calculate_100_percent(self):
        d = PercentageDiscount(100)
        assert d.calculate(BUTTER_2) == Money(40, Currency.EUR)


class TestVolumeDiscount:
    def test_init_negative_threshold_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            VolumeDiscount(-1, Money(10, Currency.EUR))

    def test_init_negative_amount_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            VolumeDiscount(5, Money(-10, Currency.EUR))

    def test_is_applicable_valid_code(self):
        d = VolumeDiscount(0, Money(10, Currency.EUR), applicable_codes={"BUTTER"})
        assert d.is_applicable(BUTTER_2) is True

    def test_is_applicable_invalid_code(self):
        d = VolumeDiscount(0, Money(10, Currency.EUR), applicable_codes={"BUTTER"})
        assert d.is_applicable(MILK_4) is False

    def test_is_applicable_valid_no_codes(self):
        d = VolumeDiscount(0, Money(10, Currency.EUR))
        assert d.is_applicable(BREAD_1) is True

    def test_is_applicable_quantity_below_threshold(self):
        d = VolumeDiscount(3, Money(5, Currency.EUR))
        assert d.is_applicable(BUTTER_2) is False

    def test_is_applicable_quantity_at_threshold(self):
        d = VolumeDiscount(3, Money(5, Currency.EUR))
        assert d.is_applicable(EGGS_3) is True

    def test_is_applicable_quantity_above_threshold(self):
        d = VolumeDiscount(3, Money(5, Currency.EUR))
        assert d.is_applicable(MILK_4) is True

    def test_is_applicable_invalid_currency(self):
        d = VolumeDiscount(5, Money(500, Currency.EUR))
        assert d.is_applicable(CHOCOLATE_5) is False

    def test_calculate_flat_amount(self):
        d = VolumeDiscount(2, Money(50, Currency.EUR))
        assert d.calculate(EGGS_3) == Money(50, Currency.EUR)

    def test_calculate_discount_higher_than_item_total(self):
        d = VolumeDiscount(2, Money(500, Currency.EUR))
        assert d.calculate(MILK_4) == Money(160, Currency.EUR)
