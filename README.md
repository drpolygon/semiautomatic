# semiautomatic

Automation tools for creative AI workflows. Generate images and videos, upscale, process, and transform media with a unified CLI and Python API.

## Installation

```bash
pip install semiautomatic
```

### Environment Setup

Create a `.env` file in your project root with the API keys you need:

```bash
# Image/video generation (FAL)
FAL_KEY=your_fal_key

# Image generation (Recraft)
RECRAFT_API_KEY=your_recraft_key

# Image upscaling (Freepik)
FREEPIK_API_KEY=your_freepik_key

# Video generation (Wavespeed)
WAVESPEED_API_KEY=your_wavespeed_key

# Video generation (Higgsfield)
HIGGSFIELD_API_KEY=your_higgsfield_key
HIGGSFIELD_SECRET=your_higgsfield_secret
```

## Image Processing

Batch resize, convert, and compress images with intelligent size optimization.

```bash
# Resize to exact dimensions
semiautomatic process-image --size 1920x1080

# Scale to 50%
semiautomatic process-image --size 0.5

# Width-constrained (preserve aspect ratio)
semiautomatic process-image --size 1920x

# Compress for API limits (e.g., Claude Vision 5MB)
semiautomatic process-image --max-size 5

# Process single file
semiautomatic process-image --input photo.jpg --size 0.5
```

```python
from pathlib import Path
from semiautomatic.image import compress_for_api

# Compress image for API upload
img_bytes = compress_for_api(Path('photo.jpg'))
```

## Image Generation

Generate images using FLUX, Qwen, WAN (via FAL) or Recraft.

```bash
# Generate with FAL (default)
semiautomatic generate-image --prompt "a cat in a sunbeam" --model flux-dev

# With LoRA
semiautomatic generate-image --prompt "my style" --model flux-krea --lora path/to/lora.safetensors:0.8

# Generate with Recraft
semiautomatic generate-image --provider recraft --prompt "cyberpunk city" --style digital_illustration

# Image-to-image with Recraft
semiautomatic generate-image --provider recraft --input-image photo.jpg --prompt "illustration style" --strength 0.7

# List models
semiautomatic generate-image --list-models
```

```python
from semiautomatic.image import generate_image, image_to_image

result = generate_image("a cat in a sunbeam", model="flux-dev")
print(result.images[0].path)

# Recraft image-to-image
result = image_to_image("photo.jpg", "make it an illustration", strength=0.7)
```

### FAL Models

| Model | Description | LoRA |
|-------|-------------|------|
| `flux-dev` | FLUX.1 Dev - balanced (default) | No |
| `flux-schnell` | FLUX.1 Schnell - ultra-fast | No |
| `flux-pro` | FLUX.1 Pro - highest quality | No |
| `flux-krea` | FLUX.1 Krea | Yes |
| `qwen` | Qwen Image | Yes |
| `wan-22` | WAN 2.2 14B | Yes |

### Recraft Styles

`realistic_image`, `digital_illustration`, `vector_illustration`, `logo_raster`, `any`

## Image Upscaling

AI upscaling with 2x or 4x via Freepik.

```bash
semiautomatic upscale-image --input photo.jpg
semiautomatic upscale-image --input photo.jpg --scale 4x --engine clarity
semiautomatic upscale-image --input photo.jpg --optimized-for soft_portraits
```

```python
from semiautomatic.image import upscale_image

result = upscale_image("photo.jpg", scale="4x", engine="clarity")
print(result.path)
```

### Engines

| Engine | Best For |
|--------|----------|
| `automatic` | Auto-select (default) |
| `clarity` | Photos, realistic images |
| `magnific` | Art, illustrations |

### Optimization Presets

`standard`, `soft_portraits`, `hard_portraits`, `art_n_illustration`, `videogame_assets`, `nature_n_landscapes`, `films_n_photography`, `3d_renders`, `science_fiction_n_horror`

## Video Processing

Speed adjustment, zoom effects, resize, trim, and frame extraction.

```bash
# Speed adjustment
semiautomatic process-video --speed 1.5
semiautomatic process-video --speed 10 --speed-ramp ease-out-in  # Whip effect

# Zoom
semiautomatic process-video --zoom 100:150

# Resize with fit modes
semiautomatic process-video --size 1080x1080 --fit crop

# Trim
semiautomatic process-video --trim-start 2.5 --trim-end 3.0

# Extract frame
semiautomatic process-video --input video.mp4 --extract-frame last
```

```python
from pathlib import Path
from semiautomatic.video import process_video, extract_frame_from_video

output = process_video(Path('input.mp4'), Path('./output'), speed=1.5)
frame = extract_frame_from_video(Path('video.mp4'), Path('./output'), frame_position='last')
```

### Speed Curves

| Curve | Effect |
|-------|--------|
| `ease-in` | Accelerates |
| `ease-out` | Decelerates |
| `ease-in-out` | Slow start/end |
| `ease-out-in` | Whip effect |

### Fit Modes

| Mode | Description |
|------|-------------|
| `stretch` | Stretch to fill |
| `crop` | Scale and crop |
| `pad` | Scale and letterbox |

## Video Generation

Generate videos using Kling, Seedance, Hailuo (via FAL), WAN/Sora (via Wavespeed), or Higgsfield.

```bash
# Text-to-video
semiautomatic generate-video --prompt "a cat walking" --model kling2.6

# Image-to-video
semiautomatic generate-video --input image.jpg --prompt "make it move"

# With motion preset (Higgsfield)
semiautomatic generate-video --input portrait.jpg --model higgsfield --motion zoom_in

# List models and motions
semiautomatic generate-video --list-models
semiautomatic generate-video --list-motions
```

```python
from semiautomatic.video import generate_video

result = generate_video("a cat walking", model="kling2.6", duration=5)
print(result.videos[0].path)

# With motion
result = generate_video("animate", input_image="portrait.jpg", model="higgsfield", motion="zoom_in")
```

### Video Models

**FAL:** `kling1.5`, `kling1.6`, `kling2.0`, `kling2.1`, `kling2.5`, `kling2.6` (default), `klingo1`, `seedance1.0`, `hailuo2.0`

**Wavespeed:** `kling2.5-wavespeed`, `wan2.2`, `wan2.5`, `sora2`

**Higgsfield:** `higgsfield`, `higgsfield_lite`, `higgsfield_preview`, `higgsfield_turbo`

## Reference

### Size Formats

| Format | Example | Description |
|--------|---------|-------------|
| `WxH` | `1920x1080` | Exact dimensions |
| `Wx` | `1920x` | Width-constrained |
| `xH` | `x1080` | Height-constrained |
| `N` | `0.5` | Scale factor |

### Image Size Presets

| Preset | Dimensions |
|--------|------------|
| `square` | 1024x1024 |
| `square_hd` | 1536x1536 |
| `portrait_4_3` | 768x1024 |
| `portrait_16_9` | 576x1024 |
| `landscape_4_3` | 1024x768 |
| `landscape_16_9` | 1024x576 |

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup.

## License

MIT
