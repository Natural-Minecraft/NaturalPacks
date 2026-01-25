# NaturalPacks 🏁🛡️

Automated Resource Pack Conversion for NaturalSMP.

## Flow
1. **Source**: NaturalUpdater (Spigot) uploads `generated.zip` from ItemsAdder via `/updater geyser`.
2. **Process**: This repository triggers a GitHub Action using `java2bedrock.sh` by @Kas-tle.
3. **Output**: Converted `.mcpack` and `.mappings` are uploaded back to the release.
4. **Deploy**: NaturalUpdater (Velocity) fetches and deploys assets to Geyser-Velocity.

## Setup
- Ensure any specific `java2bedrock.sh` flags are configured in `.github/workflows/convert.yml`.
- Make sure to use the specific `generated.zip` name when exporting.
