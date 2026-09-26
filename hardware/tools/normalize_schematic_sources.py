"""Run with project closed. Give components unique IDs and exclude unpopulated parts from BOM."""
import json,uuid
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'eda/Ruri-Passport-RevA'
uid=100000;seen=set();nobom=[]
for p in (root/'sch/Mainboard').glob('*.esch2'):
 for line in p.read_text().splitlines():
  h,b=line.split('||',1);b=b.removesuffix('|');v=json.loads(b) if b else None
  if isinstance(v,dict) and v.get('key')=='Unique ID':
   value=str(v.get('value',''))
   if value.startswith('gge') and value[3:].isdigit():uid=max(uid,int(value[3:]))
for path in sorted((root/'sch/Mainboard').glob('*.esch2')):
 rows=[];doc=None;refs={};names={};parts={};existing=set();ticket=0
 for line in path.read_text().splitlines():
  h,b=line.split('||',1);h=json.loads(h);b=b.removesuffix('|');v=json.loads(b) if b else None
  if h['type']=='DOCHEAD':doc=v['docType']
  rows.append([h,v,doc]);ticket=max(ticket,h.get('ticket',0))
  if doc!='SCH_PAGE' or not isinstance(v,dict):continue
  if h['type']=='COMPONENT':
   dn=v.get('attrs',{}).get('DeviceName','')
   if dn:names[h['id']]=json.loads(dn).get('name','')
  if h['type']=='ATTR':
   if v.get('key')=='Designator':refs[v['parentId']]=v['value']
   if v.get('key')=='Name' and v.get('value'):names[v['parentId']]=v['value']
   if v.get('key')=='Add into BOM':existing.add(v['parentId'])
   if v.get('key')=='Unique ID':parts[v['parentId']]=v
 exclude={pid for pid,ref in refs.items() if str(ref).startswith(('TP','ANT')) or 'DNP' in str(names.get(pid,'')) or ref in ('C4','C5')}
 for h,v,doc in rows:
  if doc!='SCH_PAGE' or not isinstance(v,dict):continue
  if h['type']=='ATTR' and v.get('key')=='Unique ID':
   old=str(v.get('value',''))
   if not old.startswith('gge') or not old[3:].isdigit() or int(old[3:])<100000 or old in seen:
    uid+=1;v['value']=f'gge{uid}'
   seen.add(v['value'])
  if h['type']=='ATTR' and v.get('key')=='Add into BOM' and v['parentId'] in exclude:v['value']='no'
 for pid in sorted(exclude-existing):
  ticket+=1
  v=dict(parts[pid]);v.update(key='Add into BOM',value='no',keyVisible=False,valueVisible=False)
  rows.append([{'type':'ATTR','ticket':ticket,'id':uuid.uuid4().hex[:16]},v,'SCH_PAGE'])
 nobom.extend(refs[pid] for pid in exclude)
 path.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+(json.dumps(v,separators=(',',':')) if v is not None else '')+'|' for h,v,_ in rows)+'\n')
print(f'{len(seen)} unique IDs; no BOM: '+', '.join(sorted(nobom)))
