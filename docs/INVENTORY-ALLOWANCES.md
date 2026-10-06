# Initial Inventory Allowances

Corpse generation is capped by an immutable snapshot of each NPC's initially
eligible inventory. Counts are saved by actor identity and exact base record ID.
The snapshot resolves leveled inventory and excludes restocking, enchanted,
scripted, disabled-source and otherwise ineligible records under current settings.

## Generation

- Fresh NPC scripts request a snapshot at initialization and activation.
- Repeated requests never expand an existing allowance, including an empty one.
- Death rolls use at most the original count for each base, prioritizing worn items.
- Ordinary equipment rolls separately per allowed copy; failed rolls use allowance.
- Projectiles roll once per allowed stack portion. Merged excess stays ordinary.
- Missing, failed or untrusted snapshots allow no generation, leaving items intact.
- Save/load preserves allowances; loaded NPC scripts never recapture inventory.

## Existing Saves

A new game enables trusted fresh snapshots. Upgrading a save that already had
this mod preserves any saved allowances. Previously initialized NPCs without an
allowance receive an empty one; newly initialized NPCs may receive a snapshot.

Installing the mod for the first time into an existing save requires a new game
for corpse generation. Script initialization alone cannot prove that an NPC's
current inventory predates player trading or planting. Console samples still work,
and existing generated records are not rewritten.

## Limits

This blocks quantity amplification, not every same-ID substitution. Identical
copies can merge, so an original removed and replaced with the same base ID can
still consume its original allowance. Legitimate later acquisitions do not grow
the allowance either. Changing source or value settings later cannot expand a
snapshot captured under stricter settings.

Snapshot/event ordering and inventory behavior require the in-game checks in
[Current In-Game Validation](CURRENT-INGAME-CHECKLIST.md). Mocked regression tests
cover traded/merged excess, worn priority, reloads and fail-closed migration.
