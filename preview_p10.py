from pathlib import Path
import json,re,fitz,math
R=Path(__file__).resolve().parents[1];O=R/'Docs/P10_Visual';O.mkdir(exist_ok=True)
config=json.loads((R/'UnityProject/Assets/ItmeArena/Resources/Data/accessories.json').read_text());bindings={x['id']:x for x in config['items']}
chosen=[['pofuk_baret','pofuk_boks_eldiveni','pofuk_yayli_pabuc','pofuk_kocaman_biyik','pofuk_kirmizi_pelerin'],['cengel_kafa_bandi','cengel_yuvarlak_gozluk'],['kivilcim_buyuk_fiyonk','kivilcim_cizgili_atki','kivilcim_is_eldiveni','kivilcim_paten'],['firtina_yuvarlak_gozluk','firtina_simsek_tokasi','firtina_halka_kupe','firtina_bileklik','firtina_sirt_cantasi','firtina_cizgili_corap'],['koli_kenan_boks_eldiveni','koli_kenan_kirilir_etiketi','koli_kenan_baret','koli_kenan_piksel_gozluk','koli_kenan_anten_toplari']]
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="680" viewBox="0 0 1500 680"><rect width="1500" height="680" fill="#181827"/>','<text x="30" y="46" fill="white" font-family="sans-serif" font-size="29">P10 / ACCESSORY FIT CHECK</text><text x="30" y="76" fill="#b8b5ca" font-family="sans-serif" font-size="16">Source artwork preview. Not a Unity runtime capture. No purchases or gameplay bonuses.</text>']
for i,kind in enumerate(['pofuk','cengel','kivilcim','firtina','koli_kenan']):
 stage=8 if i<2 else 9;nodes=json.loads((R/f'ArtSource/P{stage:02}/{kind}.rig.json').read_text());lookup={n['name']:n for n in nodes}
 def n(name,parent,x,y):
  d=dict(name=name,parent=parent,x=x,y=y,sx=1,sy=1,sprite=None,layer=3,active=True);nodes.append(d);lookup[name]=d
 n('SocketBody','Body',0,0 if i<2 else -.26);n('SocketNeck','Body',0,0)
 for side,x in [('L',-.42),('R',.42)]:
  n('SocketEar'+side,'Head' if i>1 else 'Body',x,0);n('SocketLeg'+side,'Leg'+side,0,-.1)
 if i==4:
  n('SocketAntennaL','Antenna',-.45,.4);n('SocketAntennaR','Antenna',.45,.4)
 for side in ['L','R']:
  shoulder=(lookup['Shoulder'+side]['x'],.9+lookup['Shoulder'+side]['y']);end=(lookup['Hand'+side]['x'],lookup['Hand'+side]['y']);dx=end[0]-shoulder[0];dy=end[1]-shoulder[1]
  lookup['Arm'+side].update(x=(end[0]+shoulder[0])/2,y=(end[1]+shoulder[1])/2,sx=math.hypot(dx,dy),rot=math.degrees(math.atan2(dy,dx)))
 for id in chosen[i]:
  for j,p in enumerate(bindings[id]['parts']):
   if p['hideBase']:lookup[p['hideBase']]['hiddenSprite']=True
   d=dict(name=id+str(j),parent=p['socket'],x=p['x'],y=p['y'],sx=p['sx'],sy=p['sy'],sprite=id,layer=p['order'],active=True,accessory=True);nodes.append(d);lookup[d['name']]=d
 x=15+i*298;svg.append(f'<rect x="{x}" y="108" width="282" height="548" rx="18" fill="#2d2943"/><text x="{x+18}" y="144" fill="#5cdfc3" font-size="20" font-family="sans-serif">{kind.upper()}</text><g transform="translate({x+140},520) scale(145,-145)">')
 for d in sorted(nodes,key=lambda x:x['layer']):
  if not d['sprite'] or not d['active'] or d.get('hiddenSprite'):continue
  chain=[];v=d
  while v:chain.append(v);v=lookup.get(v['parent'])
  tr=' '.join(f'translate({v["x"]} {v["y"]}) rotate({v.get("rot",0)}) scale({v["sx"]} {v["sy"]})' for v in reversed(chain))
  f=R/'ArtSource'/('P10' if d.get('accessory') else f'P{stage:02}')/(d['sprite']+'.svg')
  if not f.exists():f=R/'ArtSource/P08'/(d['sprite']+'.svg')
  body=re.sub(r'^.*?<svg[^>]*>','',f.read_text()).replace('</svg>','')
  svg.append(f'<g transform="{tr}"><g transform="translate(-.5 .5) scale(.01 -.01)">{body}</g></g>')
 svg.append('</g>')
 svg.append(f'<text x="{x+18}" y="610" fill="#b8b5ca" font-size="15" font-family="sans-serif">{len(chosen[i])} compatible slots / editable parts</text>')
svg.append('</svg>');s=''.join(svg);(O/'P10-outfits.svg').write_text(s);doc=fitz.open(stream=s.encode(),filetype='svg');pdf=fitz.open(stream=doc.convert_to_pdf(),filetype='pdf');pdf[0].get_pixmap(matrix=fitz.Matrix(1.333,1.333)).save(str(O/'P10-outfits.png'))
# Exact catalog contact sheet of all 26 parts.
from PIL import Image,ImageDraw,ImageFont
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15);sheet=Image.new('RGB',(1200,7*180),(27,25,43));draw=ImageDraw.Draw(sheet)
for i,a in enumerate(config['items']):
 x=(i%4)*300;y=(i//4)*180;im=Image.open(R/('UnityProject/Assets/ItmeArena/Resources/Accessories/'+a['id']+'.png')).convert('RGBA');im.thumbnail((120,120));sheet.paste(im,(x+90,y+5),im);name=a['id'].replace('_',' ');draw.text((x+8,y+132),name[:32],font=font,fill='white');draw.text((x+8,y+152),a['slot'],font=font,fill='#61e1c3')
sheet.save(O/'P10-all-accessories.png')
