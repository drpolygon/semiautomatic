# Roadmap

## v0.2.0 (Current)

### Blockers

- [ ] **Lightweight storage**: Replace boto3 (~80MB) with minimal S3/R2 implementation
  - Implement AWS4-HMAC-SHA256 signing using requests + hashlib (stdlib)
  - ~100-150 lines of code, zero new deps
  - Only used by: Higgsfield (image uploads), LoRA hosting

- [ ] **LLM provider abstraction**: Provider-agnostic LLM interface
  - `lib/llm/base.py` - LLMProvider ABC
  - `lib/llm/claude.py` - Anthropic API via requests
  - `lib/llm/openai.py` - OpenAI API via requests (optional)
  - Same pattern as image/video providers, zero SDK deps

- [ ] **Prompt generation module**: Migrate prompt tools for aesthetics-lab
  - `src/semiautomatic/prompt/image.py` - schema → platform prompts (Midjourney/FLUX)
  - `src/semiautomatic/prompt/video.py` - image + schema → motion prompts
  - CLI: `generate-image-prompt --schema FILE`, `generate-video-prompt --schema FILE`
  - Schema-agnostic (aesthetics-lab handles aesthetic ID resolution)
  - Uses `lib/llm/` for prompt generation, `lib/vision/` for image analysis

- [ ] **Simplify deps**: Remove `[generate]` extra entirely
  - Move fal-client to core deps
  - Delete optional-dependencies from pyproject.toml
  - `pip install semiautomatic` just works, no extras needed

### Release Checklist

- [ ] Lightweight storage implementation
- [ ] LLM provider abstraction
- [ ] Prompt generation module
- [ ] Move fal-client to core deps, remove extras
- [ ] Update README (remove [generate] references)
- [ ] Final CHANGELOG.md review
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
