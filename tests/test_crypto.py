"""
Unit Tests for Crypto Module

Tests the encryption and decryption functionality for private keys.

Run with:
    pytest tests/test_crypto.py -v
"""

import os
import sys
import pytest
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.crypto import (
    KeyManager,
    verify_private_key,
    generate_random_private_key,
    CryptoError,
    InvalidPasswordError
)


class TestKeyManager:
    """Tests for KeyManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = KeyManager()
        self.test_key = "0x" + "a" * 64  # Valid 32-byte key
        self.test_password = "secure_password_123"

    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypt/decrypt produces original key."""
        encrypted = self.manager.encrypt(self.test_key, self.test_password)
        decrypted = self.manager.decrypt(encrypted, self.test_password)

        assert decrypted == self.test_key

    def test_encrypt_without_0x_prefix(self):
        """Test encryption with key without 0x prefix."""
        key_without_prefix = "a" * 64
        encrypted = self.manager.encrypt(key_without_prefix, self.test_password)
        decrypted = self.manager.decrypt(encrypted, self.test_password)

        assert decrypted == "0x" + key_without_prefix

    def test_invalid_password_raises(self):
        """Test that wrong password raises InvalidPasswordError."""
        encrypted = self.manager.encrypt(self.test_key, self.test_password)

        with pytest.raises(InvalidPasswordError):
            self.manager.decrypt(encrypted, "wrong_password")

    def test_invalid_encrypted_data_raises(self):
        """Test that corrupted data raises CryptoError."""
        encrypted = {
            "version": 1,
            "salt": "invalid_base64!!!",
            "encrypted": "invalid_data"
        }

        with pytest.raises(CryptoError):
            self.manager.decrypt(encrypted, self.test_password)

    def test_empty_key_raises(self):
        """Test that empty key raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            self.manager.encrypt("", self.test_password)

    def test_short_password_raises(self):
        """Test that short password raises ValueError."""
        with pytest.raises(ValueError, match="at least 8 characters"):
            self.manager.encrypt(self.test_key, "short")

    def test_invalid_key_format_raises(self):
        """Test that invalid key format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid private key format"):
            self.manager.encrypt("not_hexadecimal", self.test_password)

    def test_encrypted_data_contains_required_fields(self):
        """Test that encrypted data has all required fields."""
        encrypted = self.manager.encrypt(self.test_key, self.test_password)

        assert "version" in encrypted
        assert "salt" in encrypted
        assert "encrypted" in encrypted
        assert encrypted["version"] == 1

    def test_save_and_load_file(self):
        """Test saving and loading from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_key.json")

            # Save
            self.manager.encrypt_and_save(
                self.test_key,
                self.test_password,
                filepath
            )

            assert os.path.exists(filepath)

            # Verify file permissions are restrictive
            mode = os.stat(filepath).st_mode & 0o777
            assert mode == 0o600, "File should have 0o600 permissions"

            # Load
            manager2 = KeyManager()
            decrypted = manager2.load_and_decrypt(self.test_password, filepath)

            assert decrypted == self.test_key

    def test_file_not_found_raises(self):
        """Test that missing file raises FileNotFoundError."""
        manager = KeyManager()

        with pytest.raises(FileNotFoundError):
            manager.load_and_decrypt(self.test_password, "/nonexistent/path")

    def test_generate_new_salt(self):
        """Test that generate_new_salt creates different salt."""
        salt1 = self.manager.salt
        self.manager.generate_new_salt()
        salt2 = self.manager.salt

        assert salt1 != salt2


class TestVerifyPrivateKey:
    """Tests for verify_private_key function."""

    def test_valid_key_with_prefix(self):
        """Test validation of valid key with 0x prefix."""
        key = "0x" + "a" * 64
        is_valid, result = verify_private_key(key)

        assert is_valid is True
        assert result == key

    def test_valid_key_without_prefix(self):
        """Test validation of valid key without prefix."""
        key = "a" * 64
        is_valid, result = verify_private_key(key)

        assert is_valid is True
        assert result == "0x" + key

    def test_invalid_length(self):
        """Test that wrong length key fails."""
        is_valid, result = verify_private_key("0x" + "a" * 32)

        assert is_valid is False
        assert "64 hex characters" in result

    def test_invalid_characters(self):
        """Test that non-hex characters fail."""
        is_valid, result = verify_private_key("0x" + "gggg" * 16)

        assert is_valid is False
        assert "invalid characters" in result

    def test_empty_string(self):
        """Test that empty string fails."""
        is_valid, result = verify_private_key("")

        assert is_valid is False


class TestGenerateRandomPrivateKey:
    """Tests for generate_random_private_key function."""

    def test_generates_valid_key(self):
        """Test that generated key is valid."""
        key = generate_random_private_key()

        assert key.startswith("0x")
        assert len(key) == 66  # 0x + 64 hex chars

        is_valid, _ = verify_private_key(key)
        assert is_valid is True

    def test_generates_unique_keys(self):
        """Test that multiple calls generate unique keys."""
        key1 = generate_random_private_key()
        key2 = generate_random_private_key()

        assert key1 != key2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
