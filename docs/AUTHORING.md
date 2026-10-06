# Authoring Map

Catalogue modifier types are **Crafted / Magical / Hybrid**; see
[Modifier Types](MODIFIER-TYPES.md) for definitions and multi-effect precedence.
Tier display labels are **Petty (T1), Lesser (T2), Common (T3), Greater (T4),
Grand (T5), Exquisite (T6)**. Internal tier identifiers remain numeric.

The website's exact-base and pair-compatibility browsing is documented in
[Catalogue Base Browser](BASE-BROWSER.md).

Current ordinary utility tier rules and magnitudes are recorded in
[Utility Affix Progression](AFFIX-PROGRESSION.md). Delivery mode can vary per
tier in expanded definitions and in utility `modes`/`durations` arrays.

- `data/loot-design.json`: fixed unique registry exported to the four runtime maps.
- `docs/reports/modifier-catalogue.md`: existing magic affix names, magnitudes, scopes.
- `tools/expanded_affix_data.py`: expanded-effect authoring definitions.
- `tools/weapon_affix_rules.py`: ordinary control-duration class factors and staff target-delivery policy; exported to `weapon_affix_policy.lua`.
- `mod/scripts/randomisedbasicloot/loot.lua`: physical families and composition.
- `mod/scripts/randomisedbasicloot/gap_affixes.lua`: earlier utility definitions.
- `mod/scripts/randomisedbasicloot/bargain_affixes.lua`: paired benefit/drawback families.
- `data/oaab_item_allowlist.json`, `data/protected_item_ids.json`: extraction inputs.
- Runtime `*_items.lua`: committed frozen pools; re-extraction requires local masters.
- `tools/unique_designs.py`, `generate_unique_registry.py`: optional registry authoring.

Generated files: `*_uniques.lua`, `magic_catalogue.lua`, `expanded_catalogue.lua`.
Do not edit their exported content directly. Website output is generated, not
an independent dataset. Existing sources remain heterogeneous; a unified schema
is a later migration, not part of the packaging change.

Historical reports describe previous prototypes and are not current runtime
guarantees. The copied DEVELOPMENT-SNAPSHOT.md records the original workspace
README and is historical context. Tests require explicit permission to execute.

The new repository is the only active workspace. Historical reports and the
development snapshot are Git-ignored; the two report-based authoring inputs
above, included-items report, and unique registry are explicit exceptions.
Keep other non-public material in ignored `local/` or `private/` directories.
Do not ignore build inputs: publishing them is necessary for clean-checkout builds.
