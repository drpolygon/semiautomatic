# semiautomatic

Automation tools for creative AI workflows.

**Note:** Early release. Currently shipping image processing, video processing, and image generation tools. Video generators, post-processing, and training modules coming soon.

## Installation

```bash
pip install semiautomatic
```

### Optional Dependencies

Some features require additional packages. Install what you need:

```bash
# For image/video generation (FAL, R2 storage)
pip install semiautomatic[generate]

# Everything
pip install semiautomatic[all]
```

| Extra | Includes | Used For |
|-------|----------|----------|
| `generate` | fal-client, boto3 | Image/video generation, cloud storage |
| `all` | All optional deps | Everything |

If you try to use a feature without its dependencies, you'll get a helpful error:
```
ImportError: boto3 package not found. Install with: pip install semiautomatic[generate]
```

### Development Setup

```bash
git clone https://github.com/drpolygon/semiautomatic.git
cd semiautomatic
uv sync
```

## Features

### Image Processing

Batch resize, convert, and compress images with intelligent size optimization for API limits.

**CLI Usage:**
```bash
# Resize images to exact dimensions
semiautomatic process-image --size 1920x1080

# Scale to 50%
semiautomatic process-image --size 0.5

# Width-constrained (preserve aspect ratio)
semiautomatic process-image --size 1920x

# Convert to PNG
semiautomatic process-image --format png

# Compress for Claude Vision API (5MB limit)
semiautomatic process-image --max-size 5

# Process single file
semiautomatic process-image --input photo.jpg --size 0.5

# Short alias
sa process-image --max-size 5
```

**Library Usage:**
```python
from pathlib import Path
from semiautomatic.image import compress_for_api, compress_to_size

# Compress image to fit API size limits (returns JPEG bytes)
img_bytes = compress_for_api(Path('photo.jpg'))

# Compress with custom limit
img_bytes = compress_for_api(Path('photo.jpg'), max_bytes=2 * 1024 * 1024)

# Full control over compression
from PIL import Image
with Image.open('photo.jpg') as img:
    result = compress_to_size(img, max_bytes=5 * 1024 * 1024)
    print(f"Final size: {result.final_size} bytes")
    print(f"Dimensions: {result.final_dims}")
    print(f"Quality: {result.quality}")
```

### Image Generation

Generate images using AI models (FLUX, Qwen, WAN) via the FAL provider.

**Requirements:** Install optional dependencies and set up API key:
```bash
pip install semiautomatic[generate]
# Add FAL_KEY to your .env file
```

**CLI Usage:**
```bash
# Generate with prompt
semiautomatic generate-image --prompt "a cat sitting on a windowsill"

# Specify model and size
semiautomatic generate-image --prompt "portrait photo" --model flux-dev --size portrait_4_3

# Generate multiple images
semiautomatic generate-image --prompt "abstract art" --num-images 4

# With LoRA (models that support it: flux-krea, qwen, wan-22)
semiautomatic generate-image --prompt "my style" --model flux-krea --lora path/to/lora.safetensors:0.8

# List available models
semiautomatic generate-image --list-models
```

**Library Usage:**
```python
from semiautomatic.image import generate_image

# Simple generation
result = generate_image("a cat sitting on a windowsill")
print(result.images[0].path)  # Path to downloaded image

# With options
result = generate_image(
    "a portrait photo",
    model="flux-dev",
    size="portrait_4_3",
    num_images=2,
)

# With LoRA
result = generate_image(
    "a cat in my style",
    model="flux-krea",
    loras=["path/to/lora.safetensors:0.8"],
)
```

**Available Models:**

| Model | Description | LoRA Support |
|-------|-------------|--------------|
| `flux-dev` | FLUX.1 Dev - balanced quality and speed (default) | No |
| `flux-schnell` | FLUX.1 Schnell - ultra-fast (4 steps) | No |
| `flux-pro` | FLUX.1 Pro - highest quality | No |
| `flux-krea` | FLUX.1 Krea with LoRA support | Yes |
| `qwen` | Qwen Image - high quality with LoRA | Yes |
| `wan-22` | WAN 2.2 14B - enhanced prompt alignment | Yes |

