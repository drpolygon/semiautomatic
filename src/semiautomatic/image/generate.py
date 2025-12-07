"""
Image generation orchestration for semiautomatic.

Provides high-level API for image generation with automatic provider selection,
image downloading, and batch processing.

Library usage:
    from semiautomatic.image import generate_image

    # Simple generation
    result = generate_image("a cat sitting on a windowsill")
    print(result.images[0].path)  # Path to downloaded image

    # With options
    result = generate_image(
        "a portrait photo",
        model="flux-dev",
        size="portrait_4_3",
        num_images=4,
        output_dir=Path("./output"),
    )

CLI usage:
    semiautomatic generate-image --prompt "a cat" --model flux-dev
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional, Union

from semiautomatic.lib.logging import log_info, log_error
from semiautomatic.lib.api import download_file
from semiautomatic.defaults import (
    IMAGE_DEFAULT_PROVIDER,
    IMAGE_DEFAULT_MODEL,
    IMAGE_DEFAULT_SIZE,
    IMAGE_DEFAULT_NUM_IMAGES,
    IMAGE_DEFAULT_OUTPUT_FORMAT,
)
from semiautomatic.image.providers import (
    get_provider,
    list_providers,
    list_all_models,
    ImageProvider,
    ImageResult,
    GenerationResult,
    ImageSize,
    LoRASpec,
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_image(
    prompt: str,
    *,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    size: Union[str, ImageSize] = None,
    num_images: int = None,
    seed: Optional[int] = None,
    loras: Optional[list[Union[str, LoRASpec]]] = None,
    output_dir: Optional[Path] = None,
    output_prefix: Optional[str] = None,
    download: bool = True,
    **kwargs,
) -> GenerationResult:
    """
    Generate images from a text prompt.

    Args:
        prompt: Text description of the image to generate.
        model: Model name (provider-specific). Uses default if not specified.
        provider: Provider name ("fal", etc.). Auto-detected from model if not specified.
        size: Image size as preset name, "WxH" string, or ImageSize.
        num_images: Number of images to generate (1-4).
        seed: Random seed for reproducibility.
        loras: List of LoRA paths or LoRASpec objects.
        output_dir: Directory to save downloaded images. Defaults to ./output.
        output_prefix: Prefix for output filenames.
        download: Whether to download images locally (default: True).
        **kwargs: Additional provider-specific parameters.

    Returns:
        GenerationResult with generated images.

    Examples:
        # Simple generation
        result = generate_image("a cat")

        # With model and size
        result = generate_image(
            "a portrait",
            model="flux-dev",
            size="portrait_4_3",
        )

        # With LoRA
        result = generate_image(
            "a cat in my style",
            model="flux-krea",
            loras=["path/to/lora.safetensors:0.8"],
        )
    """
    # Apply defaults
    model = model or IMAGE_DEFAULT_MODEL
    size = size or IMAGE_DEFAULT_SIZE
    num_images = num_images if num_images is not None else IMAGE_DEFAULT_NUM_IMAGES

    # Get provider (auto-detect or use specified)
    provider_name = provider or _detect_provider_for_model(model) or IMAGE_DEFAULT_PROVIDER
    image_provider = get_provider(provider_name)

    # Parse LoRAs
    parsed_loras = None
    if loras:
        parsed_loras = [
            lora if isinstance(lora, LoRASpec) else LoRASpec.from_string(lora)
            for lora in loras
        ]

    # Generate
    log_info(f"Generating {num_images} image(s) with {model}...")

    result = image_provider.generate(
        prompt=prompt,
        model=model,
        size=size,
        num_images=num_images,
        seed=seed,
        loras=parsed_loras,
        **kwargs,
    )

    log_info(f"Generated {len(result.images)} image(s)")

    # Download images if requested
    if download and result.images:
        output_dir = output_dir or Path("./output")
        output_dir.mkdir(parents=True, exist_ok=True)

        prefix = output_prefix or f"gen_{int(time.time())}"

        for i, img in enumerate(result.images):
            # Determine extension from URL or content type
            ext = _get_extension(img.url, img.content_type)

            if len(result.images) == 1:
                filename = f"{prefix}{ext}"
            else:
                filename = f"{prefix}_{i + 1}{ext}"

            output_path = output_dir / filename

            if download_file(img.url, output_path):
                img.path = output_path
                log_info(f"Saved: {output_path.name} ({img.width}x{img.height})")
            else:
                log_error(f"Failed to download: {img.url}")

    return result


def _detect_provider_for_model(model: str) -> Optional[str]:
    """Detect which provider supports a given model."""
    all_models = list_all_models()

    for provider_name, models in all_models.items():
        if model in models:
            return provider_name

    return None


def _get_extension(url: str, content_type: Optional[str] = None) -> str:
    """Get file extension from URL or content type."""
    # Try content type first
    if content_type:
        if "png" in content_type:
            return ".png"
        if "jpeg" in content_type or "jpg" in content_type:
            return ".jpg"

    # Fall back to URL
    url_lower = url.lower()
    if ".png" in url_lower:
        return ".png"
    if ".jpg" in url_lower or ".jpeg" in url_lower:
        return ".jpg"
    if ".webp" in url_lower:
        return ".webp"

    # Default
    return ".png"


# ---------------------------------------------------------------------------
# CLI Handler
# ---------------------------------------------------------------------------

def run_generate_image(args) -> bool:
    """
    CLI handler for generate-image command.

    Args:
        args: Parsed argparse namespace.

    Returns:
        True if successful, False otherwise.
    """
    # Handle list-models
    if getattr(args, "list_models", False):
        _print_models()
        return True

    # Validate prompt
    if not args.prompt:
        log_error("No prompt provided. Use --prompt 'your prompt here'")
        return False

    # Parse LoRAs
    loras = None
    if args.lora:
        loras = args.lora

    try:
        result = generate_image(
            prompt=args.prompt,
            model=args.model,
            provider=getattr(args, "provider", None),
            size=args.size,
            num_images=args.num_images,
            seed=getattr(args, "seed", None),
            loras=loras,
            output_dir=Path(args.output_dir),
            steps=getattr(args, "steps", None),
            guidance=getattr(args, "guidance", None),
            output_format=getattr(args, "format", IMAGE_DEFAULT_OUTPUT_FORMAT),
        )

        log_info(f"Complete! Generated {len(result.images)} image(s)")
        return True

    except Exception as e:
        log_error(f"Generation failed: {e}")
        return False


def _print_models():
    """Print available models."""
    all_models = list_all_models()

    print("\nAvailable models:\n")
    for provider_name, models in all_models.items():
        print(f"  {provider_name}:")
        provider = get_provider(provider_name)
        for model in models:
            info = provider.get_model_info(model)
            desc = info.get("description", "")
            lora = " [LoRA]" if info.get("supports_loras") else ""
            print(f"    {model}{lora}")
            if desc:
                print(f"      {desc}")
        print()
