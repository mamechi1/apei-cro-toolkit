# APEI CRO Toolkit

Version-controlled home for APEI CRO test reports and the tools that build them.

## Live report hub
Once GitHub Pages is enabled (Settings > Pages > deploy from `main` / root):
`https://<your-username>.github.io/<repo-name>/` — filterable by School (RAS/AMU/APU), Channel (LP/PW), and Year.

## Structure
```
index.html            report hub (filters; reads reports.json — never needs editing)
reports.json          manifest: one entry per report (this is what the hub renders)
reports/<year>/       self-contained HTML dashboards, one per test
skills/cro-test-report/  source of the Cowork skill that builds the reports
CHANGELOG.md          human-readable history of skill/template changes
```

## Adding a report (each test run)
1. Commit the built HTML to `reports/<year>/` (filename: `<school>_<rh#>_<slug>_report.html`).
2. Append an entry to `reports.json` (see existing entries for the schema: file, title,
   school, channel, testId, window, year, status, leading, rfiLift, sig, revenue, added).
3. Commit both together — message like `report: AMU 10989 Hero Image (Jul 2-14 window)`.

The hub picks up new schools/channels/years automatically from the manifest.

## Updating the skill
Edit under `skills/cro-test-report/`, commit with a descriptive message, and rebuild the
`.skill` installer by zipping the `cro-test-report` folder with a `.skill` extension.
Tag releases (e.g. `v2026.07.15`) so any installer can be traced to an exact commit.
