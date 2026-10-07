# Third-Party Provenance Review

Public release gate: audit copied code, documentation, icons, and data before
publication. This document is not legal clearance or a licence grant.

- Bethesda game content: installed records are referenced; no game masters,
  meshes, textures, sounds, or original plugins are included in this snapshot.
- `docs/images/loot-example.png`: player-provided gameplay screenshot, explicitly
  approved for README/release materials on 2026-10-07. It shows a modded game;
  other visible assets are not distributed by this mod. The image is not in the
  mod ZIP. Approval to use the screenshot is not a licence grant for its game assets.
- OAAB Data: optional installed content is referenced. Audit the derived
  allowlist/registry and upstream permissions before release.
- UESP: research links appear in design reports. Review any reproduced prose,
  images, or substantial table content and satisfy applicable upstream terms.
- Website images: `data/item-images.json` references externally hosted UESP
  inventory icons and OAAB Library thumbnails by exact record ID. The simulator
  credits the selected source in its footer. No image files are included in the
  mod ZIP. External hosting and attribution do not themselves establish reuse
  permission; include these references in the public-site rights review.
- Fengari Web: the website bundles version 0.1.4 with third-party licence notices
  under `site/vendor/`. Review those notices and ensure the site build includes
  them. Fengari is not part of the mod ZIP and grants no licence to our mod code.
- OpenMW and other mods: audit code provenance, especially any examples used
  during development. API usage does not itself establish copied-code licensing.
- Nexus upload action: invoked externally, not vendored. Its own MIT licence
  applies to that project, not as a licence grant for this mod.

No project LICENSE file is intentionally included. Review documentation for
local machine paths before public sync; legacy audit reports may contain them.
