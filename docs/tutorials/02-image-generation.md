# Image Generation

Generate images using FLUX models (via FAL) or Recraft. This tutorial covers text-to-image, image-to-image, LoRA support, and style controls.

## Prerequisites

Set up your API keys in `.env`:

```bash
FAL_KEY=your-fal-key           # For FLUX models
RECRAFT_API_KEY=your-recraft-key  # For Recraft
```

## Basic Image Generation (FLUX)

```bash
# Simple text-to-image
semiautomatic generate-image --prompt "a cat sitting on a windowsill"

# Specify model
semiautomatic generate-image --prompt "portrait photo" --model flux-dev

# Different sizes
semiautomatic generate-image --prompt "landscape" --size landscape_16_9
semiautomatic generate-image --prompt "portrait" --size portrait_4_3
semiautomatic generate-image --prompt "square" --size square_hd
```

### Available FLUX Models

| Model | Description | LoRA Support |
|-------|-------------|--------------|
| `flux-dev` | Balanced quality/speed (default) | No |
| `flux-schnell` | Ultra-fast | No |
| `flux-pro` | Highest quality | No |
| `flux-krea` | Krea variant | Yes |
| `qwen` | Qwen image model | Yes |
| `wan-22` | WAN 2.2 14B | Yes |

### Size Presets

| Preset | Dimensions |
|--------|------------|
| `square` | 1024x1024 |
| `square_hd` | 1536x1536 |
| `portrait_4_3` | 768x1024 |
| `portrait_16_9` | 576x1024 |
| `landscape_4_3` | 1024x768 (default) |
| `landscape_16_9` | 1024x576 |

## Using LoRA

LoRA (Low-Rank Adaptation) lets you apply custom styles. Requires `flux-krea`, `qwen`, or `wan-22` models.

```bash
# Single LoRA
semiautomatic generate-image --prompt "portrait" --model flux-krea --lora path/to/style.safetensors

# LoRA with custom weight (0.0-1.0)
semiautomatic generate-image --prompt "portrait" --model flux-krea --lora path/to/style.safetensors:0.8

# Multiple LoRAs
semiautomatic generate-image --prompt "portrait" --model flux-krea \
  --lora style1.safetensors:0.7 \
  --lora style2.safetensors:0.5
```

## Recraft Provider

Recraft offers different artistic styles and image-to-image transformation.

```bash
# Text-to-image with style
semiautomatic generate-image --provider recraft --prompt "cyberpunk city" --style digital_illustration

# Realistic photo
semiautomatic generate-image --provider recraft --prompt "product photo" --style realistic_image

# Vector illustration
semiautomatic generate-image --provider recraft --prompt "logo design" --style vector_illustration
```

### Recraft Styles

| Style | Description |
|-------|-------------|
| `realistic_image` | Photorealistic (default) |
| `digital_illustration` | Digital art style |
| `vector_illustration` | Vector graphics |
| `logo_raster` | Logo design |
| `any` | Auto-detect |

### Image-to-Image

Transform an existing image with Recraft:

```bash
# Basic i2i
semiautomatic generate-image --provider recraft \
  --input-image photo.jpg \
  --prompt "make it an illustration"

# Control transformation strength (0.0-1.0)
semiautomatic generate-image --provider recraft \
  --input-image photo.jpg \
  --prompt "watercolor style" \
  --strength 0.7
```

### Advanced Recraft Options

```bash
# Artistic level (0-5, higher = more stylized)
semiautomatic generate-image --provider recraft \
  --prompt "portrait" \
  --style digital_illustration \
  --artistic-level 3

# Color palette
semiautomatic generate-image --provider recraft \
  --prompt "abstract art" \
  --colors "#FF0000" "#00FF00" "#0000FF"

# Background color
semiautomatic generate-image --provider recraft \
  --prompt "product on background" \
  --background-color "#FFFFFF"
```

## Library Usage

```python
from semiautomatic.image import generate_image, image_to_image

# Basic generation
result = generate_image("a cat on a windowsill", model="flux-dev")
print(result.images[0].path)

# With LoRA
result = generate_image(
    "portrait in custom style",
    model="flux-krea",
    loras=["style.safetensors:0.8"]
)

# Recraft with style
result = generate_image(
    "cyberpunk city",
    provider="recraft",
    style="digital_illustration"
)

# Image-to-image
result = image_to_image(
    "photo.jpg",
    "make it a watercolor painting",
    strength=0.7
)
```

## Tips

1. **Start with flux-dev** - Good balance of quality and speed
2. **Use size presets** - Optimized for each model
3. **LoRA weights** - Start at 0.7-0.8, adjust based on results
4. **Recraft strength** - Lower values (0.3-0.5) for subtle changes, higher (0.7-0.9) for dramatic transformation

## Next Steps

- [Video Generation](03-video-generation.md) - Create videos from images
- [Image Upscaling](04-image-upscaling.md) - Enhance image resolution
