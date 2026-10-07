# Static Loot Simulator

Open `build/site/simulator.html`, or choose Loot Simulator in the catalogue.
Selecting a base displays the original item. Generate/Reroll always starts from
that base, never compounds previously rolled modifiers. Reset Item restores the
base without clearing unique discovery; Reset Session clears both.
Recent Rolls keeps the latest 20 results for the selected base. Click a row or
activate its item-name button with the keyboard to inspect that exact result
again. Browsing history does not reroll, increment the count, or rediscover a
unique. The next Reroll still generates a fresh item from the selected base.

The build bundles the actual mod Lua modules through Fengari Web 0.1.4 (MIT).
The player-facing controls are limited to base item, NPC level and NPC location.
Roll chances, tier progression settings and optional source switches are not
editable; the page uses standard mod defaults and shows read-only loot odds.
Starting configuration comes from runtime `config.lua`, not a separately authored
probability table. NPC tier progression, regional matching, family biases, mode
compatibility, weapon speed, final armor weight, charge budgets and projectile
grades use those Lua modules. Once-per-session unique discovery mirrors the
default once-per-save rule, including ordinary dual-affix fallback on exhaustion.
The browser uses its own random stream, not the game's saved seed sequence.

Item/effect/GMST metadata is committed in `data/simulator-snapshot.json` so GitHub
Pages and offline builds never require installed masters or network downloads.
Source coverage: Morrowind, Tribunal, Bloodmoon and OAAB Data. No assets, meshes,
textures, dialogue or game scripts are bundled. Modded overrides, ownership,
condition loss and actual engine combat behavior are not modeled. Every displayed
base is an allowlisted record, but runtime script/enchantment/value exclusions can
still leave it unchanged. Optional expansion switches gate source packs and effects.

`python tools/build.py site` refreshes the catalogue and simulator from current
runtime rules and authoring inputs without running tests. When source base records
change, explicitly refresh metadata with `tools/export_simulator_snapshot.py`
and the selected source-master paths in load order. It reads masters only and
uses OpenMW 0.51's published fixed effect flags; the snapshot records that source.
Then rebuild the site. New allowlisted bases lacking snapshot stats are omitted
until refreshed rather than given invented stats.

Browser regression checks: `node tests/simulator_browser.cjs` with Playwright
available and Chrome installed (`SIM_BROWSER_CHANNEL` can select another channel).
Third-party attribution: `site/vendor/fengari-LICENSE.txt`.

## Base-item images

The simulator embeds small inventory icons directly from UESP and mesh thumbnails
from the OAAB Library. Exact record IDs
are matched against the vanilla/expansion base-item tables; names alone never
select an image. `data/item-images.json` records the image URL, UESP file page
and item source page. Each displayed image links to both source pages, including
the file's attribution/rights information. These game images are not bundled or
claimed as original artwork. Items without a match show "No wiki image".
Failed image requests show "Image unavailable" without affecting generation.
Images require internet access; all loot logic still runs offline. Generated
items retain their base item's image. The fixed-size image area prevents layout
shifts while loading or rerolling.

Refresh links explicitly using `python tools/refresh_item_images.py` (network
access required), then rebuild the site. Normal builds use the committed index
and never contact UESP. Equipment-category navigation filters the base-item
picker, without changing the current item or generation probabilities.
Use `--oaab-only` to preserve existing UESP links while filling gaps from
`https://www.oaab.dev/library/`. OAAB thumbnails match the published record ID
and mesh path, and are included only if their file exists in the library's public
repository index. The footer links to the OAAB Library for these images. This
website-only imagery does not add OAAB assets or dependencies to the mod package.
