# semiautomatic

Automation tools for creative AI workflows.

**Note:** Early release (v0.1.0). Currently shipping simple image processing tools. Generators, video, post-processing, and training modules coming soon as they reach production quality.

## Installation

```bash
pip install semiautomatic
```

For development:
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

## Size Format Reference

| Format | Example | Description |
|--------|---------|-------------|
| `WxH` | `1920x1080` | Exact dimensions |
| `Wx` | `1920x` | Width-constrained, preserve aspect |
| `xH` | `x1080` | Height-constrained, preserve aspect |
| `N` | `0.5` | Scale factor (0.5 = 50%) |

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
