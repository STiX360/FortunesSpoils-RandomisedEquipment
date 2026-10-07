# Initial Inventory Allowances

Corpse generation is capped by an immutable snapshot of each living NPC's first-observed
eligible inventory. Counts are saved by actor identity and exact base record ID.
The snapshot resolves leveled inventory and excludes restocking, enchanted,
scripted, disabled-source and otherwise ineligible records under current settings.

## Generation

- Fresh NPC scripts request a snapshot at initialization and activation.
- Repeated requests never expand an existing allowance, including an empty one.
- Death rolls use at most the original count for each base, prioritizing worn items.
- Ordinary equipment rolls separately per allowed copy; failed rolls use allowance.
- Projectiles roll once per allowed stack portion. Merged excess stays ordinary.
- Missing or failed snapshots allow no generation, leaving items intact.
- Save/load preserves captured allowances, including genuinely empty ones.
- Loaded living NPCs without a snapshot may be captured under the default policy.

## Existing Saves

Default: `requireNewGameInventory = false`. Installing into an existing save
allows a snapshot of a living NPC on first observation (initialization,
activation or load). Upgrades preserve saved caps and processed corpses.

**Accepted trade-off:** first observation proves current inventory, not historical
provenance. Previously sold/planted items can enter that first cap. This deliberately
favours existing-save support; later inventory changes still cannot grow the cap.

## Strict Feature Toggle

Enable **Strict Inventory Tracking (Require New Game On First Install)** under
General, or set `requireNewGameInventory = true`, to restore the conservative
policy: first installation on an existing save blocks corpse generation, and
loaded NPCs without trusted caps get a policy-rejected empty allowance. Fresh
NPCs in new games or already-tracked upgrades may be captured normally.

Policy-rejected allowances are marked separately from genuine empty inventories
and capture failures. Turning strict mode off permits a living NPC's rejected
allowance to be captured on its next snapshot request; trusted caps never expand.
Older first-install-blocked saves have their unprocessed empty policy allowances
marked recoverable on load. Older ambiguous empty caps in tracked/migrating saves
stay frozen rather than guessing their provenance. Corpses are never snapshotted.
Turning strict mode on blocks first-install existing-save rolls even if caps were
previously captured in compatibility mode; it does not erase them or generated items.

## Limits

After the snapshot, this blocks quantity amplification, not every same-ID substitution. Identical
copies can merge, so an original removed and replaced with the same base ID can
still consume its original allowance. Legitimate later acquisitions do not grow
the allowance either. Changing source or value settings later cannot expand a
snapshot captured under stricter settings.

Snapshot/event ordering and inventory behavior require the in-game checks in
[Current In-Game Validation](CURRENT-INGAME-CHECKLIST.md). Mocked regression tests
cover traded/merged excess, worn priority, reloads and both policy modes. New
policy regression cases require an approved test run; writing them is not validation.
