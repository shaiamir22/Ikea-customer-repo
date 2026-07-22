# IKEA — customer repo

_This is a **customer repo**, not a single project. It groups every Moveo ↔ IKEA workstream under one roof. It is intentionally **not** a moveo-pm project — there is **no `methodology_version`** here, so the plugin's project skills won't treat this root as a project._

## How this repo is laid out

```
IKEA/
├── CLAUDE.md                ← this file (customer index)
├── CUSTOMER-STATUS.md       ← customer dashboard + the marker that this is a customer root
├── STAKEHOLDERS.md          ← shared stakeholder registry across all workstreams
├── README.md                ← 60-second human orientation
├── context/                 ← CROSS-PROJECT context only (events spanning workstreams)
│   ├── open-action-items.md ← cross-project / relationship-level action items (per-project items stay in <project>/context/)
│   ├── meetings/            ← cross-project meetings & calls
│   ├── stakeholder-notes/   ← cross-project 1:1s & stakeholder feedback
│   ├── research/            ← cross-project research, competitor scans
│   └── comms/               ← cross-project outbound/inbound comms worth logging
├── .claude/                 ← enables the moveo-pm plugin (settings.json) + prototype preview (launch.json)
└── <project>/               ← one full moveo-pm project per workstream (CLAUDE.md w/ methodology_version, PROJECT-STATUS.md, spec, context/)
```

The customer-level `context/` mirrors a project's `context/` (same `meetings|stakeholder-notes|research|comms` buckets + `open-action-items.md`) — the difference is **scope**: only material that spans workstreams or belongs to the relationship lives here. Anything tied to one workstream belongs in `<project>/context/`.

## Two ways to work here

**Drill into one project** — `cd` into the project subfolder and run the moveo-pm skills there. They resolve to the nearest `CLAUDE.md` (walk-up), so they target that project. **Run project skills from inside a project subfolder, not from this customer root** — from here they have no project to act on.

**See the whole customer**
- Live cross-project rollup: `pm-brief projects_root=<path to this repo>` → "what's active / what's next" across all projects. (The customer-aware `pm-brief` also picks this up from a default global run, via the `CUSTOMER-STATUS.md` marker.)
- Durable account state: open `CUSTOMER-STATUS.md`. It holds relationship/commercial state and links to each project's `PROJECT-STATUS.md` — it does **not** restate per-project execution detail.

## Conventions

- `CUSTOMER-STATUS.md` is the canonical marker that this folder is a customer root.
- Project status is owned per-project (`<project>/PROJECT-STATUS.md`). Customer status links to it rather than duplicating it, so nothing drifts.
- Cross-project context lives in `./context/`; project-specific context lives in `<project>/context/`. Same bucket names at both levels — scope decides where a note lands.
- Cross-project / relationship-level action items go in `./context/open-action-items.md`; per-project action items stay in `<project>/context/open-action-items.md`. Don't restate per-project items at the customer level.
- One git repo for the whole customer (the customer mono-repo). The moveo-pm plugin is enabled once, at this root, and inherited by every project.

## Running skills from the customer root

Most moveo-pm skills are **project-scoped** and refuse to run without a `methodology_version` (which this root deliberately lacks). Two patterns apply here:

- **`digest`** — when the input spans workstreams (a kickoff, a customer-wide call, a handoff), run it from this customer root and it writes to `./context/{meetings|stakeholder-notes|research|comms}/` and syncs any cross-project action items into `./context/open-action-items.md`. When the input is about a single workstream, `cd` into that project and run `digest` there instead.
- **Everything else** (`brief`, `status`, `prd`, `prototype`, `refresh-status`, `monday`, `sync-drive`) is project-scoped — `cd` into a project subfolder. For the customer-wide rollup use `pm-brief projects_root=<this repo>`.

## What NOT to do

- **Do not add a `methodology_version` to this file** — it would make the plugin treat the customer root as a (malformed) project.
- **Do not duplicate per-project status here.** Link to it.
- **Do not modify files in any project's `prototypes/archive/`.** Frozen snapshots.
- **Do not commit secrets** (no `.env`, no API keys).
