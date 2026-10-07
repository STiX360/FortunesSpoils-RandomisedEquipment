# Release Readiness

Status: release preparation, not publication. Candidate: `0.1.0`,
a functional early beta, not balanced for regular play. Feedback on bugs,
oversights and balance is welcome. Do not mark this
checklist complete based on mocked APIs, website checks or package generation.

## Prepared

- [x] Production defaults: 33% single affix, 33% dual, 33% unchanged, 1% unique
  for eligible non-projectiles; routine logging off.
- [x] NPC-level tier scaling, equal tier weights at NPC level 25+.
- [x] Player installation guide documents existing-save trade-off, strict toggle, optional content,
  runtime settings name and save restrictions.
- [x] Website catalogue and player-reference simulator; not an in-game feature.
- [x] Manual packaging, draft GitHub release and gated Nexus-upload workflows.
- [x] Draft first-release description and known limitations.

## Validation Required

- [ ] Approve and run the relevant automated suites against the final commit.
- [ ] Complete [in-game validation](../docs/CURRENT-INGAME-CHECKLIST.md) on the
  intended supported OpenMW version, recording engine version and package hash.
- [ ] Confirm worn corpse replacements, counts, normal kills and no duplicate originals.
- [ ] Confirm projectile stacking, equipping and firing across separate drops/reloads.
- [ ] Confirm save/load persistence, no corpse rerolls and unique discovery persistence.
- [ ] Confirm sold/planted items cannot expand original inventory roll allowances.
- [ ] Validate existing-save first-observation snapshots, accepted pre-snapshot
  trade-off, strict toggle and migration of earlier first-install policy blocks.
- [ ] Test base-game-only installation and optional content/effect gating.
- [ ] Validate production settings in-game; saved testing settings override defaults.
- [ ] Review representative uniques, charged effects, drawbacks and CE removal.

## Publication Required

- [x] Position the first public release as an early beta welcoming bug, oversight
  and balance feedback; candidate version `0.1.0`, labelled prerelease on GitHub.
- [ ] Freeze the selected commit before final validation/packaging. A production
  ZIP is not proof of stability or balance.
- [x] Add the player-approved corpse loot/tooltip screenshot to the README and release notes.
- [ ] Optional additional screenshots: a unique, settings and the website.
- [ ] Complete [third-party review](../docs/THIRD-PARTY-NOTICES.md), including
  website UESP/OAAB imagery and bundled Fengari notices. No project licence is granted.
- [x] Resolve and pin official workflow action tags to fixed commits.
- [x] Inspect the local 0.1.0 production ZIP: 27 runtime files only, production
  defaults, companion manifest and matching ZIP/file/checksum hashes.
- [ ] Review the final tag-built GitHub release assets before publishing.
- [ ] Approve release notes and save-compatibility wording for the chosen version.
- [ ] Configure protected publishing environments and Pages source in GitHub.
- [ ] Create/review the GitHub draft release from the selected version tag.
- [ ] Create the Nexus page and upload the first approved file manually.
- [ ] Configure Nexus credentials outside the repository only after approval.

## Distribution

The mod ZIP contains only runtime Lua, localisation and the OpenMW manifest.
The player installation guide, build manifest and checksums are companion release
assets outside the ZIP. The screenshot, catalogue/simulator and third-party image
links are not in the mod ZIP. Release manifests currently retain
`validated=false`; do not silently promote them to validated during packaging.

No publishing, tagging, credential configuration or validation approval is implied
by this preparation. At v1, freeze the agreed legacy-affix/save compatibility policy.

Manual feedback on 2026-10-07: the player reported the revised existing-save build
working and provided a corpse-loot screenshot showing several generated items.
OpenMW version was not supplied; unreported validation cases remain unchecked.
