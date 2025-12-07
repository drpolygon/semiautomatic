# Roadmap

## v0.2.0 (Current)

All blockers complete. Ready for user testing.

### Pre-Release

- [ ] User testing of new features
- [ ] Tutorials for new features
- [ ] Final CHANGELOG.md review

### Release Checklist

- [ ] Merge to main
- [ ] Tag v0.2.0
- [ ] Publish to PyPI

---

## v0.2.1+

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
