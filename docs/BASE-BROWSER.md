# Catalogue Base Browser

The static catalogue includes source and base-name/record-ID filters. Selecting
an exact base narrows prefix and suffix families and displays its registered
fixed unique recipes, including effects, stats and drawbacks.

The base list uses the committed included-items report. Unique recipes use
`data/loot-design.json`. Ordinary family restrictions are attached during
catalogue export, using the shared scope vocabulary for existing magic tables
and the expanded authoring definitions. Earlier utility slot rules are mapped
in `tools/catalogue_bases.py`; keep this mapping aligned with `gap_affixes.lua`.

The Pair with selector chooses an affix and tier, then filters the opposite side
by enchantment delivery mode, duplicate family and Hybrid opposite-effect rules.
It is an eligibility preview, not a probability calculator or live engine simulator.

Armor-skill entries are conditional alternatives. The corresponding skill is
selected using the generated item's final weight class; tier and magnitude
remain equivalent across Light, Medium and Heavy Armor. The preview does not
simulate installed GMST overrides or weight/class thresholds.

Enchantment-capacity candidates require positive loaded base capacity. The
source report has no capacity column, so these remain visible with this
condition rather than guessing capacity from modified unique recipes.
Settings, expansion availability, summon/bound record mappings, script
protection and installed record overrides still determine in-game eligibility.

Projectile bases display only the current stack-quality prefix family and no
uniques or pair selector, matching the dedicated projectile generation path.

The build embeds all metadata and JavaScript in the HTML. No server, external
data requests or local master files are required for browsing or GitHub Pages.
Run `tools/build.py site` to update it; this does not run tests.