**Size Presets:**

| Preset | Dimensions |
|--------|------------|
| `square` | 1024x1024 |
| `square_hd` | 1536x1536 |
| `portrait_4_3` | 768x1024 |
| `portrait_16_9` | 576x1024 |
| `landscape_4_3` | 1024x768 (default) |
| `landscape_16_9` | 1024x576 |

Custom dimensions can also be specified as `WxH` (e.g., `1920x1080`).

### Video Processing

Speed adjustment, zoom effects, resize, trim, and frame extraction with FFmpeg.

**CLI Usage:**
```bash
# Speed adjustment
semiautomatic process-video --speed 1.25              # 1.25x speed
semiautomatic process-video --speed 0.5               # Slow motion

# Speed with easing curves
semiautomatic process-video --speed 10 --speed-ramp ease-out-in  # Whip effect

# Zoom effects
semiautomatic process-video --zoom 100:150            # Zoom from 100% to 150%
semiautomatic process-video --zoomh 100:110           # Horizontal zoom only

# Resize with fit modes
semiautomatic process-video --size 1080x1080          # Square (stretch)
semiautomatic process-video --size 1080x1080 --fit crop  # Crop to fill
semiautomatic process-video --size 1080x1080 --fit pad   # Letterbox

# Trimming
semiautomatic process-video --trim-start 2.5          # Remove first 2.5s
semiautomatic process-video --trim-end 3.0            # Remove last 3s

# Frame extraction
semiautomatic process-video --input video.mp4 --extract-frame last
semiautomatic process-video --input video.mp4 --extract-frame -5   # 5th from end
semiautomatic process-video --input video.mp4 --extract-time 5.5   # At 5.5 seconds

# Process single file with output path
semiautomatic process-video --input raw.mp4 --output final.mp4 --speed 1.5
```

**Library Usage:**
```python
from pathlib import Path
from semiautomatic.video import process_video, extract_frame_from_video

# Process video with speed and zoom
output = process_video(
    Path('input.mp4'),
    Path('./output'),
    speed=1.5,
    zoom_h=(100, 150),  # Zoom from 100% to 150%
)

# Extract a frame
frame = extract_frame_from_video(
    Path('video.mp4'),
    Path('./output'),
    frame_position='last'
)
```

## Size Format Reference

| Format | Example | Description |
|--------|---------|-------------|
| `WxH` | `1920x1080` | Exact dimensions |
| `Wx` | `1920x` | Width-constrained, preserve aspect |
| `xH` | `x1080` | Height-constrained, preserve aspect |
| `N` | `0.5` | Scale factor (0.5 = 50%) |

## Video Options Reference

### Speed Ramp Curves

| Curve | Effect |
|-------|--------|
| `ease-in` | Accelerates (quadratic) |
| `ease-out` | Decelerates |
| `ease-in-out` | Slow start/end, fast middle |
| `ease-out-in` | Fast start/end, slow middle (whip effect) |
| `ease-in-cubic` | More aggressive acceleration |
| `ease-in-quartic` | Very aggressive acceleration |
| `ease-in-quintic` | Extremely aggressive acceleration |

### Fit Modes

| Mode | Description |
|------|-------------|
| `stretch` | Stretch to fill (may distort) |
| `crop` | Scale to fill, crop excess |
| `crop-max` | Crop at source resolution, then scale |
| `pad` | Scale to fit, pad with black bars |

### Crop Alignment

`center`, `left`, `right`, `top`, `bottom`, `topleft`, `topright`, `bottomleft`, `bottomright`

## Compression Algorithm

When using `--max-size`, the compressor uses a multi-stage strategy:

1. Start at quality 95
2. If oversized and large, resize to max 1920px on longest edge
3. Progressively reduce JPEG quality (in steps of 5)
4. If still over limit at quality 60, shrink dimensions by 10%
5. Repeat until under limit or image too small (512px minimum)

This ensures maximum quality preservation while meeting size constraints.

## Development

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=semiautomatic
```

## License

MIT
