#!/usr/bin/env python3
"""
build_report.py — GA4 pull JSON + config → self-contained A/B test report HTML.

Usage:
  python3 build_report.py --config config.json --pull ga4_pull.json --out report.html

config.json (see references/example_config_10464.json):
{
  "title": "ECE Redesign A/B Test Report",
  "testId": "10464",
  "school": "RAS",
  "property": "253925809",
  "hostname": "info.rasmussen.edu",
  "dateStart": "2026-05-28",
  "dateEnd": "2026-06-11",
  "dateSource": "Asana: Live Date -> End Date",
  "rfiEvent": "landing_page_inquiry",
  "appEvent": "lp_application_complete",
  "controlToken": "Control",          # substring identifying the control audience
  "campaignMinSessions": 20            # tail campaigns below this collapse to "(other)"
}

pull JSON must contain GA4 runReport responses under these keys
(dimension order matters — see references/ga4_queries.md):
  abTraffic : dims [audienceName, deviceCategory, newVsReturning, sessionCampaignName]
              metrics [sessions, engagedSessions, newUsers, totalUsers]
  abConv    : same dims + eventName; metric [eventCount]
              (eventName filtered to rfiEvent + appEvent via inList)
  abDaily   : dims [date, audienceName]; metrics [sessions, screenPageViews]

Exit code non-zero on any verification failure. Never ship an unverified report.
"""
import json, argparse, collections, datetime, sys, re, os

