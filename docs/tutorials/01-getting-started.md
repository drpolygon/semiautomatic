# Getting Started

This tutorial walks you through installing semiautomatic and running your first commands.

## Installation

```bash
pip install semiautomatic
```

Verify the installation:

```bash
semiautomatic --version
```

You can also use the shorter alias:

```bash
sa --version
```

## System Requirements

**FFmpeg** (optional, for video processing):

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows - download from https://ffmpeg.org/download.html
```

Only needed if you'll use `process-video` for speed/zoom/trim effects. Not required for video generation.

## Environment Setup

Create a `.env` file in your project directory with API keys for the providers you want to use:

```bash
# Required for image/video generation (FAL)
FAL_KEY=your-fal-key

# Required for prompt generation
ANTHROPIC_API_KEY=your-anthropic-key

# Optional providers
RECRAFT_API_KEY=your-recraft-key
FREEPIK_API_KEY=your-freepik-key
WAVESPEED_API_KEY=your-wavespeed-key
HIGGSFIELD_API_KEY=your-higgsfield-key
HIGGSFIELD_SECRET=your-higgsfield-secret
OPENAI_API_KEY=your-openai-key
```

Get your API keys:
- **FAL**: https://fal.ai/dashboard/keys
- **Anthropic**: https://console.anthropic.com/
- **Recraft**: https://www.recraft.ai/
- **Freepik**: https://www.freepik.com/api
- **Wavespeed**: https://wavespeed.ai/
- **Higgsfield**: https://higgsfield.ai/
- **OpenAI**: https://platform.openai.com/api-keys

## Your First Commands

### Generate an Image

```bash
semiautomatic generate-image --prompt "a cat sitting on a windowsill, golden hour lighting"
```

Output is saved to `./output/` by default.

### Process an Image

```bash
# Resize to 50%
semiautomatic process-image --input photo.jpg --size 0.5

# Compress for API upload (e.g., Claude Vision 5MB limit)
semiautomatic process-image --input photo.jpg --max-size 5
```

### Generate a Video

```bash
semiautomatic generate-video --prompt "camera slowly zooms in" --image photo.jpg
```

### Get Help

```bash
# List all commands
semiautomatic --help

# Help for a specific command
semiautomatic generate-image --help
```

## Using as a Library

```python
from semiautomatic.image import generate_image, compress_for_api
from semiautomatic.video import generate_video

# Generate an image
result = generate_image("a cat on a windowsill")
print(result.images[0].path)

# Compress for API
img_bytes = compress_for_api("photo.jpg")

# Generate a video
result = generate_video("camera zooms in", input_image="photo.jpg")
print(result.videos[0].path)
```

## Next Steps

- [Image Generation](02-image-generation.md) - FLUX, Recraft, LoRA support
- [Video Generation](03-video-generation.md) - Kling, WAN, Higgsfield motion presets
- [Image Upscaling](04-image-upscaling.md) - AI upscaling with Freepik
- [Video Processing](05-video-processing.md) - Speed, zoom, resize, trim
- [Prompt Generation](06-prompt-generation.md) - AI-powered prompt creation
- [Vision & Captioning](07-vision-captioning.md) - Image understanding
