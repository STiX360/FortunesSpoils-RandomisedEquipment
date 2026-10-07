# Publishing GitHub Releases And Nexus Updates

First version: **0.1.0**, a functional early-beta **prerelease**, not a stable or
balanced playthrough recommendation. Version-tag pushes publish GitHub prereleases;
Nexus uploads remain manual. These workflows run no test suites. Pages deploys
on push to `main` or manual dispatch. Preparing
these files does not publish the mod or configure credentials.

## Local Packaging

From the repository root:

```powershell
python tools/build.py package --profile production
python tools/verify_release.py dist/fortunes-spoils-0.1.0-production.zip --version 0.1.0 --profile production
```

Outputs:

- `fortunes-spoils-0.1.0-production.zip`: installable runtime files only.
- `fortunes-spoils-0.1.0-production.manifest.json`: version/profile/defaults,
  source commit, validation flag and hashes of every packaged file.
- `fortunes-spoils-0.1.0-production.zip.sha256`: hashes of the ZIP and manifest.
- `INSTALL.md`: separate player installation guide.

The ZIP root contains `scripts/`, `l10n/` and `Randomised Basic Loot.omwscripts`.
No extra wrapping folder, README, build metadata, screenshots, website, tests,
source registries or tools. Do not install GitHub's source-code archive as the
mod. `verify_release.py` inspects artifact contents/hashes, not game behavior.
Local builds before committing are previews; the release workflow rebuilds from
the final tag so the companion manifest names the published commit.

## First GitHub Release: Your Steps

1. Review [Release Readiness](../release/READINESS.md), installation guide,
   release notes and third-party notices. Disclose early-beta validation gaps;
   do not mark them complete. Tests still require explicit permission.
2. Commit the release preparation and screenshot, then push to `main`. This also
   triggers Pages deployment; it does not publish a mod release.
3. In repository Settings > Environments, configure `release` and
   `nexus`, using reviewers and tag restrictions where available.
   Pages should use GitHub Actions as its publishing source.
4. Tag the approved checked-out commit and push the tag:

```powershell
git tag v0.1.0
git push origin v0.1.0
```

5. A new version-tag push now runs **Publish version release**, packaging and
   verifying production files before publishing the early-beta prerelease.
   The tag must match `release/metadata.json`. Environment approval rules still
   apply. Review release notes and assets before pushing a publication tag.
6. For an already-existing tag such as `v0.1.0`, commit/push the updated workflow
   to `main`, then use Actions > **Publish version release** > Run workflow.
   Choose `main`, tag `v0.1.0`, production, blank override and enable **publish**.
   Existing tags do not retroactively trigger a push event. Leaving publish off
   creates a draft for manual review instead. Do not move or recreate the tag.
   If a draft already exists, review/publish it instead of creating it again.
7. Download the published production ZIP for the first Nexus upload; do not
   rebuild a different ZIP for Nexus. The workflow never overwrites an existing
   release; inspect a failed run before retrying.

Official workflow actions and the Nexus uploader are pinned to fixed commits.
Build/release workflows do not deploy Nexus.

## First Nexus Post: Your Steps

1. Create the Morrowind Nexus mod page. Pitch it as functional early beta, not
   balanced for regular play; welcome bugs, oversights and balance feedback.
2. Upload the **same production ZIP downloaded from GitHub** as the first main
   file, version `0.1.0`. Use `release/INSTALL.md` and `release/NOTES.md` as copy
   references and the approved screenshot for media.
3. Record the existing **file ID**, not merely the mod ID. The official uploader
   describes finding it using Advanced in the public Files tab or Manage Files.
4. In GitHub's `nexus` environment, add variable `NEXUSMODS_FILE_ID`
   and secret `NEXUSMODS_API_KEY`. Never paste the key into source, issues or chat.
5. Once approved, add repository Actions variable `NEXUS_PUBLISH_ENABLED=true`.
   Leave it unset/false until the first page/file exists and wiring is reviewed.

This does not upload another 0.1.0 copy automatically. Use the next workflow for
the next approved version.

## Future Versions

1. Bump `release/metadata.json` to the next 0.X.X version and update
   `release/NOTES.md`, including version-specific links and screenshot URL.
2. Review the release material, commit and push a matching version tag. GitHub
   packages and publishes the prerelease automatically as above.
3. Run **Upload existing release to Nexus (manual)** with the published tag.
4. It downloads the release's production ZIP, manifest and checksums, verifies
   version/profile and every runtime file, then uploads that ZIP unchanged as a
   new version of the configured Nexus file. It never rebuilds.
5. Record the returned Nexus version ID and review the listing. Older versions
   are not archived and the mod-page version is not changed automatically.
   Update them manually as appropriate. Check history before retrying an uncertain
   upload: a retry may create another file version.

References: [Official Nexus uploader](https://github.com/Nexus-Mods/upload-action),
[GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

## Validation And Compatibility

The companion manifest retains `validated=false` until formal release validation
is completed. A working screenshot, production profile or successful workflow is
not a stability/balance guarantee. At v1, freeze the agreed legacy-affix/save
compatibility policy. No project licence is granted by this setup.
