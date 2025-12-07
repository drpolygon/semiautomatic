# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
  - `lib/vision/`: Vision provider architecture with Moondream 3 support
  - `lib/api.py`: Polling utilities, download helpers, HTTP utilities
  - `defaults.py`: Centralized configuration defaults

- **Optional Dependencies**
  - `semiautomatic[generate]`: FAL client and boto3 for generation features
  - Graceful error messages when optional dependencies missing

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

### Changed

- Updated `pyproject.toml` with new dependencies (`python-dotenv`, `requests`)
- Updated `README.md` with optional dependencies documentation

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

[Unreleased]: https://github.com/drpolygon/semiautomatic/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/drpolygon/semiautomatic/releases/tag/v0.1.0
