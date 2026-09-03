# IKEA — Moveo PM customer workspace

This is the **customer mono-repo** for the Moveo ↔ IKEA relationship. One git repo, one customer, one project subfolder per workstream.

## 60-second orientation

- **The account at a glance:** open [`CUSTOMER-STATUS.md`](CUSTOMER-STATUS.md).
- **Who's who:** [`STAKEHOLDERS.md`](STAKEHOLDERS.md).
- **The work:** each engagement is a project subfolder with its own spec, status, and context.
- **The paper trail before July 2026:** the shared Drive folder `Clients › IKEA` is indexed in [`context/research/2026-09-03-drive-ikea-folder-index.md`](context/research/2026-09-03-drive-ikea-folder-index.md); every readable document there is digested into `context/` or `whatsapp-agent/context/`.

## Projects

| Project | What it is |
|---|---|
| [whatsapp-agent](whatsapp-agent/) | WhatsApp personal shopping agent for IKEA employees (phase 1) and, later, customers. |

## How to work here

`cd` into a project subfolder and run the moveo-pm skills (`brief`, `digest`, `prd`, `status`, `refresh-status`, `monday`, `sync-drive`) — they target the nearest project. For the cross-project view, run `pm-brief` or open `CUSTOMER-STATUS.md`. Don't run project skills from this customer root — there's no project here to act on.

This repo is managed by the `moveo-pm` Cowork plugin (enabled once in `.claude/`). The customer root deliberately has **no `methodology_version`** so the plugin treats it as an index, not a project.
