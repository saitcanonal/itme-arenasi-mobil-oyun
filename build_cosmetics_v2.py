"""PNG + cosmetics_v2.json -> Unity catalog/bindings and reviewable server SQL.
Run from any directory. SQL output is a draft; never auto-applied to a live DB.
"""
from pathlib import Path
import json,uuid
R=Path(__file__).resolve().parents[1];D=R/'UnityProject/Assets/ItmeArena/Resources/Data';RES=D.parent
items=json.loads((D/'cosmetics_v2.json').read_text())['items'];catalog=json.loads((D/'catalog.json').read_text());bindings=json.loads((D/'accessories.json').read_text());seen=set();sql=[]
def quote(v):return "'"+str(v).replace("'","''")+"'"
for m in items:
 assert m['id'] not in seen;seen.add(m['id']);slot=m['slot'];assert slot in ['feet','hands','face','head','body'];assert m['currency']=='gold' and m['price']>=2000;assert m['rarity'] in ['common','rare','epic','legendary','mythic'];assert m['canvas']==512 and m['anchor']==[.5,.5]
 assert m['pairMode'] in ['single','mirror','separate'];assert m['pairMode']!='separate' or m.get('leftSprite')
 for sprite in [m['sprite']]+([m['leftSprite']] if m.get('leftSprite') else []):
  path=RES/(sprite+'.png');assert path.exists(),path
  if not path.with_suffix('.png.meta').exists():path.with_suffix('.png.meta').write_text('fileFormatVersion: 2\nguid: '+uuid.uuid4().hex+'\nTextureImporter:\n  textureType: 8\n  spriteMode: 1\n  spritePixelsToUnits: 512\n  spritePivot: {x: 0.5, y: 0.5}\n  alphaIsTransparency: 1\n  textureSettings:\n    filterMode: 1\n  maxTextureSize: 512\n')
 a=next((x for x in catalog['accessories'] if x['id']==m['id']),None)
 if a is None:a={};catalog['accessories'].append(a)
 a.update(id=m['id'],displayName=m['displayName'],characterId='*',slot=slot,examplePrice=m['price'],rarity=m['rarity'],currency='gold',assetKey=m['sprite'])
 parts=[]
 for side in (['L','R'] if slot in ['feet','hands'] else ['']):
  socket={'feet':'SocketFoot'+side,'hands':'SocketWrist'+side,'face':'SocketFace','head':'SocketHead','body':'SocketBody'}[slot];sx,sy={'feet':(.46,.34),'hands':(.43,.43),'face':(.8,.62),'head':(.87,.52),'body':(1.05,1.1)}[slot]
  left=side=='L';parts.append(dict(sprite=m['leftSprite'] if left and m['pairMode']=='separate' else m['sprite'],socket=socket,x=0,y=0,sx=-sx if left and m['pairMode']=='mirror' else sx,sy=sy,order=m['sortingOrder'],hideBase='Foot'+side if slot=='feet' else 'HandArt'+side if slot=='hands' else ''))
 b=next((x for x in bindings['items'] if x['id']==m['id']),None)
 if b is None:b={};bindings['items'].append(b)
 b.update(id=m['id'],characterId='*',slot=slot,parts=parts)
 sql.append(f"INSERT INTO accessories(id,character_id,display_name,purchasable) VALUES({quote(m['id'])},'human_male',{quote(m['displayName'])},true) ON CONFLICT(id) DO NOTHING;")
 sql.append(f"INSERT INTO shop_products(id,kind,accessory_id,display_name,character_id,slot,price,purchasable) VALUES({quote(m['id'])},'accessory',{quote(m['id'])},{quote(m['displayName'])},'human_male',{quote(slot)},{m['price']},true) ON CONFLICT(id) DO NOTHING;")
(D/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2));(D/'accessories.json').write_text(json.dumps(bindings,ensure_ascii=False,indent=2))
(R/'Docs/COSMETICS_PRODUCTS_DRAFT.sql').write_text('-- Review and place in a NEW Flyway migration; does not reprice existing products.\n'+'\n'.join(sql)+'\n');print('Built',len(items),'items; server SQL draft ready.')
