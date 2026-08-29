"""Helpers Wikidata (sin dependencias). search(term) -> candidatos; get(qids) -> labels es/en, sitelinks, coords P625."""
import json, urllib.request, urllib.parse, time
API='https://www.wikidata.org/w/api.php'
UA={'User-Agent':'historia-mvp/0.1 (carlos@sbc-spain.com)'}
def _call(params):
    params['format']='json'
    req=urllib.request.Request(API+'?'+urllib.parse.urlencode(params),headers=UA)
    for i in range(3):
        try: return json.load(urllib.request.urlopen(req,timeout=30))
        except Exception as e: time.sleep(1+i)
    raise
def search(term,lang='en',limit=5):
    r=_call({'action':'wbsearchentities','search':term,'language':lang,'limit':limit})
    return [(e['id'],e.get('label'),e.get('description')) for e in r.get('search',[])]
def get(qids):
    out={}
    qids=list(qids)
    for i in range(0,len(qids),50):
        r=_call({'action':'wbgetentities','ids':'|'.join(qids[i:i+50]),'props':'labels|sitelinks|claims','languages':'es|en'})
        for q,e in r['entities'].items():
            lab=e.get('labels',{}); sl=e.get('sitelinks',{}); cl=e.get('claims',{})
            coord=None
            if 'P625' in cl:
                v=cl['P625'][0]['mainsnak'].get('datavalue',{}).get('value')
                if v: coord=(v['latitude'],v['longitude'])
            out[q]={'es':lab.get('es',{}).get('value'),'en':lab.get('en',{}).get('value'),
                    'eswiki':sl.get('eswiki',{}).get('title'),'enwiki':sl.get('enwiki',{}).get('title'),'coord':coord}
    return out
