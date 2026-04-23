import pytest

from calculator.models import CartItem, Currency, Money


class TestMoney:
    def test_init_negative_amount_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            Money(-1, Currency.EUR)

    def test_validation_add(self):
        with pytest.raises(ValueError, match="Currency mismatch"):
            Money(100, Currency.EUR) + Money(100, Currency.PLN)

    def test_validation_sub(self):
        with pytest.raises(ValueError, match="Currency mismatch"):
            Money(100, Currency.EUR) - Money(100, Currency.PLN)

    def test_validation_gt(self):
        with pytest.raises(ValueError, match="Currency mismatch"):
            Money(100, Currency.EUR) > Money(100, Currency.PLN)

    def test_add(self):
        result = Money(100, Currency.EUR) + Money(200, Currency.EUR)
        assert result == Money(300, Currency.EUR)

    def test_sub(self):
        result = Money(200, Currency.EUR) - Money(100, Currency.EUR)
        assert result == Money(100, Currency.EUR)

    def test_mul(self):
        result = Money(100, Currency.EUR) * 3
        assert result == Money(300, Currency.EUR)

    def test_gt(self):
        assert Money(200, Currency.EUR) > Money(100, Currency.EUR)
        assert not Money(100, Currency.EUR) > Money(200, Currency.EUR)

    def test_ge(self):
        assert Money(200, Currency.EUR) >= Money(100, Currency.EUR)
        assert Money(100, Currency.EUR) >= Money(100, Currency.EUR)

    def test_lt(self):
        assert Money(100, Currency.EUR) < Money(200, Currency.EUR)
        assert not Money(200, Currency.EUR) < Money(100, Currency.EUR)

    def test_le(self):
        assert Money(100, Currency.EUR) <= Money(200, Currency.EUR)
        assert Money(200, Currency.EUR) <= Money(200, Currency.EUR)

    def test_zero(self):
        z = Money.zero(Currency.EUR)
        assert z == Money(0, Currency.EUR)


class TestCartItem:
    def test_init_empty_code_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            CartItem("", Money(10, Currency.EUR), 1)

    def test_init_zero_quantity_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            CartItem("X", Money(10, Currency.EUR), 0)

    def test_init_negative_quantity_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            CartItem("X", Money(10, Currency.EUR), -1)
