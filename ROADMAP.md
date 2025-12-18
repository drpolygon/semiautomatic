# Roadmap

## v0.2.1 (Current)

v0.2.0 was yanked, moving directly to v0.2.1b1. Now on b2 after removing FAL size presets.

### Blockers

**Recraft (02-image-generation tutorial)**:
- Investigate why `--background-color` is not working

**Higgsfield (03-video-generation tutorial)**:
- Model mapping broken: defaults to "kling2.6" instead of valid Higgsfield model
- Valid models: higgsfield, higgsfield_preview, higgsfield_lite, higgsfield_turbo

**Wavespeed model naming**:
- `kling2.5-wavespeed` should just be `kling2.5` - provider determines routing
- Model name shouldn't include provider suffix

**Batch mode for generate-video**:
- Add `--input-dir` support for batch image-to-video generation
- Consistent with process-video and upscale-image

### Pre-Release

- [ ] Beta test 0.2.1b2
- [ ] Final CHANGELOG.md review

### Release Checklist

- [ ] Merge to main
- [ ] Tag v0.2.1
- [ ] Publish to PyPI

---

## Future Features

### Caption CLI Command

Add `sa caption` (or `sa get-caption`) CLI command for image captioning. Currently vision is library-only. Reference implementation exists in legacy repo.

### Cinematic Storytelling

Import cinematic storytelling feature from legacy video-prompt generator.

### Storyboard Mode

Generate cinematic storyboards from a single image using image-edit models. Depends on edit-image module.

### Text-to-Video Support

Add t2v models (WAN, Luma, etc.) - currently all video models are i2v only. Re-add `--aspect-ratio` / `--ar` flag when t2v is implemented.

### Kling 2.6 Audio Control

Add `--no-audio` flag for Kling 2.6 video generation.

### Auto-Prompt for generate-video

Add `--auto-prompt` flag to `generate-video`. Should call `generate-video-prompt` internally to avoid duplicating vision-to-motion-prompt logic.

### generate-video-prompt QOL

Two improvements:
1. **Batch to JSON**: Add `--input-dir` that outputs all prompts to a single JSON file, easily piped into `generate-video`.
2. **Auto-compress**: Detect when image exceeds vision API payload limits and auto-reduce using `process-image` before sending.

### LoRA Upload Caching

Cache uploaded LoRA files to avoid re-uploading on every API call. Currently `upload_lora()` uploads the full file every generation request. Implement hash-based deduplication: compute file hash, check if already uploaded (local cache or remote check), return cached URL if exists. Significant optimization for workflows using the same LoRA repeatedly.

### Concurrent Workers for upscale-image

Add `--workers` flag to `upscale-image` for parallel batch processing. Currently batch mode processes images sequentially.

### Multiple Upscale Providers

Abstract upscale provider interface to support multiple upscalers (Topaz, Real-ESRGAN, etc.). Currently types like `ScaleFactor`, `UpscaleEngine`, `UpscaleSettings` are imported from the Freepik provider. Need a base `UpscaleProvider` class (like `ImageProvider`) with provider-agnostic settings.

### Magnific Mystic Model

Add Magnific's Mystic model to `generate-image` as a new image generation provider/model.

### Shell Completion

Add tab completion for subcommands and flags using `argcomplete`. Users would activate with `eval "$(register-python-argcomplete sa)"`. Can also complete flag values (model names, provider names, etc.) with custom completers.

### Version in Error Messages

Include version number in CLI error output to help diagnose wrong-install issues.

### Platform-Specific Prompt Tuning

Tune prompt generators for different platforms. Image: FLUX prefers detailed narratives, Midjourney prefers frontloaded comma-separated values. Video: Higgsfield vs Kling vs generic styles need refinement. The `--platform` and `--video-model` flags exist but outputs aren't well-optimized.

### Exact Size Output

Auto-resize generated images to match requested dimensions when model output differs (e.g., 1080x1080 requested but model produces 1072x1072 due to model constraints). Add `--no-resize` flag to skip resizing and keep native model output.

### CLI Modularization

Split cli.py into modules when it exceeds 800 lines:

```
src/semiautomatic/cli/
  __init__.py       # main(), build_parser()
  image.py          # generate-image, upscale-image, process-image
  video.py          # generate-video, process-video
```

Not blocking for 0.2.0 - current monolithic structure still works.

---

## Future Ideas

- Captioning module from legacy (with HF_TOKEN support for priority access)
- MkDocs + GitHub Pages if docs grow
- More providers (Replicate, Stability, etc.)
- Audio generation module
- Workflow chaining (generate → upscale → process)
- **Job runner**: Structured logging, manifest files for tracking jobs/outputs/params, resume/retry, batch operations
- **Parameter sweeps**: Test across models, LoRA strengths, prompts, upscaling engines, upscaling presets (soft_portraits, etc.), fine-tuning controls (creativity, hdr, resemblance, fractality) to compare outputs systematically
- **Flux-2 LoRA support**: See task-migration doc in legacy project for reference
- **Claude skills**: Documentation, tutorialization, testing, integration testing, publishing, roadmapping, changelogging
- **Multi-format compression**: Support PNG and other formats for `--max-size` (currently JPEG only)
- **Semantic size presets**: Redesign size presets with semantic names (e.g., `landscape`, `portrait`, `square`) that map to optimal dimensions per model/provider. Example: `landscape` → 1280x720 for FLUX, 1365x1024 for Recraft. Include all major aspect ratios with HD variants.
- **--dry flag for validation**: Add `--dry` to generation commands to validate CLI args, provider resolution, and payload construction without calling APIs. Enables tutorial testing: `pytest -m tutorials` (dry, default) or `pytest -m tutorials --live` (real API)
