# Changelog

## 2026-10-30: v2026.10.30
- CORRECTION: RAS | PW | AI Effectiveness (11044) has NOT gone live (Michael, 10/30). It is now an
  **Idea / On hold**: no actual start or end, no final outcome or winner, no results or revenue.
- reports.json: the 11044 entry is now an unlinked placeholder (status "Idea / On hold", window
  "Not launched"). The "Complete", one-day Sep 22 window, -100.0% RFI, 2.8% sig and -$917,286 claims
  were removed from the index. The report file and earlier manifest stay in git history.
- index.html (hub): entries without a report file render without a link or metrics and are not
  counted as reports; status badges use a sanitized class (adds `b-status-IdeaOnhold`).
- archive: tests.json 11044 row synced from apei-cro-experiments/tests.csv (outcome "Idea / On hold").
  archive/index.html adds the outcome as a filter chip and badge, shows "Not launched", and excludes
  ideas on hold from test counts, the year table, Running and final-result KPIs. 2026 now reads 18
  tests (was 19); all-years 96 tests plus 1 idea on hold.
- Freshness: the hub and archive now fetch reports.json / tests.json with a timestamp query and
  `cache: "no-store"`, so a correction shows on the next load instead of after the cache expires.

## 2026-10-19 — v2026.10.19
- CORRECTION (supersedes the AMU 10926 closeout bullet below): 10926 has NOT ended. It is still running and sits in
  Recommend Ending; there is no final decision. Official start is 10/10 (the initial 10/08 launch and all 10/08 to 10/09 data
  are excluded from every query). The report at the same URL is now an INTERIM build for Oct 10 – Oct 18 (latest complete
  day): exposure users -10.65% RFI at 75.9% one-sided worse; tables are an audience-session diagnostic for the same window.
  reports.json: 10926 -> Running, window Oct 10 - Oct 18. live-tests: 10926 moved to Recommend Ending with the official start.
  The earlier closeout build remains in git history.
- AMU 10926 MultiStep Form closed out: final decision Inconclusive (approved 10/19), -10.65% RFI at 75.9% one-sided worse on
  exposure users, clean window 10/10 to 10/18 (10/08 to 10/09 excluded for duplicate form tracking). The Asana ticket window is
  10/08 to 10/22; data coverage is complete through 10/18, so the report covers Oct 8 – Oct 18 and its pill reads "Data coverage".
  The 10/19 audience-session readout (-16.58% at 92%) is kept in the decision note as a previous diagnostic only. This one page
  was built with a local, unpublished label patch (date pill label; significance shown as the probability the variation beats
  control). The shared skill sources in skills/ are unchanged.
- reports.json: 10926 -> Complete, window Oct 8 - Oct 18; revenue = modeled RFI-path projection (-$271,868), credited lift $0.
- report_template.html: Hondros renders as Hondros. Added `HON` to the JS `SCHOOL_BRAND` map
  ('H' / HONDROS / COLLEGE OF NURSING) and an `html[data-school="HON"]` palette. The palette is a
  neutral navy/light-blue set chosen for legibility, not an official Hondros brand spec. Before this,
  the runtime script overrode the correct static header with RASMUSSEN UNIVERSITY and RAS green.
- report_template.html: no more NaN for unmeasured or unmodeled metrics. When `DATA.meta.appMeasured`
  is false, App Complete columns, totals and score cards read N/A and the sigbox reads
  "App Complete: not measured". When the school/channel has no revenue model, the table shows
  "Not modeled", the footnote says so, and the sigbox reads "Revenue: not modeled". This fixes the
  "App Complete CVR: NaN%" and "$NaN/enrollment" issue noted in v2026.10.05.
- report_template.html + build_report.py: optional `decisionNote` in config.json renders as a box
  above the results table. Use it to state the approved final decision and cohort, and to label the
  dashboard's filterable tables as an audience-session diagnostic, so the date-range pill stays short.
  build_report.py also emits `appMeasured` (false when the config's appEvent starts with "n/a").
- Rebuilt on the final Asana windows: HON 11107 (Sep 22 – Oct 8; final decision Winner, +10.1% at
  91.7% one-sided on exposure users) and RAS 11044B (Sep 29 – Oct 14; final decision Inconclusive,
  -7.78% at 72.0% one-sided worse on exposure users). Session-diagnostic numbers in the tables are not
  the decision cohort; canonical funnel counts appear only in the decision note.
- reports.json: 11107 -> Winner, 11044B -> Complete with the final windows. The four 10893 entries
  now carry revenue 0 (credited lift) with leading text noting the 10/01 business-rollout approval,
  10/13 implementation, and that report revenue figures are modeled projections only.

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
