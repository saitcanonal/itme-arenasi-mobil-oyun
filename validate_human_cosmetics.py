from pathlib import Path
import json,re
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena';D=A/'Resources/Data'
c=json.loads((D/'catalog.json').read_text());b=json.loads((D/'accessories.json').read_text());m=json.loads((D/'cosmetics_v2.json').read_text())['items'];ids={x['id'] for x in c['accessories']};assert len(ids)==31
assert {'human_male','human_female'}<={x['id'] for x in c['characters']}
assert {x['slot'] for x in m}=={'feet','hands','face','head','body'}
assert len({x['id'] for x in m})==len(m)
for item in m:
 assert item['id'] in ids and item['currency']=='gold' and item['price']>=2000
 im=Image.open(A/'Resources'/(item['sprite']+'.png'));assert im.size==(512,512) and im.mode=='RGBA',(item['id'],im.size,im.mode)
 assert im.getextrema()[3][0]==0
 binding=next(x for x in b['items'] if x['id']==item['id']);assert binding['characterId']=='*'
 parts=binding['parts'];assert len(parts)==(2 if item['slot'] in ['feet','hands'] else 1)
 if len(parts)==2:assert parts[0]['socket'].endswith('L') and parts[1]['socket'].endswith('R')
 for part in parts:assert part['order']==item['sortingOrder'] and (A/'Resources'/(part['sprite']+'.png')).exists()
# Contract regression from previous reward hotfix remains present.
s=(A/'Runtime/RewardStatusView.cs').read_text();body=re.search(r'class RewardResponse\s*\{([^}]+)',s).group(1)
assert 'recoveryAmount' in body and 'recovered' in body
# Delimiter check is supplemental, NOT a Unity compilation.
for p in [A/'Runtime'/n for n in ['HumanRig.cs','CharacterVisual.cs','FirstLaunchScreen.cs','CharacterCustomizationScreen.cs','AccessoryVisual.cs','CatalogLoader.cs','StudioPanel.cs']]:
 s=p.read_text();s=re.sub(r'"(?:\\.|[^"\\])*"','""',s);s=re.sub(r'//[^\n]*','',s);assert s.count('{')==s.count('}'),p
print('PASS: 31 IDs, five slots, 512px transparent assets, paired bindings, reward DTO and source delimiters. Unity play tests NOT RUN.')
