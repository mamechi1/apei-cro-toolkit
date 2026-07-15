# GA4 Queries — CRO Test Report

Three required queries per test, all against the school's GA4 property, all filtered to
the school hostname AND `audienceName CONTAINS` the audience match token
(default: the page-path + `(<RH#>)` fragment, e.g. `"overview (10464)"` — page path
included because RH#s are NOT unique across tests).

Date range = Asana test window (Live Date → End Date, else Live Date → yesterday).

## Access hierarchy (in order — never Windsor.ai, it is retired)
1. **GA MCP** (`google-analytics:run_report`) — primary.
2. **Direct Data API** — proven fallback when the MCP is down. The user's ADC token
   works: see the PowerShell block at the bottom. Ask the user to run it and upload
   the JSON (or run it yourself if you have shell access on the user's machine).
3. **Claude in Chrome** with GA4 open — last resort for a 4-dimension cross-tab; slow.

If the MCP times out (4-min no-response), do NOT keep retrying — go to fallback 2
and tell the user their MCP needs a restart/log check. Known failure modes from
2026-07-15 debugging: stale token cached at server start (fix: restart Claude Desktop
AFTER `gcloud auth application-default login`), missing analytics scope (fix: login with
`--client-id-file="$HOME\.ga4-mcp\oauth_client.json"` and BOTH scopes, quoted — plain
gcloud client gets "This app is blocked"), orphaned `google-analytics-mcp.exe`
(fix: `taskkill /F /IM google-analytics-mcp.exe`).

## Query 1 — abTraffic
dims:    audienceName, deviceCategory, newVsReturning, sessionCampaignName
metrics: sessions, engagedSessions, newUsers, totalUsers
filter:  hostName EXACT <hostname> AND audienceName CONTAINS <audMatch>
limit:   10000

## Query 2 — abConv
dims:    audienceName, deviceCategory, newVsReturning, sessionCampaignName, eventName
metrics: eventCount
filter:  hostName AND audienceName AND eventName inList [<rfiEvent>, <appEvent>]
limit:   10000
⚠ Use inList with the exact mapped event names (references/event_map.json).
  Do NOT use CONTAINS guessing — "rfi/app/submit" missed `landing_page_inquiry` once.

## Query 3 — abDaily
dims:    date, audienceName
metrics: sessions, screenPageViews
filter:  hostName AND audienceName
orderBy: date asc; limit 200

## First run on a NEW property/school — event discovery
Before the first report for a school, verify event names:
dims [eventName], metric [eventCount], hostname filter, order desc, limit 50.
Present the top candidates to the user, confirm which is RFI and which is App
Complete, then record them in references/event_map.json. Known mappings live there.

## Audience discovery fallback
If Query 1 returns zero audiences for the match token, the Optimizely audiences may
not be visible in GA yet. Pull the experiment from the Optimizely MCP
(`exp_...` tools; Project/Experiment IDs come from the Asana task custom fields) to get
canonical audience names, then retry the GA filter with a distinctive fragment of those
names. Personalization variants of the same test (audience name contains
"PERSONALIZATION") should be INCLUDED as additional variation rows.


## AMU / APU specifics (verified 2026-07-15)

- Both share property **249537963**. LP hostnames: AMU `start.amu.apus.edu`, APU `start.apu.apus.edu`.
- **abConv: DROP the hostName filter** for AMU/APU — application completes fire on
  `apply.apus.edu` and profile events on `login.apus.edu`, so a LP-hostname filter
  zeroes the app funnel. The audienceName filter alone scopes the query to the test.
  (abTraffic and abDaily keep the LP hostname filter.)
- **Audience suffix caveat:** APUS Optimizely audiences don't always carry the "(RH#)"
  suffix (e.g. test 10989's audiences are named `CRO | AMU | LP | Hero Image |
  /military-degrees/overview-<Variation>`). If the RH# match returns zero rows, match
  on the test-name/page-path fragment from the Asana task name instead.
- Generic vs school events: `rfi_short_thankyou` has a school-suffixed twin on the school's
  own LP hostname; always use the school-specific event (`_amu` / `_apu`) so cross-school
  bleed is impossible. Same for `application_completed` vs `amu_/apu_application_completed`.

## Phase 2 (not yet implemented — cards auto-hide until then)
Overview detail tables (pages, sources, geo, browsers, demographics), click-event
tables (needs event-scoped custom dims `customEvent:click_text` etc. — run
getMetadata on the property to confirm names), and form-step tables. When adding,
extend build_report.py and populate the corresponding DATA arrays; the template
shows any table whose array is non-empty.

## Direct Data API fallback (PowerShell, run on user's machine)
Replace PROPERTY / HOSTNAME / AUDMATCH / RFI_EVENT / APP_EVENT / dates:

```powershell
$ErrorActionPreference="Stop"
$t = gcloud auth application-default print-access-token
$B = "https://analyticsdata.googleapis.com/v1beta/properties/PROPERTY:runReport"
$H = @{Authorization="Bearer $t"}
function Q($body){ try { Invoke-RestMethod -Method Post -Uri $B -Headers $H -ContentType "application/json" -Body $body } catch { @{error=$_.Exception.Message} } }
$dates = '"dateRanges":[{"startDate":"YYYY-MM-DD","endDate":"YYYY-MM-DD"}]'
$host_ = '{"filter":{"fieldName":"hostName","stringFilter":{"matchType":"EXACT","value":"HOSTNAME"}}}'
$aud   = '{"filter":{"fieldName":"audienceName","stringFilter":{"matchType":"CONTAINS","value":"AUDMATCH"}}}'
$ev    = '{"filter":{"fieldName":"eventName","inListFilter":{"values":["RFI_EVENT","APP_EVENT"]}}}'
$r = [ordered]@{}
$r.abTraffic = Q "{$dates,`"dimensions`":[{`"name`":`"audienceName`"},{`"name`":`"deviceCategory`"},{`"name`":`"newVsReturning`"},{`"name`":`"sessionCampaignName`"}],`"metrics`":[{`"name`":`"sessions`"},{`"name`":`"engagedSessions`"},{`"name`":`"newUsers`"},{`"name`":`"totalUsers`"}],`"dimensionFilter`":{`"andGroup`":{`"expressions`":[$host_,$aud]}},`"limit`":10000}"
$r.abConv    = Q "{$dates,`"dimensions`":[{`"name`":`"audienceName`"},{`"name`":`"deviceCategory`"},{`"name`":`"newVsReturning`"},{`"name`":`"sessionCampaignName`"},{`"name`":`"eventName`"}],`"metrics`":[{`"name`":`"eventCount`"}],`"dimensionFilter`":{`"andGroup`":{`"expressions`":[$host_,$aud,$ev]}},`"limit`":10000}"
$r.abDaily   = Q "{$dates,`"dimensions`":[{`"name`":`"date`"},{`"name`":`"audienceName`"}],`"metrics`":[{`"name`":`"sessions`"},{`"name`":`"screenPageViews`"}],`"dimensionFilter`":{`"andGroup`":{`"expressions`":[$host_,$aud]}},`"orderBys`":[{`"dimension`":{`"dimensionName`":`"date`"}}],`"limit`":200}"
$out = "$HOME\Documents\Claude\ga4_TESTID_pull.json"
$r | ConvertTo-Json -Depth 40 | Out-File $out -Encoding utf8
Write-Host "Saved: $out (abTraffic=$($r.abTraffic.rowCount) abConv=$($r.abConv.rowCount) abDaily=$($r.abDaily.rowCount))"
```

Note: PowerShell splits unquoted comma lists — always quote `--scopes` values.
Note: PS `Out-File utf8` writes a BOM — read pulls with `encoding='utf-8-sig'`
(build_report.py already does).
