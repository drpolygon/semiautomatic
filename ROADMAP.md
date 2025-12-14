# Roadmap

## v0.2.0 (Current)

All blockers complete. Ready for user testing.

### Pre-Release

- [ ] Tutorials for new features
- [ ] User testing (follow the tutorials)
- [ ] Final CHANGELOG.md review

### Release Checklist

- [ ] Merge to main
- [ ] Tag v0.2.0
- [ ] Publish to PyPI

---

## v0.2.1+

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

### Batch Mode for generate-video

Add `--input-dir` support to `generate-video` for batch image-to-video generation. Consistent with process-video and upscale-image.

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

### Version in Error Messages

Include version number in CLI error output to help diagnose wrong-install issues.

### Platform-Specific Prompt Tuning

Tune prompt generators for different platforms. Image: FLUX prefers detailed narratives, Midjourney prefers frontloaded comma-separated values. Video: Higgsfield vs Kling vs generic styles need refinement. The `--platform` and `--video-model` flags exist but outputs aren't well-optimized.

### Fix Zoom < 100% Centering

Video processing `--zoomh` and `--zoomv` values below 100% push the image to top-left instead of centering. Need to implement letterboxing/centering when zoom scale is less than 1.0.

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
- **More size presets**: All major aspect ratios (2:3, 3:2, 4:5, 5:4, etc.) with HD variants
- **--dry flag for validation**: Add `--dry` to generation commands to validate CLI args, provider resolution, and payload construction without calling APIs. Enables tutorial testing: `pytest -m tutorials` (dry, default) or `pytest -m tutorials --live` (real API)
