# RAS Campaign × Landing Page Explorer

Live Cowork artifact that answers: **which campaigns drive RFIs to a given landing page?** (e.g. `/overview`).

Built as the interactive replacement for the one-off `RAS_Campaign_LP_Explorer_FY26.xlsx` workbook.

## How it works

- `index.html` is the full source of the Cowork artifact (`ras-lp-explorer`). It runs inside Claude Cowork's sandboxed artifact view and pulls **fresh data from GA4 on every open** via the local Google Analytics MCP (`run_report`), so numbers are always current — no manual refresh of a spreadsheet.
- Requires: Claude Cowork with the Google Analytics MCP connected and access to GA4 property **253925809** (rasmussen.edu).
- Note: opening `index.html` directly in a browser will show the loading state only — `window.cowork.callMcpTool` exists only inside Cowork. The file lives here for review/versioning.

## Data definitions

| Metric | Definition |
|---|---|
| RFI | `landing_page_inquiry` key events, by session campaign × landing page |
| Apps | `lp_application_complete` key events, by session campaign × landing page |
| Sessions | Sessions on `info.rasmussen.edu`, by session campaign × landing page |
| RFI CVR / App CVR | RFIs ÷ Sessions, Apps ÷ Sessions (pair level) |

**Thresholds** (to keep GA4 responses manageable): session pairs pulled at >20 sessions (smaller pairs show “—”); app pairs at ≥3 apps; RFI pairs at ≥1 RFI. Zero-RFI pairs are only shown when they have ≥100 sessions.

**Non-campaign traffic** — `(direct)`, `(organic)`, `(referral)`, `(cross-network)`, `(not set)` — is excluded by default via checkbox.

## Features

- Left pane: all landing pages, sortable (RFIs, sessions, CVR, # campaigns), searchable.
- Right pane: every campaign driving to the selected page, with sessions / RFIs / RFI CVR / apps / App CVR.
- Date range selector (90 / 180 / 365 days) — re-queries GA4.
- Preferences (range, non-campaign toggle) persist between opens.

## Verification

Pair-level RFI sums were reconciled against page-level GA4 totals for FY26 (Jul 16 2025 – Jul 15 2026): `/` = 31,205, `/overview` = 30,839, `/medical-billing-coding/certificate` = 17,042; grand total 199,970 — exact match on both cuts.

---
Maintained via Claude Cowork · Data: GA4 property 253925809 · Owner: Amechi
