#!/usr/bin/env python3
"""Build one frozen copy of Terminal SIM per video.

Each episode folder ep/<id>/ gets:
  index.html               - opens online at that episode's module, sandbox pre-set
  Terminal-SIM-<ID>.html   - same thing as an offline download

Existing episode folders are FROZEN: they are not rebuilt, so every video keeps
the exact version it was recorded with. Use --force <id> to rebuild one on purpose.

Usage: python3 tools/build_episodes.py [--force ep07b ...]
"""
import json, os, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'Terminal-SIM.html')        # current release build
CFG = json.load(open(os.path.join(ROOT, 'tools', 'episodes.json')))
force = set(a.lower() for a in sys.argv[1:] if not a.startswith('--'))

BOOT = r"""
<script>
/* Terminal SIM episode build: __LABEL__ */
(async function(){
  var E = __CFG__;
  try { document.title = 'Terminal SIM · ' + E.label + ': ' + E.title; } catch(e){}
  var bar = document.createElement('div');
  bar.id = 'ep-bar';
  bar.style.cssText = 'background:#16a34a;color:#04130a;font:600 12px/1.4 system-ui,sans-serif;padding:6px 10px;text-align:center';
  bar.innerHTML = 'Video version: <b>' + E.label + ' · ' + E.title + '</b>' +
    (location.protocol.indexOf('http') === 0 ? ' &nbsp;·&nbsp; <a style="color:#04130a" href="../">All episodes</a>' : '');
  document.body.insertBefore(bar, document.body.firstChild);
  if (E.view) { var b = document.querySelector('[data-v="' + E.view + '"]'); if (b) b.click(); }
  go(E.module - 1);
  var t = document.getElementById('term');
  if (E.setup.length) {
    busy = true; t.style.visibility = 'hidden';
    for (var i = 0; i < E.setup.length; i++) {
      try { S.hist.push(E.setup[i]); await runLine(E.setup[i]); } catch(e) {}
    }
    hIdx = S.hist.length;
    try { C.clear([]); } catch(e) {}
    busy = false; t.style.visibility = ''; updatePrompt();
  }
  print(M('g', '▶ ' + E.label + ': ' + E.title + (E.setup.length ? ' (picking up where the last part left off)' : '')));
  if (E.try) print(M('w', 'Try this first: ' + E.try));
})();
</script>
"""

src = open(SRC, encoding='utf-8').read()
assert src.count('</body>') == 1
built, skipped = [], []
for e in CFG['episodes']:
    d = os.path.join(ROOT, 'ep', e['id'])
    if os.path.isdir(d) and e['id'] not in force:
        skipped.append(e['id']); continue
    os.makedirs(d, exist_ok=True)
    cfg = {k: e.get(k, '') for k in ('id', 'label', 'title', 'module', 'view', 'try')}
    cfg['setup'] = e.get('setup', [])
    page = src.replace("'termuxSim.", "'termuxSim." + e['id'] + ".")   # separate progress per episode
    page = page.replace('</body>', BOOT.replace('__CFG__', json.dumps(cfg)).replace('__LABEL__', e['label']) + '</body>')
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page)
    open(os.path.join(d, 'Terminal-SIM-%s.html' % e['id'].upper()), 'w', encoding='utf-8').write(page)
    built.append(e['id'])

# episode list page
rows = []
for e in CFG['episodes']:
    up = e['id'].upper()
    rows.append('<li><div><b>%s</b> <span>%s</span></div><div class="b"><a class="o" href="%s/">Open</a>'
                '<a href="%s/Terminal-SIM-%s.html" download>Download</a></div></li>'
                % (html.escape(e['label']), html.escape(e['title']), e['id'], e['id'], up))
idx = open(os.path.join(ROOT, 'tools', 'episodes_index.html'), encoding='utf-8').read().replace('__ROWS__', '\n'.join(rows))
open(os.path.join(ROOT, 'ep', 'index.html'), 'w', encoding='utf-8').write(idx)
print('built:', built); print('frozen (kept):', skipped)
