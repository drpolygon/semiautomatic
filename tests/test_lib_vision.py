"""
Tests for semiautomatic.lib.vision module.

Tests cover:
- Vision provider registry
- MoondreamProvider (mocked)
- Public API functions
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from semiautomatic.lib.vision import (
    get_caption,
    get_prompt,
    describe_image,
    get_provider,
    list_providers,
    register_provider,
    VisionProvider,
    MoondreamProvider,
)


class TestProviderRegistry:
    """Tests for provider registry functions."""

    def test_list_providers_includes_moondream(self):
        """Should include moondream in available providers."""
        providers = list_providers()
        assert "moondream" in providers

    def test_get_provider_returns_moondream(self):
        """Should return MoondreamProvider for 'moondream'."""
        provider = get_provider("moondream")
        assert isinstance(provider, MoondreamProvider)

    def test_get_provider_default_is_moondream(self):
        """Should return moondream when no name specified."""
        provider = get_provider()
        assert isinstance(provider, MoondreamProvider)

    def test_get_provider_raises_for_unknown(self):
        """Should raise ValueError for unknown provider."""
        with pytest.raises(ValueError) as exc_info:
            get_provider("nonexistent_provider")

        assert "nonexistent_provider" in str(exc_info.value)
        assert "moondream" in str(exc_info.value)  # Should list available

    def test_register_provider_adds_new_provider(self):
        """Should be able to register custom providers."""

        class CustomVisionProvider(VisionProvider):
            @property
            def name(self):
                return "custom"

            def caption(self, image_path, *, length="normal", model=None):
                return "custom caption"

            def query(self, image_path, question, *, model=None):
                return "custom answer"

        register_provider("custom_test", CustomVisionProvider)

        providers = list_providers()
        assert "custom_test" in providers


class TestMoondreamProvider:
    """Tests for MoondreamProvider."""

    def test_name_is_moondream(self):
        """Provider name should be 'moondream'."""
        provider = MoondreamProvider()
        assert provider.name == "moondream"

    def test_default_model_is_moondream3(self):
        """Default model should be moondream3."""
        provider = MoondreamProvider()
        assert provider.default_model == "moondream3"

    def test_list_models_includes_moondream3(self):
        """Should list moondream3 as available model."""
        provider = MoondreamProvider()
        models = provider.list_models()
        assert "moondream3" in models

    def test_caption_raises_for_invalid_length(self, small_image_path):
        """Should raise ValueError for invalid length."""
        provider = MoondreamProvider()

        # ValueError for invalid length is checked before fal_client is accessed
        with pytest.raises(ValueError) as exc_info:
            provider.caption(small_image_path, length="invalid")

        assert "invalid" in str(exc_info.value).lower()

    def test_caption_raises_for_missing_file(self, temp_dir):
        """Should raise FileNotFoundError for missing image."""
        provider = MoondreamProvider()
        missing_path = temp_dir / "nonexistent.jpg"

        with pytest.raises(FileNotFoundError):
            provider.caption(missing_path)

    def test_query_raises_for_missing_file(self, temp_dir):
        """Should raise FileNotFoundError for missing image."""
        provider = MoondreamProvider()
        missing_path = temp_dir / "nonexistent.jpg"

        with pytest.raises(FileNotFoundError):
            provider.query(missing_path, "What is this?")


class TestGetCaption:
    """Tests for get_caption() public API."""

    def test_raises_for_missing_file(self, temp_dir):
        """Should raise FileNotFoundError for missing image."""
        missing_path = temp_dir / "missing.jpg"

        with pytest.raises(FileNotFoundError):
            get_caption(missing_path)

    def test_accepts_string_path(self, small_image_path):
        """Should accept string path."""
        with patch.object(MoondreamProvider, "caption", return_value="test caption"):
            # This should not raise - string paths are valid
            result = get_caption(str(small_image_path))
            assert result == "test caption"

    def test_accepts_path_object(self, small_image_path):
        """Should accept Path object."""
        with patch.object(MoondreamProvider, "caption", return_value="test caption"):
            result = get_caption(small_image_path)
            assert result == "test caption"


class TestGetPrompt:
    """Tests for get_prompt() public API."""

    def test_returns_short_caption(self, small_image_path):
        """Should use short caption as prompt."""
        with patch.object(
            MoondreamProvider, "caption", return_value="short description"
        ) as mock_caption:
            result = get_prompt(small_image_path)

            mock_caption.assert_called_once()
            # Should request short length
            call_kwargs = mock_caption.call_args[1]
            assert call_kwargs.get("length") == "short"

    def test_truncates_long_prompts(self, small_image_path):
        """Should truncate prompts longer than max_length."""
        long_caption = "x" * 600

        with patch.object(MoondreamProvider, "caption", return_value=long_caption):
            result = get_prompt(small_image_path, max_length=100)

            assert len(result) == 100
            assert result.endswith("...")


class TestDescribeImage:
    """Tests for describe_image() public API."""

    def test_raises_for_missing_file(self, temp_dir):
        """Should raise FileNotFoundError for missing image."""
        missing_path = temp_dir / "missing.jpg"

        with pytest.raises(FileNotFoundError):
            describe_image(missing_path, "What is this?")

    def test_passes_question_to_provider(self, small_image_path):
        """Should pass question to provider query method."""
        with patch.object(
            MoondreamProvider, "query", return_value="It's a test image"
        ) as mock_query:
            result = describe_image(small_image_path, "What do you see?")

            mock_query.assert_called_once()
            call_args = mock_query.call_args[0]
            assert call_args[1] == "What do you see?"


@pytest.mark.integration
class TestMoondreamIntegration:
    """Integration tests for Moondream provider.

    These tests require FAL_KEY to be set and make real API calls.
    Run with: pytest -m integration
    """

    @pytest.fixture(autouse=True)
    def check_dependencies(self):
        """Skip if fal_client not installed."""
        try:
            import fal_client
        except ImportError:
            pytest.skip("fal_client not installed (pip install semiautomatic[generate])")

    def test_caption_generates_text(self, small_image_path, integration_output_dir):
        """Should generate a caption for a real image."""
        import os

        if not os.environ.get("FAL_KEY"):
            pytest.skip("FAL_KEY not set")

        result = get_caption(small_image_path, length="short")

        assert isinstance(result, str)
        assert len(result) > 0

        # Save output for inspection
        output_file = integration_output_dir / "moondream_caption.txt"
        output_file.write_text(f"Caption: {result}")

    def test_query_answers_question(self, small_image_path, integration_output_dir):
        """Should answer a question about a real image."""
        import os

        if not os.environ.get("FAL_KEY"):
            pytest.skip("FAL_KEY not set")

        result = describe_image(small_image_path, "What colors do you see?")

        assert isinstance(result, str)
        assert len(result) > 0

        # Save output for inspection
        output_file = integration_output_dir / "moondream_query.txt"
        output_file.write_text(f"Question: What colors do you see?\nAnswer: {result}")
