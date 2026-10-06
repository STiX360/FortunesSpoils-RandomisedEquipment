# Affix Tier Names

Approved display names for the six-tier ordinary-affix system:

| Internal Tier | Display Label |
| --- | --- |
| T1 | Petty (T1) |
| T2 | Lesser (T2) |
| T3 | Common (T3) |
| T4 | Greater (T4) |
| T5 | Grand (T5) |
| T6 | Exquisite (T6) |

Internal tier identifiers remain numeric `1-X`. These labels describe affix
strength, not item rarity. Unique items remain a separate classification, and
item names retain their individual prefix/suffix names.

A dual-affix item can have different prefix and suffix tiers; preserve both rather
than assigning one combined item tier. All eligible bases retain access to every
applicable tier. Functionally redundant tiers can be omitted.

## Implementation Status

The website uses these labels in tier filters, family summaries and tier rows.
The earlier proposed Modest/Potent/Exalted three-tier naming scheme is superseded.
Power values and tier weights have not been changed by this display update.
Numeric filters and serialized tiers remain unchanged. Modifier types are
separate from grades; see [Crafted, Magical and Hybrid](MODIFIER-TYPES.md).

This documentation/website update changes no runtime settings, unique recipes,
generated item records or save data. No tests were run.
