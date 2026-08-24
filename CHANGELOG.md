# Changelog

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
