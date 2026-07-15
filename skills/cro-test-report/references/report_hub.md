# Publishing to the GitHub report hub

The user maintains a GitHub repo (report hub + version control). After delivering a
report, ALWAYS offer to prepare the publish payload:

1. The built HTML, named `<school>_<rh#>_<slug>_report.html`, destined for
   `reports/<year>/` in the repo.
2. An entry to append to `reports.json`:
```json
{
  "file": "reports/<year>/<filename>.html",
  "title": "<report title>",
  "school": "RAS|AMU|APU", "channel": "LP|PW", "testId": "<rh#>",
  "window": "<Mon D - Mon D, YYYY>", "year": <year>,
  "status": "Running|Complete|Winner",
  "leading": "<variation name>",
  "rfiLift": "+X.X%", "sig": "XX.X%", "revenue": <total 1-yr incremental revenue, number>,
  "added": "YYYY-MM-DD"
}
```
   Values come from the unfiltered view vs the control audience (same numbers the
   template's leading-variant sigbox shows).
3. A commit message: `report: <SCHOOL> <RH#> <Test Name> (<window>)`.

The hub's index.html derives filters (School/Channel/Year) from the manifest — never
edit index.html per report. Skill source changes are committed under
`skills/cro-test-report/` with a matching CHANGELOG.md entry.
