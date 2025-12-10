# Image Upscaling

Upscale images using AI with Freepik's upscaling engines. Supports 2x and 4x scaling with optimization presets for different image types.

## Prerequisites

Set up your API key in `.env`:

```bash
FREEPIK_API_KEY=your-freepik-key
```

## Basic Upscaling

```bash
# 2x upscale (default)
sa upscale-image -iphoto.jpg

# 4x upscale
sa upscale-image -iphoto.jpg --scale 4x

# Specify output directory
sa upscale-image -iphoto.jpg --output-dir ./upscaled
```

## Upscaling Engines

```bash
# Auto-select best engine (default)
sa upscale-image -iphoto.jpg --engine automatic

# Clarity - best for photos
sa upscale-image -iphoto.jpg --engine clarity

# Magnific - best for art/illustrations
sa upscale-image -iillustration.png --engine magnific
```

| Engine | Best For |
|--------|----------|
| `automatic` | Auto-detect (default) |
| `clarity` | Photos, realistic images |
| `magnific` | Art, illustrations, stylized images |

## Optimization Presets

Optimize results for specific image types:

```bash
# Portrait photos (soft details)
sa upscale-image -iportrait.jpg --optimized-for soft_portraits

# Portrait photos (sharp details)
sa upscale-image -iportrait.jpg --optimized-for hard_portraits

# Artwork
sa upscale-image -iart.png --optimized-for art_n_illustration

# Game assets
sa upscale-image -isprite.png --optimized-for videogame_assets

# Landscapes
sa upscale-image -ilandscape.jpg --optimized-for nature_n_landscapes
```

| Preset | Best For |
|--------|----------|
| `standard` | General purpose (default) |
| `soft_portraits` | Portrait photos with soft details |
| `hard_portraits` | Portrait photos with sharp details |
| `art_n_illustration` | Artwork and illustrations |
| `videogame_assets` | Game textures and sprites |
| `nature_n_landscapes` | Nature and landscape photos |
| `films_n_photography` | Film stills and professional photos |
| `3d_renders` | 3D rendered images |
| `science_fiction_n_horror` | Sci-fi and horror imagery |

## Fine-Tuning Controls

```bash
# Creativity (0-10) - higher adds more details
sa upscale-image -iphoto.jpg --creativity 3

# HDR enhancement (0-10)
sa upscale-image -iphoto.jpg --hdr 5

# Resemblance to original (0-10)
sa upscale-image -iphoto.jpg --resemblance 7

# Detail fractality (0-10)
sa upscale-image -iphoto.jpg --fractality 4

# Combine options
sa upscale-image -iphoto.jpg \
  --scale 4x \
  --engine clarity \
  --optimized-for soft_portraits \
  --creativity 2 \
  --hdr 3
```

## Prompt-Guided Upscaling

Guide the upscaling with a text prompt:

```bash
# Manual prompt
sa upscale-image -iphoto.jpg --prompt "high detail portrait photo"

# Auto-generate prompt using vision model
sa upscale-image -iphoto.jpg --auto-prompt
```

## Batch Processing

Process all images in a directory:

```bash
# Process entire directory
sa upscale-image --input-dir ./images --scale 2x

# With options
sa upscale-image --input-dir ./images \
  --scale 4x \
  --engine clarity \
  --auto-prompt
```

## Library Usage

```python
from semiautomatic.image import upscale_image

# Basic upscale
result = upscale_image("photo.jpg")
print(result.path)

# With options
result = upscale_image(
    "photo.jpg",
    scale="4x",
    engine="clarity",
    optimized_for="soft_portraits"
)

# With fine-tuning
result = upscale_image(
    "photo.jpg",
    scale="4x",
    creativity=3,
    hdr=5,
    prompt="detailed portrait photograph"
)
```

## Tips

1. **Start with 2x** - Test before committing to 4x
2. **Match the preset** - Use the right preset for your image type
3. **Auto-prompt** - Let the vision model describe the image for better results
4. **Creativity balance** - Higher creativity adds details but may alter the image
5. **Resemblance** - Increase if the upscaled image diverges too much

## Next Steps

- [Video Processing](05-video-processing.md) - Edit videos
- [Prompt Generation](06-prompt-generation.md) - Create better prompts
