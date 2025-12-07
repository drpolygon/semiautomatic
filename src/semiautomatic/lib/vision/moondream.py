"""
Moondream vision provider.

Uses Moondream 3 via FAL for image captioning and queries.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from semiautomatic.lib.vision.base import VisionProvider


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MOONDREAM_CAPTION_ENDPOINT = "fal-ai/moondream3-preview/caption"
MOONDREAM_QUERY_ENDPOINT = "fal-ai/moondream3-preview/query"

VALID_LENGTHS = ("short", "normal", "long")


# ---------------------------------------------------------------------------
# Provider Implementation
# ---------------------------------------------------------------------------

class MoondreamProvider(VisionProvider):
    """
    Moondream 3 vision provider via FAL.

    Requires FAL_KEY environment variable.
    """

    def __init__(self):
        self._client = None

    @property
    def name(self) -> str:
        return "moondream"

    @property
    def default_model(self) -> str:
        return "moondream3"

    def list_models(self) -> list[str]:
        return ["moondream3"]

    @property
    def _fal_client(self):
        """Lazy-load FAL client."""
        if self._client is None:
            try:
                import fal_client
            except ImportError:
                raise ImportError(
                    "fal_client package not found. Install with: pip install fal-client"
                )

            if not os.environ.get("FAL_KEY"):
                raise EnvironmentError(
                    "FAL_KEY environment variable not set. "
                    "Add FAL_KEY=... to your .env file."
                )

            self._client = fal_client

        return self._client

    def caption(
        self,
        image_path: Path,
        *,
        length: str = "normal",
        model: Optional[str] = None,
    ) -> str:
        """
        Generate a caption for an image.

        Args:
            image_path: Path to the image file.
            length: Caption length - "short", "normal", or "long".
            model: Ignored (only moondream3 available).

        Returns:
            Generated caption string.

        Raises:
            ValueError: If length is invalid.
            FileNotFoundError: If image doesn't exist.
        """
        # Validate inputs before making API calls
        if length not in VALID_LENGTHS:
            raise ValueError(
                f"Invalid length '{length}'. Use: {', '.join(VALID_LENGTHS)}"
            )

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Upload image and run captioning (requires fal_client)
        image_url = self._fal_client.upload_file(str(image_path))

        result = self._fal_client.run(
            MOONDREAM_CAPTION_ENDPOINT,
            arguments={
                "image_url": image_url,
                "length": length,
            },
        )

        return result["output"]

    def query(
        self,
        image_path: Path,
        question: str,
        *,
        model: Optional[str] = None,
    ) -> str:
        """
        Ask a question about an image.

        Args:
            image_path: Path to the image file.
            question: Question to ask about the image.
            model: Ignored (only moondream3 available).

        Returns:
            Model's response to the question.

        Raises:
            FileNotFoundError: If image doesn't exist.
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Upload image and run query
        image_url = self._fal_client.upload_file(str(image_path))

        result = self._fal_client.run(
            MOONDREAM_QUERY_ENDPOINT,
            arguments={
                "image_url": image_url,
                "query": question,
            },
        )

        return result["output"]
