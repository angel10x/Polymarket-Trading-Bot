"""
Unit Tests for Utils Module

Tests helper functions for common operations.

Run with:
    pytest tests/test_utils.py -v
"""

import os
import sys
import pytest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import (
    validate_address,
    validate_private_key,
    format_price,
    format_usdc,
    get_env,
    truncate_address,
    truncate_token_id,
)


class TestValidateAddress:
    """Tests for validate_address function."""

    def test_valid_address(self):
        """Test valid Ethereum address."""
        assert validate_address("0x1234567890123456789012345678901234567890") is True

    def test_valid_address_uppercase(self):
        """Test valid address with uppercase letters."""
        assert validate_address("0xABCDEF1234567890ABCDEF1234567890ABCDEF12") is True

    def test_invalid_no_prefix(self):
        """Test address without 0x prefix."""
        assert validate_address("1234567890123456789012345678901234567890") is False

    def test_invalid_too_short(self):
        """Test address that's too short."""
        assert validate_address("0x1234") is False

    def test_invalid_too_long(self):
        """Test address that's too long."""
        assert validate_address("0x12345678901234567890123456789012345678901234") is False

    def test_invalid_characters(self):
        """Test address with invalid characters."""
        assert validate_address("0xGGGG567890123456789012345678901234567890") is False

    def test_empty_string(self):
        """Test empty string."""
        assert validate_address("") is False

    def test_none(self):
        """Test None value."""
        assert validate_address(None) is False


class TestValidatePrivateKey:
    """Tests for validate_private_key function."""

    def test_valid_key_with_prefix(self):
        """Test valid key with 0x prefix."""
        key = "0x" + "a" * 64
        is_valid, result = validate_private_key(key)
        assert is_valid is True
        assert result == key

    def test_valid_key_without_prefix(self):
        """Test valid key without 0x prefix."""
        key = "a" * 64
        is_valid, result = validate_private_key(key)
        assert is_valid is True
        assert result == "0x" + key

    def test_normalizes_to_lowercase(self):
        """Test that result is lowercase."""
        key = "A" * 64
        is_valid, result = validate_private_key(key)
        assert is_valid is True
        assert result == "0x" + "a" * 64

    def test_invalid_too_short(self):
        """Test key that's too short."""
        is_valid, result = validate_private_key("0x" + "a" * 32)
        assert is_valid is False
        assert "64" in result

    def test_invalid_characters(self):
        """Test key with invalid characters."""
        is_valid, result = validate_private_key("0x" + "g" * 64)
        assert is_valid is False
        assert "invalid" in result.lower()

    def test_empty_string(self):
        """Test empty string."""
        is_valid, result = validate_private_key("")
        assert is_valid is False
        assert "empty" in result.lower()


class TestFormatPrice:
    """Tests for format_price function."""

    def test_basic_price(self):
        """Test basic price formatting."""
        result = format_price(0.65)
        assert "0.65" in result
        assert "65%" in result

    def test_zero_price(self):
        """Test zero price."""
        result = format_price(0.0)
        assert "0.00" in result
        assert "0%" in result

    def test_one_price(self):
        """Test 100% price."""
        result = format_price(1.0)
        assert "1.00" in result
        assert "100%" in result

    def test_custom_decimals(self):
        """Test custom decimal places."""
        result = format_price(0.6543, decimals=3)
        assert "0.654" in result


class TestFormatUsdc:
    """Tests for format_usdc function."""

    def test_basic_amount(self):
        """Test basic USDC formatting."""
        result = format_usdc(10.5)
        assert "$10.50" in result
        assert "USDC" in result

    def test_large_amount(self):
        """Test large amount."""
        result = format_usdc(1000.00)
        assert "$1000.00" in result

    def test_small_amount(self):
        """Test small amount."""
        result = format_usdc(0.01)
        assert "$0.01" in result


class TestGetEnv:
    """Tests for get_env function."""

    def test_existing_variable(self):
        """Test getting existing environment variable."""
        os.environ["POLY_TEST_VAR"] = "test_value"
        try:
            result = get_env("TEST_VAR")
            assert result == "test_value"
        finally:
            del os.environ["POLY_TEST_VAR"]

    def test_missing_variable(self):
        """Test getting missing variable returns default."""
        result = get_env("NONEXISTENT_VAR", "default")
        assert result == "default"

    def test_empty_default(self):
        """Test empty default."""
        result = get_env("NONEXISTENT_VAR")
        assert result == ""


class TestTruncateAddress:
    """Tests for truncate_address function."""

    def test_basic_truncation(self):
        """Test basic address truncation."""
        address = "0x1234567890123456789012345678901234567890"
        result = truncate_address(address)
        assert result == "0x123456...567890"

    def test_custom_chars(self):
        """Test custom character count."""
        address = "0x1234567890123456789012345678901234567890"
        result = truncate_address(address, chars=4)
        assert result == "0x1234...7890"

    def test_short_address(self):
        """Test short address not truncated."""
        address = "0x1234"
        result = truncate_address(address)
        assert result == address

    def test_empty_address(self):
        """Test empty address."""
        result = truncate_address("")
        assert result == ""


class TestTruncateTokenId:
    """Tests for truncate_token_id function."""

    def test_basic_truncation(self):
        """Test basic token ID truncation."""
        token = "123456789012345678901234567890"
        result = truncate_token_id(token)
        assert result == "12345678..."

    def test_short_token(self):
        """Test short token not truncated."""
        token = "12345"
        result = truncate_token_id(token)
        assert result == token

    def test_custom_chars(self):
        """Test custom character count."""
        token = "123456789012345678901234567890"
        result = truncate_token_id(token, chars=4)
        assert result == "1234..."


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
