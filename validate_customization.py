"""P10 structural checks; not a substitute for Unity and C# tests."""
from pathlib import Path
import json,re,struct
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena'
catalog=json.loads((A/'Resources/Data/catalog.json').read_text());data=json.loads((A/'Resources/Data/accessories.json').read_text())['items'];items={a['id']:a for a in catalog['accessories']}
assert len(data)==len(items)==26 and {a['id'] for a in data}==set(items)
for item in data:
 assert item['characterId']==items[item['id']]['characterId'] and item['slot']==items[item['id']]['slot']
 kind=item['characterId'];stage=8 if kind in ['pofuk','cengel'] else 9
 nodes=json.loads((R/f'ArtSource/P{stage:02}/{kind}.rig.json').read_text());names={n['name'] for n in nodes}
 names.update(['SocketBody','SocketNeck','SocketEarL','SocketEarR','SocketLegL','SocketLegR'])
 if kind=='koli_kenan':names.update(['SocketAntennaL','SocketAntennaR'])
 assert item['parts']
 for part in item['parts']:
  assert part['socket'] in names
  assert not part['hideBase'] or part['hideBase'] in names
  assert 0<part['sx']<=2 and 0<part['sy']<=2
  p=A/('Resources/'+part['sprite']+'.png');b=p.read_bytes();w,h,depth,color=struct.unpack('>IIBB',b[16:26]);assert (w,h)==(256,256) and color in [4,6]
  assert Path(str(p)+'.meta').is_file()
 assert items[item['id']]['artStatus']=='accessory-v1-runtime-unverified'
print('PASS: all 26 catalog accessories have matching owner/slot, valid sockets, base-part names, 256px alpha sprites and metadata')
for kind in ['pofuk','cengel','kivilcim','firtina','koli_kenan']:
 assert len([i for i in data if i['characterId']==kind])<=6
print('PASS: catalog retains at most six accessories per character; runtime pages show two items per category')
code=(A/'Runtime/CharacterCustomizationScreen.cs').read_text()
assert '#if UNITY_EDITOR || DEVELOPMENT_BUILD' in code and 'SaveServer()' in code and 'shop.Equip' in code
assert 'TouchScreenKeyboard' in (A/'Runtime/MainMenuScreen.cs').read_text()
assert 'camera.targetTexture=null' in code and 'texture.Release()' in code and 'studio.SetActive(false)' in code
print('PASS: explicit development save compile gate, keyboard accommodation and preview cleanup present (static only)')
print('NOT RUN: draft/save C# behavior suite, Unity render/animation/UI/import, device keyboard, persistence and performance')
