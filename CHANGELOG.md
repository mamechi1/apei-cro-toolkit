# Changelog

## 2026-10-05 — v2026.10.05
- Scheduled refresh of both Live-column tests (automated run, no interactive confirmation).
  RAS 11044B RFI Form Placement extended to Sep 29 – Oct 4 (+0.9% RFI lift, 52.3% one-sided,
  $85,968 projected) and HON 11107 Homepage Hero Design to Sep 22 – Oct 4, which crossed the
  ship rule: **+11.0% RFI lift at 93.4% one-sided confidence** (was +6.6% / 79.0% at Oct 1).
- Confirmed the reused-audience check the 2026-10-02 entry calls for: the stale
  `RAS | PW | Degree Finder Higher | homepage-*` audiences carrying 11044B's variations have
  **zero sessions before the Sep 29 Live Date**, so no prior-test membership is bleeding in.
- build_report.py: added a **HON** entry to `SCHOOL_BRAND` ('H' / HONDROS / COLLEGE OF NURSING).
  Without it `SCHOOL_BRAND.get('HON', ...)` fell through to the RAS default, so every Hondros
  report's no-JS header read "RASMUSSEN UNIVERSITY". Donut palettes still fall back to RAS
  green — no Hondros palette is defined, and none was invented here.
- Known cosmetic issue, not fixed: with no Hondros application event, the HON sigbox renders
  "App Complete CVR: NaN% lift". Needs a zero-denominator guard in report_template.html's
  sigSummary(), which is engine code and out of scope for an unattended run.

## 2026-10-02 — v2026.10.02
- event_map.json: added **RAS_PW** (www.rasmussen.edu · `lead_inquiry` / `pub_application_complete`)
  and **HON** (Hondros, start.hondros.edu · `requestinfomation_lp`). The existing RAS entry is
  LP-only: its info.rasmussen.edu hostname and `landing_page_inquiry` event see ~1% of a homepage
  PW test's traffic. Hondros has no application-complete event anywhere in GA4, so App Complete is
  always 0 there, and the template's revenue engine has no HON segment — those reports publish
  revenue 0.
- Documented the stale-GA-audience-name trap. Test 11044B's Optimizely variations
  (`v0_Control_11044B` / `v1_RFI_Move_11044B`) export to GA4 under the *previous* experiment's
  labels, `RAS | PW | Degree Finder Higher | homepage-*`. A match on the Asana test name or the
  RH# returns zero audiences and the test looks untracked. Resolve the audience from Optimizely's
  Variation Audiences panel, and confirm the audience has no sessions before the Live Date (a
  reused audience carries prior members for up to its 540-day membership duration).
- Rejected `request_info_click` as an RFI metric for 11044B: it is a button click, and the
  variation removes the click by putting the form inline (64 control vs 36 variation while
  completions stayed flat), so it would report a ~40% false loss.
- New reports: RAS 11044B RFI Form Placement (Sep 29 – Oct 1), HON 11107 refreshed (Sep 22 – Oct 1).

## 2026-08-24 — v2026.08.24
- report_template.html: the static banner markup no longer ships the ECE 10464 stub
  values. `#reportTitle` falls back to a generic "A/B Test Report" and `#hostNote`,
  `#dateRange`, `#brandShield`, `#brandName`, `#brandSub` are now empty in the template.
  Previously any reader that does not execute JS — curl, raw.githubusercontent, link
  unfurls, GitHub's own file preview — saw "ECE Redesign A/B Test Report / May 29, 2026
  – Jul 14, 2026" on every report regardless of which test it was.
- build_report.py: after splicing the DATA block it now also stamps the real title,
  date range, hostname note, school brand, and document `<title>` into that static
  markup, so a no-JS view matches what the browser renders. Exits non-zero if any of
  the seven header hooks is missing from the template.
- ras_11037_new_template_overview_report.html: rebuilt with the fixed template and
  script. DATA/FACTS blocks are byte-identical to the previous build — only the three
  static header lines changed.

## 2026-07-15 — v2026.07.15b
- report_template.html: <title> and footer now stamped from DATA.meta (school, testId, title) instead of the hardcoded "Test 10464 - Rasmussen University (RAS)" leftovers; stale source comment above the data block genericized.
- amu_10989_hero_image_report.html: rebuilt with the fixed template (data unchanged).
- .nojekyll added (skip Jekyll on Pages deploys).
    
## 2026-07-15 — v2026.07.15
- event_map.json: all three schools VERIFIED (AMU + APU discovered and confirmed;
  RAS re-confirmed). AMU/APU caveats documented: app completes fire on apply.apus.edu
  (drop hostName filter on abConv); audiences may lack the (RH#) suffix.
- report_template.html: per-school branding via html[data-school]
  (RAS green #004712/#A6CE39/#EEB111 · AMU black+gold #FFC600 · APU black+cyan #00E5E5);
  banner shield/name and hostname footnote switch automatically.
- Results table: added RFI Lift, Sig. (one-sided z), and 1-Yr Revenue columns vs the
  selected Control; ★ LEADING chip on the top variant by projected revenue.
- Revenue engine embedded (CRO Incremental Calculator v4 assumptions, 2026-06-18, all
  six school x channel segments); recomputes live with filters.
- Significance box now follows the leading variant and includes its revenue projection.
- Variation snapshot: added 1-Yr Incremental Revenue card; removed the empty second
  variation block.
- Report is now single-page (A/B Tests only; Overview/Acquisition/Clicks/Forms removed).
- build_report.py: school palettes for donut charts; meta gains hostname + channel.
- First published report: AMU Hero Image (10989), Jul 2-14 2026 window.
