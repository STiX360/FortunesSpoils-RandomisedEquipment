# Publishing Setup and Release Gates

No workflow runs automatically on push, pull requests, or tags. None runs tests.
No GitHub remote is configured and no repository, Pages site, or Nexus upload
is created by preparing this folder.

## Before Public Sync

1. Review THIRD-PARTY-NOTICES.md and complete provenance/redistribution checks.
2. Review historical documents for local paths or private notes.
3. Keep the project unlicensed as requested; do not label it open source.
4. Choose the initial version and production defaults. 0.1.0-dev is a placeholder.
5. Commit the prepared sources, then add the intended GitHub remote.

## GitHub Actions

- Build artifacts: manual packaging and website generation, no deployment.
- Deploy catalogue: choose Actions as the Pages publishing source and dispatch
  from the desired version tag. It builds ONLY build/site. For development
  previews, dispatch from the development branch instead.
- Draft release: create and push a version tag first, then dispatch with that
  tag. Packages the tag, not a moving branch. Produces a draft prerelease; review
  it before publication. The production profile is not validation approval.
- Create release and nexus-production environments with required reviewers
  and appropriate branch/tag restrictions before enabling publishing.
- Official GitHub actions currently use major version tags. Review and pin
  their full commit SHAs before first publishing; remote resolution was not
  available during local preparation. The Nexus action is already SHA pinned.

## Nexus

Create the mod page and manually upload the first file. Obtain the existing
file ID (not just the mod ID). Configure:

- Repository variable NEXUS_PUBLISH_ENABLED=true only after release approval.
- nexus-production variable NEXUSMODS_FILE_ID for the existing main file.
- nexus-production secret NEXUSMODS_API_KEY; never commit it.

The workflow downloads the production ZIP and checksum from a published GitHub
release and checks version/profile identity. It never rebuilds the mod. It does
not archive older Nexus versions or update the displayed mod version by default.
Check Nexus history before retrying an uncertain upload: retrying can create
another file version. Save the returned version ID from the workflow summary.

Action reference: https://github.com/Nexus-Mods/upload-action
Pages reference: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Release Validation

Tests remain opt-in and require permission. Before v1, approve a validation
checklist, production settings, supported OpenMW version, and legacy-affix/save
compatibility guarantees. Copied prototype tests are not proof of current engine
behaviour. The current package manifest intentionally records validated=false.
