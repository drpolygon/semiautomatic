# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-12-08

### Added

- **LLM Provider Abstraction** (`lib/llm/`)
  - Provider-agnostic LLM interface with registry pattern
  - Claude provider via Anthropic API (requests-based, no SDK)
  - OpenAI provider via OpenAI API (requests-based, no SDK)
  - Public API: `complete()`, `complete_with_vision()`, `get_provider()`
  - Supports system prompts, temperature, max_tokens

- **Prompt Generation Module** (`prompt/`)
  - `generate-image-prompt` CLI command for platform-specific image prompts
  - `generate-video-prompt` CLI command for motion prompts from images
  - Schema-agnostic design with optional `--schema` for styling
  - Platforms: flux (default), midjourney
  - Video models: higgsfield (default), kling, generic
  - Library API: `generate_image_prompt()`, `generate_video_prompt()`

- **HuggingFace Vision Provider** (`lib/vision/huggingface.py`)
  - JoyCaption model via HuggingFace Gradio Space
  - Caption lengths: short, normal, long
  - Default vision provider (replaces FAL/Moondream)

### Changed

- **Vision providers refactored to infra-naming** (consistent with image/video)
  - `MoondreamProvider` → `FalVisionProvider` (provider: fal, model: moondream3)
  - `JoyCaptionProvider` → `HuggingFaceVisionProvider` (provider: huggingface, model: joycaption)
  - Default changed from fal to huggingface

- **Higgsfield Video Generation Provider**
  - Higgsfield DOP API integration with 120 motion presets
  - Models: higgsfield, higgsfield_lite, higgsfield_preview, higgsfield_turbo
  - Motion presets: camera movements, visual effects, action sequences
  - `--motion` and `--motion-strength` CLI options
  - `--list-motions` flag to display all available presets

- **Wavespeed Video Generation Provider**
  - Wavespeed API integration with HTTP polling
  - Models: kling2.5-wavespeed, wan2.2, wan2.5, sora2
  - Base64 image encoding for direct local file support
  - Loop mode for wan2.2 (tail image support)

- **FAL Video Generation Provider**
  - `generate-video` CLI command for AI video generation
  - FAL provider supporting Kling, Seedance, and Hailuo models
  - Models: kling1.5, kling1.6, kling2.0, kling2.1, kling2.5, kling2.6, klingo1, seedance1.0, hailuo2.0
  - Image-to-video generation with tail image support
  - Loop mode for seamless looping videos
  - Duration control (5s or 10s)
  - Library API: `generate_video()` with automatic downloads

- **Image Upscaling with Freepik Provider**
  - `upscale-image` CLI command for AI image upscaling
  - Freepik provider supporting 2x and 4x upscaling
  - Engines: automatic, clarity, magnific
  - Optimization presets: standard, soft_portraits, hard_portraits, art_n_illustration, videogame_assets, nature_n_landscapes, films_n_photography, 3d_renders, science_fiction_n_horror
  - Advanced controls: creativity, hdr, resemblance, fractality, prompt
  - Auto-prompt support using vision model
  - Library API: `upscale_image()` with automatic downloads
  - Batch processing with `--input-dir`

- **Recraft Image Generation Provider**
  - Recraft provider for text-to-image and image-to-image generation
  - Models: recraftv3, recraftv2
  - Built-in styles: realistic_image, digital_illustration, vector_illustration, logo_raster, any
  - Custom style UUID support
  - Image-to-image transformation with strength control
  - Controls: artistic_level, colors, background_color, no_text
  - Library API: `image_to_image()` for style transformation
  - Size presets: square, landscape, portrait, square_hd

- **FAL Image Generation Provider**
  - `generate-image` CLI command for AI image generation
  - FAL provider supporting FLUX, Qwen, and WAN models
  - Models: flux-dev, flux-schnell, flux-pro, flux-krea, qwen, wan-22
  - LoRA support for flux-krea, qwen, and wan-22 models
  - Size presets: square, square_hd, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9
  - Library API: `generate_image()` with automatic downloads
  - Provider registry pattern for extensibility

- **Shared Infrastructure for Generation Tools**
  - `lib/env.py`: Project root detection and automatic `.env` loading
  - `lib/storage.py`: Abstract `StorageBackend` protocol with R2 implementation
  - `lib/s3.py`: Lightweight S3 client with AWS4-HMAC-SHA256 signing (replaces boto3)
  - `lib/vision/`: Vision provider architecture with Moondream 3 support
  - `lib/api.py`: Polling utilities, download helpers, HTTP utilities
  - `defaults.py`: Centralized configuration defaults

- **Simplified Dependencies**
  - Removed `[generate]` optional extra - all features now included in base install
  - Replaced boto3 (~80MB) with minimal S3 implementation (~150 lines, zero new deps)

- **Configuration**
  - `.env.example`: Template for all supported environment variables

- **Video Processing Module**
  - Speed adjustment with easing curves (ease-in, ease-out, whip effects)
  - Zoom effects with independent horizontal/vertical control
  - Video resize with multiple fit modes (stretch, crop, pad)
  - Video trimming (start/end)
  - Frame extraction (first, last, middle, specific frame, timestamp)
  - `process-video` CLI command

- **Developer Experience**
  - `CLAUDE.md`: Project conventions for Claude Code sessions
  - `lib/subprocess.py`: UTF-8 subprocess wrapper for Windows compatibility
  - Integration test framework with `tests/output/` for manual inspection

- **Documentation**
  - `CONTRIBUTING.md`: Development setup, project structure, code style

### Changed

- Default video model changed from `kling2.1` to `kling2.6`
- Updated `pyproject.toml` with new dependencies (`python-dotenv`, `requests`)
- Comprehensive `README.md` with all user-facing documentation

### Fixed

- FAL video provider now supports local file paths (auto-uploads via `fal_client`)
- Wavespeed/Higgsfield providers now correctly handle `Path` objects
- Moondream vision provider uses correct API parameter (`prompt` instead of `query`)
- pytest `conftest.py` now loads `.env` for integration tests

## [0.1.0] - 2025-12-05

### Added

- **Image Processing Module**
  - Batch resize, convert, and compress images
  - Intelligent compression for API size limits (e.g., Claude Vision 5MB)
  - Multiple size formats: exact dimensions, scale factors, constrained dimensions
  - Format conversion (PNG, JPEG, auto-detect)
  - `process-image` CLI command

- **Library API**
  - `compress_for_api()`: Quick compression for API limits
  - `compress_to_size()`: Full control over progressive compression
  - `process_single_image()`: Single image processing

- **CLI**
  - `semiautomatic` command with `sa` alias
  - Subcommand architecture for extensibility

- **Project Setup**
  - Package structure with `src/` layout
  - pytest test suite with programmatic fixtures
  - hatchling build backend
  - Python 3.9+ compatibility

[Unreleased]: https://github.com/drpolygon/semiautomatic/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/drpolygon/semiautomatic/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/drpolygon/semiautomatic/releases/tag/v0.1.0
