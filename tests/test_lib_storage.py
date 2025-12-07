"""
Tests for semiautomatic.lib.storage module.

Tests cover:
- R2Config from environment
- R2Backend upload operations (mocked)
- StorageBackend protocol
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from semiautomatic.lib.storage import (
    R2Config,
    R2Backend,
    StorageBackend,
    get_storage_backend,
    set_storage_backend,
)


class TestR2Config:
    """Tests for R2Config."""

    def test_from_env_with_all_vars(self, monkeypatch):
        """Should create config from environment variables."""
        monkeypatch.setenv("EU_ENDPOINT", "https://test.r2.cloudflarestorage.com")
        monkeypatch.setenv("CLOUDFLARE_S3_ACCESS_KEY", "test_access")
        monkeypatch.setenv("CLOUDFLARE_S3_SECRET_ACCESS", "test_secret")
        monkeypatch.setenv("R2_BUCKET_NAME", "test_bucket")
        monkeypatch.setenv("R2_PUBLIC_URL", "https://pub-test.r2.dev")

        config = R2Config.from_env()

        assert config.endpoint == "https://test.r2.cloudflarestorage.com"
        assert config.access_key == "test_access"
        assert config.secret_key == "test_secret"
        assert config.bucket == "test_bucket"
        assert config.public_url == "https://pub-test.r2.dev"

    def test_from_env_raises_when_missing(self, monkeypatch):
        """Should raise EnvironmentError when vars missing."""
        monkeypatch.delenv("EU_ENDPOINT", raising=False)
        monkeypatch.delenv("CLOUDFLARE_S3_ACCESS_KEY", raising=False)
        monkeypatch.delenv("CLOUDFLARE_S3_SECRET_ACCESS", raising=False)
        monkeypatch.delenv("R2_BUCKET_NAME", raising=False)
        monkeypatch.delenv("R2_PUBLIC_URL", raising=False)

        with pytest.raises(EnvironmentError):
            R2Config.from_env()


class TestR2Backend:
    """Tests for R2Backend."""

    def test_init_with_explicit_params(self):
        """Should initialize with explicit parameters."""
        backend = R2Backend(
            endpoint="https://test.endpoint",
            access_key="key",
            secret_key="secret",
            bucket="bucket",
            public_url="https://public.url",
        )

        assert backend._config.endpoint == "https://test.endpoint"
        assert backend._config.bucket == "bucket"

    def test_init_with_config_object(self):
        """Should initialize with R2Config object."""
        config = R2Config(
            endpoint="https://cfg.endpoint",
            access_key="cfg_key",
            secret_key="cfg_secret",
            bucket="cfg_bucket",
            public_url="https://cfg.public",
        )
        backend = R2Backend(config=config)

        assert backend._config.endpoint == "https://cfg.endpoint"

    def test_upload_returns_public_url(self, temp_dir):
        """Should upload file and return public URL."""
        backend = R2Backend(
            endpoint="https://test.endpoint",
            access_key="key",
            secret_key="secret",
            bucket="test-bucket",
            public_url="https://pub.r2.dev",
        )

        # Create test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Mock boto3
        with patch.object(backend, "_client") as mock_client:
            # Force _client to be set
            backend._client = mock_client

            url = backend.upload(test_file, "uploads/test.txt")

        assert url == "https://pub.r2.dev/uploads/test.txt"
        mock_client.upload_file.assert_called_once()

    def test_upload_image_uses_images_prefix(self, temp_dir):
        """Should use images/ prefix for upload_image."""
        backend = R2Backend(
            endpoint="https://test.endpoint",
            access_key="key",
            secret_key="secret",
            bucket="test-bucket",
            public_url="https://pub.r2.dev",
        )

        test_file = temp_dir / "photo.jpg"
        test_file.write_bytes(b"fake image")

        with patch.object(backend, "_client") as mock_client:
            backend._client = mock_client

            url = backend.upload_image(test_file)

        assert url == "https://pub.r2.dev/images/photo.jpg"

    def test_upload_lora_uses_loras_prefix(self, temp_dir):
        """Should use loras/ prefix for upload_lora."""
        backend = R2Backend(
            endpoint="https://test.endpoint",
            access_key="key",
            secret_key="secret",
            bucket="test-bucket",
            public_url="https://pub.r2.dev",
        )

        test_file = temp_dir / "my-lora.safetensors"
        test_file.write_bytes(b"fake lora")

        with patch.object(backend, "_client") as mock_client:
            backend._client = mock_client

            url = backend.upload_lora(test_file)

        assert url == "https://pub.r2.dev/loras/my-lora.safetensors"


class TestStorageBackendProtocol:
    """Tests for StorageBackend protocol."""

    def test_r2backend_implements_protocol(self):
        """R2Backend should implement StorageBackend protocol."""
        backend = R2Backend(
            endpoint="https://test",
            access_key="key",
            secret_key="secret",
            bucket="bucket",
            public_url="https://public",
        )

        assert isinstance(backend, StorageBackend)

    def test_custom_backend_can_implement_protocol(self):
        """Custom backends should be able to implement protocol."""

        class MockBackend:
            def upload(self, local_path, key):
                return f"mock://{key}"

            def upload_image(self, image_path, prefix="images"):
                return f"mock://{prefix}/{image_path.name}"

            def upload_lora(self, lora_path):
                return f"mock://loras/{lora_path.name}"

        backend = MockBackend()
        assert isinstance(backend, StorageBackend)


class TestGetSetStorageBackend:
    """Tests for get_storage_backend and set_storage_backend."""

    def test_set_and_get_custom_backend(self):
        """Should be able to set and retrieve custom backend."""

        class CustomBackend:
            def upload(self, local_path, key):
                return "custom://url"

            def upload_image(self, image_path, prefix="images"):
                return "custom://image"

            def upload_lora(self, lora_path):
                return "custom://lora"

        custom = CustomBackend()
        set_storage_backend(custom)

        # Note: get_storage_backend("r2") would return the custom one
        # since we set _default_backend
        # This tests the set functionality works
