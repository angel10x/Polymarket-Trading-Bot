"""
Unit Tests for Bot Module

Tests the TradingBot class and related functionality.

Run with:
    pytest tests/test_bot.py -v
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.bot import TradingBot, OrderResult, NotInitializedError
from src.config import Config, BuilderConfig, ClobConfig


class TestOrderResult:
    """Tests for OrderResult dataclass."""

    def test_from_response_success(self):
        """Test creating OrderResult from successful response."""
        response = {
            "success": True,
            "orderId": "order_123",
            "status": "live"
        }

        result = OrderResult.from_response(response)

        assert result.success is True
        assert result.order_id == "order_123"
        assert result.status == "live"
        assert "successfully" in result.message.lower()

    def test_from_response_failure(self):
        """Test creating OrderResult from failed response."""
        response = {
            "success": False,
            "errorMsg": "Insufficient balance"
        }

        result = OrderResult.from_response(response)

        assert result.success is False
        assert result.message == "Insufficient balance"

    def test_order_result_defaults(self):
        """Test OrderResult default values."""
        result = OrderResult(success=True, message="Test")

        assert result.order_id is None
        assert result.status is None
        assert result.data == {}


class TestTradingBot:
    """Tests for TradingBot class."""

    TEST_PRIVATE_KEY = "0x" + "a" * 64
    TEST_SAFE_ADDRESS = "0x" + "b" * 40

    def test_init_with_config(self):
        """Test initialization with Config object."""
        config = Config(
            safe_address=self.TEST_SAFE_ADDRESS,
            use_gasless=False
        )

        bot = TradingBot(config=config)

        assert bot.config == config
        assert bot.signer is None  # No private key provided

    def test_init_with_private_key(self):
        """Test initialization with private key."""
        bot = TradingBot(
            private_key=self.TEST_PRIVATE_KEY,
            safe_address=self.TEST_SAFE_ADDRESS
        )

        assert bot.signer is not None
        # Signer address is derived from private key, not safe_address
        assert bot.signer.address.startswith("0x")
        assert len(bot.signer.address) == 42

    def test_init_with_partial_params(self):
        """Test initialization with partial parameters."""
        # Should work with just safe_address
        bot = TradingBot(safe_address=self.TEST_SAFE_ADDRESS)

        assert bot.config.safe_address == self.TEST_SAFE_ADDRESS

    def test_is_initialized_without_signer(self):
        """Test is_initialized returns False without signer."""
        bot = TradingBot(safe_address=self.TEST_SAFE_ADDRESS)

        assert bot.is_initialized() is False

    def test_is_initialized_with_signer(self):
        """Test is_initialized returns True with signer."""
        bot = TradingBot(
            private_key=self.TEST_PRIVATE_KEY,
            safe_address=self.TEST_SAFE_ADDRESS
        )

        assert bot.is_initialized() is True

    def test_require_signer_without_signer(self):
        """Test require_signer raises when no signer."""
        bot = TradingBot(safe_address=self.TEST_SAFE_ADDRESS)

        with pytest.raises(NotInitializedError):
            bot.require_signer()

    def test_require_signer_with_signer(self):
        """Test require_signer returns signer when available."""
        bot = TradingBot(
            private_key=self.TEST_PRIVATE_KEY,
            safe_address=self.TEST_SAFE_ADDRESS
        )

        signer = bot.require_signer()
        assert signer is not None
        # Signer address is derived from private key
        assert signer.address.startswith("0x")
        assert len(signer.address) == 42

    def test_config_from_yaml(self, tmp_path):
        """Test loading config from YAML file."""
        config_content = '''
safe_address: "0x1234567890123456789012345678901234567890"
rpc_url: https://polygon-rpc.com
default_token_id: "0xabcdef1234567890"
default_size: 5.0
default_price: 0.65
data_dir: test_credentials
log_level: DEBUG
'''
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        config = Config.load(str(config_file))

        assert config.safe_address == "0x1234567890123456789012345678901234567890"
        assert config.rpc_url == "https://polygon-rpc.com"
        assert config.default_token_id == "0xabcdef1234567890"
        assert config.default_size == 5.0
        assert config.default_price == 0.65
        assert config.data_dir == "test_credentials"
        assert config.log_level == "DEBUG"

    def test_config_with_builder_credentials(self, tmp_path):
        """Test config with Builder credentials enables gasless."""
        config_content = '''
safe_address: "0x1234567890123456789012345678901234567890"
builder:
  api_key: test_key_123
  api_secret: secret_abc
  api_passphrase: passphrase_xyz
'''
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        config = Config.load(str(config_file))

        assert config.use_gasless is True
        assert config.builder.is_configured()

    def test_config_without_builder_credentials(self, tmp_path):
        """Test config without Builder credentials disables gasless."""
        config_content = '''
safe_address: "0x1234567890123456789012345678901234567890"
builder:
  api_key: ""
  api_secret: ""
  api_passphrase: ""
'''
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        config = Config.load(str(config_file))

        assert config.use_gasless is False
        assert config.builder.is_configured() is False

    def test_config_validate_missing_safe_address(self, tmp_path):
        """Test config validation fails without safe_address."""
        config = Config()
        errors = config.validate()

        assert len(errors) > 0
        assert any("safe_address" in error for error in errors)

    def test_config_validate_valid_config(self, tmp_path):
        """Test config validation passes with valid config."""
        config = Config(safe_address=self.TEST_SAFE_ADDRESS)
        errors = config.validate()

        assert len(errors) == 0

    def test_create_order_dict(self):
        """Test creating order dictionary."""
        bot = TradingBot(
            private_key=self.TEST_PRIVATE_KEY,
            safe_address=self.TEST_SAFE_ADDRESS
        )

        order_dict = bot.create_order_dict(
            token_id="1234567890",
            price=0.65,
            size=10.0,
            side="BUY"
        )

        assert order_dict["token_id"] == "1234567890"
        assert order_dict["price"] == 0.65
        assert order_dict["size"] == 10.0
        assert order_dict["side"] == "BUY"

    def test_create_order_dict_side_normalized(self):
        """Test that side is normalized to uppercase."""
        bot = TradingBot(
            private_key=self.TEST_PRIVATE_KEY,
            safe_address=self.TEST_SAFE_ADDRESS
        )

        order_dict = bot.create_order_dict(
            token_id="1234567890",
            price=0.65,
            size=10.0,
            side="buy"
        )

        assert order_dict["side"] == "BUY"


class TestCreateBot:
    """Tests for create_bot convenience function."""

    def test_create_bot_with_config_path(self, tmp_path):
        """Test create_bot with config path."""
        config_content = '''
safe_address: "0x1234567890123456789012345678901234567890"
'''
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        bot = TradingBot(config_path=str(config_file))

        assert bot.config.safe_address == "0x1234567890123456789012345678901234567890"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
