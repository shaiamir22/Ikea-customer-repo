# CLAUDE.md — WhatsApp Shopping Agent

_This file is the project's identity card and the contract between the project folder and the `moveo-pm` plugin. Skills read this file to find the project root and load project-specific configuration. Don't restructure the headings — skills look for them by name._

## Project identity

- **project_name:** WhatsApp Shopping Agent
- **client:** IKEA
- **pm_name:** Shai Amir
- **pm_email:** shai.amir@moveo.co.il
- **engagement_type:** product
- **methodology_version:** 1

## Current state pointers

- **deployed_url:** https://d3dhoisfjbdi8v.cloudfront.net (business dashboard) · https://d3dhoisfjbdi8v.cloudfront.net/agent-management.html (agent dashboard)
- **github_repo_url:** agent code lives in IKEA's own GitHub workspace, not here. This repo is for customer management and product work.
- **monday_item_url:** not configured
- **gdrive_folder_id:** 1CY2UskhBZyxC7w3y-5ieNIj2GQj0z75Y (shared `Clients › IKEA` folder; the customer-level index at `../context/research/2026-09-03-drive-ikea-folder-index.md` lists what is in it)
- **spec_file:** IKEA_WhatsApp_Shopping_Agent_PRD.md

## Project-specific overrides (optional)

_Most projects leave this section empty. Use it only when a plugin-default needs to change for this specific engagement._

- **brand_voice_profile:** default
- **comms_default_language:** auto
- **status_default_window_days:** 14

## Conventions

The `moveo-pm` plugin owns the methodology — skills, folder structure, file formats, and hard rules. This project follows that methodology. To learn what's available, run `brief` at the start of a session or check the plugin's README.

Project-specific files live in this repo. Skill behavior lives in the plugin. Update the plugin once; every project picks up the change.

## What NOT to do

- **Do not modify files in `prototypes/archive/`.** Those are frozen snapshots.
- **Do not silently overwrite the spec or prototypes.** All skills show a diff and wait for approval.
- **Do not commit secrets** (no `.env`, no API keys).
- **Do not change the four-section structure of `PROJECT-STATUS.md`** or the PRD template — skills assume the format.
- **Do not invent decisions or progress.** If a context file is ambiguous, ask. If a "shipped" claim isn't backed by evidence, mark it as reported / verify with the PM.

## Quick reference

- Preview prototypes locally: `python3 -m http.server 3000`, then open `http://localhost:3000/prototypes/current/{file}.html`
- Open project dashboard: `PROJECT-STATUS.md`
- Update the Monday item: run `monday`
- Back the spec up to Drive: run `sync-drive`
