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

### Cinematic Storytelling

Import cinematic storytelling feature from legacy video-prompt generator.

### Storyboard Mode

Generate cinematic storyboards from a single image using image-edit models. Depends on edit-image module.

### Kling 2.6 Audio Control

Add `--no-audio` flag for Kling 2.6 video generation.

### Batch Mode for generate-video

Add `--input-dir` support to `generate-video` for batch image-to-video generation. Consistent with process-video and upscale-image.

### Version in Error Messages

Include version number in CLI error output to help diagnose wrong-install issues.

### Fix process-video -o Shortcut

`process-video` is missing `-o` alias for `--output`. Other commands have it.

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

- MkDocs + GitHub Pages if docs grow
- More providers (Replicate, Stability, etc.)
- Audio generation module
- Workflow chaining (generate → upscale → process)
- **Job runner**: Structured logging, manifest files for tracking jobs/outputs/params, resume/retry, batch operations
- **Parameter sweeps**: Test across models, LoRA strengths, prompts, etc. to compare outputs systematically
- **Flux-2 LoRA support**: See task-migration doc in legacy project for reference
- **Claude skills**: Documentation, tutorialization, testing, integration testing, publishing, roadmapping, changelogging
