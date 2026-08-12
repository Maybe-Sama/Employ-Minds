# Upstream provenance

Employ-Minds is not a wholesale vendoring of either upstream project. It is an independently authored synthesis designed to avoid two independent workflow governors competing in the same agent context.

## Everything Claude Code (ECC)

- Repository: `affaan-m/ECC`
- Initial synthesis revision: see `UPSTREAMS.lock.json`
- License: MIT
- Ideas used as architectural reference: broad harness composition, skills/agents/tool-native project structure, orchestration breadth, research and reusable engineering conventions.

## Superpowers

- Repository: `obra/superpowers`
- Initial synthesis revision: see `UPSTREAMS.lock.json`
- License: MIT
- Ideas used as process reference: design discipline, TDD, root-cause debugging, structured delegation/review, and verification before completion.

## Synthesis boundary

Employ-Minds intentionally does **not** load both frameworks wholesale. Overlapping concepts are normalized into the Employ-Minds router and gates. Upstream licenses are preserved in `third_party/`; this repository's own implementation is MIT licensed separately.