def rows(resp, key):
    if not isinstance(resp, dict) or 'error' in resp:
        sys.exit(f"FATAL: pull section '{key}' missing or errored: {resp.get('error') if isinstance(resp,dict) else resp}")
    return resp.get('rows', [])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--pull', required=True)
    ap.add_argument('--template', default=os.path.join(os.path.dirname(__file__), '..', 'assets', 'report_template.html'))
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    cfg  = json.load(open(a.config, encoding='utf-8-sig'))
    pull = json.load(open(a.pull, encoding='utf-8-sig'))

    Z = lambda: dict(sessions=0, engaged=0, newUsers=0, users=0, rfi=0, app=0)

    # ---- campaign tail collapse ----
    camp_sessions = collections.Counter()
    for r in rows(pull['abTraffic'], 'abTraffic'):
        camp_sessions[r['dimensionValues'][3]['value']] += int(r['metricValues'][0]['value'])
    minS = cfg.get('campaignMinSessions', 20)
    keep = {c for c, s in camp_sessions.items() if s >= minS}
    campof = lambda c: c if c in keep else '(other)'

    # ---- facts: (aud, dev, ut, camp) tuples ----
    facts = collections.defaultdict(Z)
    for r in rows(pull['abTraffic'], 'abTraffic'):
        dv = [x['value'] for x in r['dimensionValues']]
        mv = [int(x['value']) for x in r['metricValues']]
        f = facts[(dv[0], dv[1], dv[2], campof(dv[3]))]
        f['sessions'] += mv[0]; f['engaged'] += mv[1]; f['newUsers'] += mv[2]; f['users'] += mv[3]

    for r in rows(pull['abConv'], 'abConv'):
        dv = [x['value'] for x in r['dimensionValues']]
        c = int(r['metricValues'][0]['value'])
        k = (dv[0], dv[1], dv[2], campof(dv[3]))
        if dv[4] == cfg['rfiEvent']:   facts[k]['rfi'] += c
        elif dv[4] == cfg['appEvent']: facts[k]['app'] += c

    # ---- site (= report) scope ----
    site = collections.defaultdict(Z)
    for (aud, de, ut, ca), f in list(facts.items()):
        s = site[('__site__', de, ut, ca)]
        for k in f: s[k] += f[k]
    facts.update(site)

    # ---- audiences: control first, personalization last ----
    ctok = cfg.get('controlToken', 'Control').lower()
    def aud_rank(name):
        n = name.lower()
        if ctok in n and 'personalization' not in n: return (0, name)
        if 'personalization' in n: return (2, name)
        return (1, name)
    auds = sorted({k[0] for k in facts if k[0] != '__site__'}, key=aud_rank)
    if len(auds) < 2:
        sys.exit(f"FATAL: expected >=2 audiences, found {auds}. Check audience filter / test number.")

    agg = {x: Z() for x in auds + ['__site__']}
    for (aud, de, ut, ca), f in facts.items():
        for k in f: agg[aud][k] += f[k]

    # ---- donuts ----
    dev_s, ut_s = collections.Counter(), collections.Counter()
    tot = agg['__site__']['sessions']
    for (aud, de, ut, ca), f in facts.items():
        if aud == '__site__':
            dev_s[de] += f['sessions']; ut_s[ut] += f['sessions']
    SCHOOL_PAL = {
        'RAS': ({'mobile': '#eeb111', 'desktop': '#004712', 'tablet': '#a6ce39', 'smart tv': '#7a8a76'},
                {'new': '#004712', 'returning': '#a6ce39', '(not set)': '#c9d3c4'}),
        'AMU': ({'mobile': '#ffc600', 'desktop': '#1a1a1a', 'tablet': '#8f6f00', 'smart tv': '#9a9a9a'},
                {'new': '#1a1a1a', 'returning': '#ffc600', '(not set)': '#cccccc'}),
        'APU': ({'mobile': '#f5e400', 'desktop': '#0d0d0d', 'tablet': '#00b8b8', 'smart tv': '#9a9a9a'},
                {'new': '#0d0d0d', 'returning': '#00b8b8', '(not set)': '#cccccc'}),
    }
    devcolors, utcolors = SCHOOL_PAL.get(str(cfg.get('school', 'RAS')).upper(), SCHOOL_PAL['RAS'])
    deviceSplit = [{'label': d, 'pct': round(v / tot * 100, 1), 'color': devcolors.get(d, '#999')}
                   for d, v in dev_s.most_common() if v > 0]
    nvr = [{'label': u, 'pct': round(v / tot * 100, 1), 'color': utcolors.get(u, '#999')}
           for u, v in ut_s.most_common() if v > 0]

    # ---- campaigns table (report scope) ----
    camp_tbl = collections.defaultdict(Z)
    for (aud, de, ut, ca), f in facts.items():
        if aud == '__site__':
            for k in f: camp_tbl[ca][k] += f[k]
    campaigns = [[c, v['sessions'], v['rfi'], v['app']]
                 for c, v in sorted(camp_tbl.items(), key=lambda x: -x[1]['sessions'])]
    campTotals = [sum(x[1] for x in campaigns), sum(x[2] for x in campaigns), sum(x[3] for x in campaigns)]

    # ---- daily ----
    daily = collections.defaultdict(lambda: [0, 0])
    for r in rows(pull['abDaily'], 'abDaily'):
        d0 = r['dimensionValues'][0]['value']
        daily[d0][0] += int(r['metricValues'][0]['value'])
        daily[d0][1] += int(r['metricValues'][1]['value'])
    days = sorted(daily)
    dailySessions = [daily[d][0] for d in days]
    views = sum(daily[d][1] for d in days)
    def lbl(s): return datetime.datetime.strptime(s, '%Y%m%d').strftime('%b ') + str(int(s[6:]))
    labels = [lbl(days[i]) for i in range(0, len(days), max(1, len(days) // 6))]
    if days and lbl(days[-1]) not in labels: labels.append(lbl(days[-1]))

    # ---- verification gate ----
    errs = []
    if agg['__site__']['sessions'] != sum(agg[x]['sessions'] for x in auds):
        errs.append('site sessions != sum(audiences)')
    for x in auds:
        if agg[x]['sessions'] <= 0: errs.append(f'zero sessions for {x}')
    got_conv = sum(agg[x]['rfi'] for x in auds) + sum(agg[x]['app'] for x in auds)
    if got_conv == 0:
        errs.append(f"zero conversions — check rfiEvent '{cfg['rfiEvent']}' / appEvent '{cfg['appEvent']}' exist in abConv")
    if not dailySessions: errs.append('empty daily series')
    if errs:
        sys.exit('FATAL verification: ' + '; '.join(errs))

    # ---- emit JS data block ----
    def fmt_date(s): return datetime.date.fromisoformat(s).strftime('%b %-d, %Y') if '-' in s else s
    dr = f"{fmt_date(cfg['dateStart'])} – {fmt_date(cfg['dateEnd'])} · Asana test window"
    now = datetime.date.today().strftime('%-m/%-d/%Y')

    aud_js = ",\n      ".join(
        '{ name:%s, role:"%s" }' % (json.dumps(x), 'control' if i == 0 else 'variation')
        for i, x in enumerate(auds))
    fact_rows = ",\n    ".join(
        '{a:%d,d:%s,u:%s,c:%s,s:%d,e:%d,n:%d,us:%d,r:%d,ap:%d}' % (
            -1 if aud == '__site__' else auds.index(aud),
            json.dumps(de), json.dumps(ut), json.dumps(ca),
            f['sessions'], f['engaged'], f['newUsers'], f['users'], f['rfi'], f['app'])
        for (aud, de, ut, ca), f in sorted(facts.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2], kv[0][3])))
    camps_order = [c[0] for c in campaigns if c[0] != '(other)'] + (['(other)'] if any(c[0]=='(other)' for c in campaigns) else [])
    dev_order = [d['label'] for d in deviceSplit]
    ut_order  = [u['label'] for u in nvr]

    E = lambda o: json.dumps(o, ensure_ascii=False)
    block = f'''const DATA = {{
  meta: {{
    title: {E(cfg['title'])},
    testId: {E(cfg['testId'])},
    school: {E(cfg['school'])},
    hostname: {E(cfg.get('hostname',''))},
    channel: {E(cfg.get('channel','LP'))},
    dateRange: {E(dr)},
    dateSource: {E(cfg.get('dateSource','Asana: Live Date -> End Date'))},
    lastUpdated: {E(now + ' · GA4 pull (property ' + cfg['property'] + ')')},
    legacyNote: "",
    dailySessions: {E(dailySessions)},
    dailyLabels: {E(labels)},
    dailyStart: {E(cfg['dateStart'])}
  }},
  overview: {{
    kpis: {{ sessions:{tot}, views:{views}, avgSessionDuration:null, totalUsers:0 }},
    newVsReturning: {E(nvr)},
    deviceSplit: {E(deviceSplit)},
    mostViewedPages: [], mostViewedTotal:0, mostViewedCount:0,
    topSources: [], topSourcesTotal:0, topSourcesCount:0,
    usersByCountry: [], usersByCountryTotals:[0,0], usersByCountryCount:0,
    browsers: [], deviceBrands: [], browsersTotal:0,
    gender: [], interests: [], interestsTotal:0, interestsCount:0,
    age: [], ageTotals:[0,0]
  }},
  acquisition: {{
    landingPages: [], landingTotals:[0,0,"0%",0,"0%"], landingCount:0,
    channels: [],
    sourcesMediums: [], sourcesTotals:[0,0,0], sourcesCount:0,
    campaigns: {E(campaigns)},
    campaignsTotals: {E(campTotals)},
    campaignsCount: {len(campaigns)}
  }},
  abtests: {{
    audiences: [
      {aud_js}
    ]
  }},
  clicks: {{ clickEvents: [], clickEventsTotal:0, clickEventsCount:0,
             clickToCall: [], clickToCallTotal:0, clickToCallCount:0,
             degreeSearch: [], degreeSearchTotal:0, degreeSearchCount:0 }},
  forms: {{ steps: [], programs: [] }}
}};

/* FACTS from GA4 property {cfg['property']} · window {cfg['dateStart']}..{cfg['dateEnd']}
   Grain: (a: audience index | -1 report scope, d device, u newVsReturning, c campaign["(other)"=tail]).
   Metrics: s sessions, e engaged, n newUsers, us users, r RFI ({cfg['rfiEvent']}), ap App ({cfg['appEvent']}).
   Source of truth: GA4 via the GA MCP; fallback direct Data API / Claude in Chrome. Windsor.ai: retired. */
const AUD_CONTROL = DATA.abtests.audiences[0].name;
const AUD_V1      = DATA.abtests.audiences[1].name;
const FACTS = {{
  audNames: {E(auds)},
  core: [
    {fact_rows}
  ],
  dims: {{
    devices: {E(dev_order)},
    userTypes: {E(ut_order)},
    campaigns: {E(camps_order)}
  }},
  clicksSegmented: false
}};
'''

    tpl = open(a.template, encoding='utf-8').read()
    m = re.search(r'/\*__DATA_START__\*/.*?/\*__DATA_END__\*/', tpl, re.S)
    if not m: sys.exit('FATAL: template markers not found')
    out = tpl[:m.start()] + '/*__DATA_START__*/\n' + block + '/*__DATA_END__*/' + tpl[m.end():]
    open(a.out, 'w', encoding='utf-8').write(out)

    # ---- summary to stdout for the chat recap ----
    print(f"OK -> {a.out}")
    for x in auds:
        g = agg[x]
        print(f"  {x.split('|')[-1].strip():<45} sessions={g['sessions']:>6} rfi={g['rfi']:>4} ({g['rfi']/g['sessions']*100:.2f}%) app={g['app']:>4} ({g['app']/g['sessions']*100:.2f}%)")
    print(f"  {'REPORT SCOPE':<45} sessions={tot:>6} rfi={sum(agg[x]['rfi'] for x in auds):>4} app={sum(agg[x]['app'] for x in auds):>4} | facts rows={len(facts)} campaigns={len(campaigns)} days={len(dailySessions)}")

if __name__ == '__main__':
    main()
