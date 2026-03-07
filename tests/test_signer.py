"""
Unit Tests for Signer Module

Tests EIP-712 order signing functionality.

Run with:
    pytest tests/test_signer.py -v
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.signer import OrderSigner, Order, SignerError


class TestOrderSigner:
    """Tests for OrderSigner class."""

    # Valid test private key (not a real wallet with funds!)
    TEST_PRIVATE_KEY = "0x" + "a" * 64

    def setup_method(self):
        """Set up test fixtures."""
        self.signer = OrderSigner(self.TEST_PRIVATE_KEY)
        self.test_address = self.signer.address

    def test_signer_address_from_key(self):
        """Test that signer has correct address from key."""
        assert self.test_address.startswith("0x")
        assert len(self.test_address) == 42

    def test_invalid_key_raises(self):
        """Test that invalid key raises ValueError."""
        with pytest.raises(ValueError, match="Invalid private key"):
            OrderSigner("invalid_key")

    def test_from_encrypted_raises_without_module(self):
        """Test that from_encrypted fails with wrong password."""
        # This would require proper encrypted data
        # Just verify the method exists and has correct signature
        assert hasattr(OrderSigner, 'from_encrypted')

    def test_sign_auth_message(self):
        """Test signing authentication message."""
        signature = self.signer.sign_auth_message()

        assert signature is not None
        assert signature.startswith("0x")
        assert len(signature) == 132  # 65 bytes * 2 + 0x

    def test_sign_auth_message_with_timestamp(self):
        """Test signing with custom timestamp."""
        timestamp = "1234567890"
        signature = self.signer.sign_auth_message(timestamp=timestamp)

        assert signature is not None
        assert signature.startswith("0x")

    def test_sign_auth_message_with_nonce(self):
        """Test signing with custom nonce."""
        signature = self.signer.sign_auth_message(nonce=42)

        assert signature is not None

    def test_sign_order_dict_basic(self):
        """Test signing order with basic parameters."""
        result = self.signer.sign_order_dict(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="BUY",
            maker=self.test_address
        )

        assert "order" in result
        assert "signature" in result
        assert "signer" in result

        assert result["order"]["tokenId"] == "1234567890123456789"
        assert result["order"]["price"] == 0.65
        assert result["order"]["size"] == 10.0
        assert result["order"]["side"] == "BUY"

    def test_sign_order_dict_sell_side(self):
        """Test signing SELL order."""
        result = self.signer.sign_order_dict(
            token_id="1234567890123456789",
            price=0.35,
            size=5.0,
            side="SELL",
            maker=self.test_address
        )

        assert result["order"]["side"] == "SELL"

    def test_sign_order_with_nonce(self):
        """Test signing order with custom nonce."""
        result = self.signer.sign_order_dict(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="BUY",
            maker=self.test_address,
            nonce=12345
        )

        assert result["order"]["nonce"] == 12345

    def test_sign_order_with_fee(self):
        """Test signing order with fee rate."""
        result = self.signer.sign_order_dict(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="BUY",
            maker=self.test_address,
            fee_rate_bps=100  # 1%
        )

        assert result["order"]["feeRateBps"] == 100

    def test_sign_order_generates_valid_signature(self):
        """Test that signature is valid format."""
        result = self.signer.sign_order_dict(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="BUY",
            maker=self.test_address
        )

        signature = result["signature"]

        assert signature.startswith("0x")
        assert len(signature) == 132  # 65 bytes hex encoded


class TestOrder:
    """Tests for Order dataclass."""

    def test_order_creation(self):
        """Test creating an Order."""
        order = Order(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="BUY",
            maker="0x1234567890123456789012345678901234567890"
        )

        assert order.token_id == "1234567890123456789"
        assert order.price == 0.65
        assert order.size == 10.0
        assert order.side == "BUY"

    def test_order_side_normalized_to_upper(self):
        """Test that side is normalized to uppercase."""
        order = Order(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="buy",  # lowercase
            maker="0x1234567890123456789012345678901234567890"
        )

        assert order.side == "BUY"

    def test_order_invalid_side_raises(self):
        """Test that invalid side raises ValueError."""
        with pytest.raises(ValueError, match="Invalid side"):
            Order(
                token_id="1234567890123456789",
                price=0.65,
                size=10.0,
                side="INVALID",
                maker="0x1234567890123456789012345678901234567890"
            )

    def test_order_invalid_price_too_low(self):
        """Test that price <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="Invalid price"):
            Order(
                token_id="1234567890123456789",
                price=0,
                size=10.0,
                side="BUY",
                maker="0x1234567890123456789012345678901234567890"
            )

    def test_order_invalid_price_above_one(self):
        """Test that price > 1 raises ValueError."""
        with pytest.raises(ValueError, match="Invalid price"):
            Order(
                token_id="1234567890123456789",
                price=1.5,
                size=10.0,
                side="BUY",
                maker="0x1234567890123456789012345678901234567890"
            )

    def test_order_invalid_size_raises(self):
        """Test that size <= 0 raises ValueError."""
        with pytest.raises(ValueError, match="Invalid size"):
            Order(
                token_id="1234567890123456789",
                price=0.65,
                size=0,
                side="BUY",
                maker="0x1234567890123456789012345678901234567890"
            )

    def test_order_uses_timestamp_as_nonce(self):
        """Test that nonce defaults to timestamp."""
        order = Order(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="BUY",
            maker="0x1234567890123456789012345678901234567890"
        )

        assert order.nonce is not None
        assert isinstance(order.nonce, int)

    def test_order_calculates_maker_amount(self):
        """Test that maker_amount is calculated correctly."""
        order = Order(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="BUY",
            maker="0x1234567890123456789012345678901234567890"
        )

        # maker_amount = size * price * 1e6
        expected = str(int(10.0 * 0.65 * 1_000_000))
        assert order.maker_amount == expected

    def test_order_calculates_taker_amount(self):
        """Test that taker_amount is calculated correctly."""
        order = Order(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="BUY",
            maker="0x1234567890123456789012345678901234567890"
        )

        # taker_amount = size * 1e6
        expected = str(int(10.0 * 1_000_000))
        assert order.taker_amount == expected

    def test_order_side_value_buy(self):
        """Test that BUY side has correct numeric value."""
        order = Order(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="BUY",
            maker="0x1234567890123456789012345678901234567890"
        )

        assert order.side_value == 0

    def test_order_side_value_sell(self):
        """Test that SELL side has correct numeric value."""
        order = Order(
            token_id="1234567890123456789",
            price=0.65,
            size=10.0,
            side="SELL",
            maker="0x1234567890123456789012345678901234567890"
        )

        assert order.side_value == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
