# Fortune's Spoils - Randomised Equipment

Randomised loot for OpenMW, featuring tiered prefixes and suffixes, modified
equipment stats, and custom unique items. Configurable drop rates, optional
content support, and an interactive modifier catalogue.

**Development snapshot. Not validated for production saves.**

The current ordinary-affix [utility progression](docs/AFFIX-PROGRESSION.md)
includes timed-to-constant Water Breathing/Walking, Slowfall and Levitate tiers.
Other utility effects retain CE with magnitude/range scaling. Unique templates
and previously generated items are unchanged. No tests were run for this update.

## Repository Boundaries

This folder is the active working root. The previous Morrowind workspace is
historical and is not used as a build input or synchronised source.
Keep non-public notes, screenshots, and local audit outputs under `local/` or
`private/`; both are ignored. Historical reports and the old development
snapshot are ignored too. Required authoring tables and curated item catalogues
remain publishable so a clean GitHub checkout can build the website and mod.

| Directory | Purpose | Distributed in the mod ZIP? |
| --- | --- | --- |
| `mod/` | Installable Lua scripts, localisation, OpenMW manifest | Yes |
| `data/` | Authoring registry and frozen/protected item lists | No |
| `site/` | Static catalogue template | No |
| `tools/` | Export, build, and optional game-data inspection tools | No |
| `docs/` | Installation, research, design, historical reports | No |
| `tests/` | Manually invoked tests; some retain prototype assumptions | No |
| `release/` | Version, packaging profiles, packaged installation notes | Selected notes |
| `build/`, `dist/` | Generated output; ignored by Git | Not source |

## Build

Python 3.10+; normal builds use the standard library and need no installed game
masters. Run commands from the repository root:

```powershell
python tools/build.py site
python tools/build.py package --profile testing
```

Open `build/site/index.html` directly in a browser. Website output is static and
can be deployed to GitHub Pages. ZIPs and SHA-256 sidecars appear in `dist/`.

The Loot Simulator is at `build/site/simulator.html`, linked from the catalogue.
It runs the bundled Lua loot rules offline with selectable bases, NPC levels and
mapped locations. See [Simulator Details](docs/LOOT-SIMULATOR.md).

Production defaults use 33% single affix, 33% dual affix, 33% unchanged and 1%
global unique chance (eligible non-projectiles with feasible outcomes):

```powershell
python tools/build.py package --profile production
```

Saved settings override package defaults. Production logging defaults off; this
profile is not a claim of engine validation. No build task
runs tests. Export authoring changes explicitly with `python tools/build.py export`;
this updates generated Lua in `mod/` and generated expanded-affix documentation.

## Runtime Identity

The public working title is Fortune's Spoils. The manifest, Lua namespace, and
settings label retain Randomised Basic Loot to avoid a saved-script identity
change. See [installation](release/INSTALL.md) and [testing notes](docs/TESTING.md).

## Publishing

GitHub workflows are manual only: build artifacts, deploy Pages, prepare a draft
release, or upload an existing release asset to Nexus. No scheduled publishing
or tests are enabled. See [publishing setup](docs/PUBLISHING.md).

## Rights

No project licence has been granted at this stage. This repository is not
advertised as open source. Third-party rights remain with their owners; see
[provenance review](docs/THIRD-PARTY-NOTICES.md). Game masters and original assets
must not be committed or included in release archives.
