# RAS Campaign × Landing Page Explorer

Answers: **which campaigns drive RFIs to a given landing page?** (e.g. `/overview`) for info.rasmussen.edu.

## Two versions

| File | Where it runs | Data |
|---|---|---|
| `index.html` | **Live URL:** https://mamechi1.github.io/apei-cro-toolkit/ras-lp-explorer/ | Static snapshot baked in at build time (90-day and 365-day ranges). "Data as of" date shown in the header. Refreshed weekly via scheduled Cowork task. |
| `cowork-artifact.html` | Claude Cowork artifact ("Ras Lp Explorer" in the sidebar) | Pulls fresh GA4 data on every open via the Google Analytics MCP. |

## Data definitions

- **RFI** = `landing_page_inquiry` key events, by GA4 session campaign × landing page
- **Apps** = `lp_application_complete` key events
- **Sessions** = sessions on info.rasmussen.edu; **CVRs** = per sessions (pair level)
- Thresholds: RFI pairs ≥1 RFI; session pairs >20 sessions (smaller show "—"); app pairs ≥3 apps; zero-RFI pairs kept only at 300+ sessions (static) / 100+ (live)
- Non-campaign traffic — (direct), (organic), (referral), (cross-network), (not set) — excluded by default via checkbox

## Verification

Pair-level RFI sums reconciled against page-level GA4 totals for FY26: `/` = 31,205, `/overview` = 30,839, `/medical-billing-coding/certificate` = 17,042; grand total 199,970 — exact match.

---
Maintained via Claude Cowork · GA4 property 253925809 · Owner: Amechi
