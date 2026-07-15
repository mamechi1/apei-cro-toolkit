# Changelog

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
