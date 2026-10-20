from pathlib import Path
import json,uuid,fitz
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena';D=A/'Resources/Accessories';D.mkdir(exist_ok=True);S=R/'ArtSource/P10';S.mkdir(parents=True,exist_ok=True)
def path(d,c,stroke='',w=4):return f'<path d="{d}" fill="{c}"'+(f' stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '')+'/>'
def ellipse(x,y,rx,ry,c,stroke='',w=4):return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"'+(f' stroke="{stroke}" stroke-width="{w}"' if stroke else '')+'/>'
def existing(name,stage):return (R/f'ArtSource/P{stage:02}/{name}.svg').read_text().split('>',1)[1].rsplit('</svg>',1)[0]
glasses=ellipse(25,50,21,31,'none','#29273d',7)+ellipse(75,50,21,31,'none','#29273d',7)+path('M46 48 H54 M0 40 L5 44 M95 44 L100 40','none','#29273d',5)
art={
'pofuk_baret':existing('helmet',8),
'pofuk_kaynak_gozlugu':ellipse(27,50,24,40,'#46dcc3','#263d43',5)+ellipse(78,50,18,29,'#46dcc3','#263d43',5)+path('M49 47 H60','none','#263d43',5),
'pofuk_kirmizi_pelerin':path('M30 5 L70 5 L95 95 Q70 78 53 96 Q23 78 5 95 Z','#d62c4c')+path('M32 10 L50 30 L68 10','none','#ff5874',6),
'pofuk_boks_eldiveni':existing('pofuk_hand',8),
'pofuk_yayli_pabuc':path('M20 6 H80 L20 18 L80 29 L20 40 L80 51','none','#c7c9dc',5)+ellipse(50,76,46,20,'#9c9bb9')+path('M5 87 Q50 99 95 87','none','white',6),
'pofuk_kocaman_biyik':path('M50 45 C25 3 18 69 3 26 C-10 79 34 96 50 67 C67 95 110 79 97 26 C84 69 75 3 50 45','#52301e'),
'cengel_kafa_bandi':existing('headband',8),
'cengel_yuvarlak_gozluk':glasses.replace('#29273d','#efbd24'),
'kivilcim_kulaklik':path('M10 68 V44 C10 -2 90 -2 90 44 V68','none','#29273d',10)+'<rect x="0" y="48" width="22" height="42" rx="9" fill="#e73550"/><rect x="78" y="48" width="22" height="42" rx="9" fill="#e73550"/>',
'kivilcim_buyuk_fiyonk':existing('bow',9),
'kivilcim_kaynak_gozlugu':glasses.replace('none','#ffcd29').replace('#29273d','#705124'),
'kivilcim_cizgili_atki':path('M3 4 Q50 21 97 4 L97 30 L84 30 L98 96 L76 99 L60 31 Q25 39 3 29 Z','#ff8b32')+path('M19 10 L19 29 M40 14 L40 31 M63 12 L63 30 M73 48 L88 44 M77 66 L93 62 M81 83 L96 80','none','#fff4d0',4),
'kivilcim_is_eldiveni':existing('cengel_hand',8).replace('#ff9f8e','#dfad0c'),
'kivilcim_paten':path('M16 4 H62 L66 40 Q98 40 96 69 H6 V39 L16 39 Z','#c3c5d9')+ellipse(20,84,12,12,'#4d4c62')+ellipse(76,84,12,12,'#4d4c62'),
'firtina_yuvarlak_gozluk':glasses,
'firtina_simsek_tokasi':existing('lightning',9),
'firtina_halka_kupe':ellipse(50,54,27,39,'none','#ffcf3b',8),
'firtina_bileklik':'<rect x="3" y="34" width="94" height="31" rx="9" fill="#e63551"/>'+path('M17 38 V61','none','#ff8e9a',7),
'firtina_sirt_cantasi':'<rect x="9" y="3" width="82" height="94" rx="18" fill="#f6ce37"/><rect x="22" y="46" width="56" height="38" rx="8" fill="#e8a914"/>'+path('M24 8 V91 M77 8 V91','none','#5d4934',6),
'firtina_cizgili_corap':'<rect x="20" y="1" width="60" height="95" rx="6" fill="white"/>'+path('M20 25 H80 M20 54 H80 M20 82 H80','none','#e53951',10),
'koli_kenan_boks_eldiveni':existing('pofuk_hand',8).replace('#e53250','#f2c52c').replace('#f0657e','#ffe77a'),
'koli_kenan_kirilir_etiketi':existing('fragile',9),
'koli_kenan_koli_bandi':path('M0 7 L12 0 L100 85 L88 100 Z M88 0 L100 12 L13 100 L0 87 Z','#ecd297'),
'koli_kenan_baret':existing('helmet',8),
'koli_kenan_piksel_gozluk':path('M2 20 H44 V28 H56 V20 H98 V66 H88 V78 H64 V66 H56 V40 H44 V66 H36 V78 H12 V66 H2 Z','#121219')+path('M11 29 H20 M25 29 H34 M66 29 H75 M80 29 H89','none','white',6),
'koli_kenan_anten_toplari':ellipse(50,50,43,43,'#e53250','#29273d',6)
}
catalog=json.loads((A/'Resources/Data/catalog.json').read_text());bindings=[]
for a in catalog['accessories']:
 id=a['id'];svg='<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 100 100">'+art[id]+'</svg>';(S/(id+'.svg')).write_text(svg)
 doc=fitz.open(stream=svg.encode(),filetype='svg');pdf=fitz.open(stream=doc.convert_to_pdf(),filetype='pdf');png=D/(id+'.png');pdf[0].get_pixmap(matrix=fitz.Matrix(256/pdf[0].rect.width,256/pdf[0].rect.height),alpha=True).save(str(png))
 g=uuid.uuid5(uuid.NAMESPACE_URL,'itme-v1/'+str(png.relative_to(R/'UnityProject/Assets'))).hex
 template=(A/'Resources/Characters/pofuk_body.png.meta').read_text();import re
 template=re.sub(r'guid: [a-f0-9]{32}','guid: '+g,template);template=re.sub(r'spriteID: [a-f0-9]{32}','spriteID: '+g,template).replace('21300000: pofuk_body','21300000: '+id);Path(str(png)+'.meta').write_text(template)
 slot=a['slot'];parts=[]
 def add(socket,sx,sy,x=0,y=0,order=9,hide=''):
  parts.append(dict(sprite='Accessories/'+id,socket=socket,x=x,y=y,sx=sx,sy=sy,order=order,hideBase=hide))
 if slot=='head':
  if 'baret' in id:add('SocketHead',1.12 if a['characterId']=='pofuk' else .96,.51,y=.02)
  elif 'kafa_bandi' in id:add('SocketHead',.73,.18,y=-.15)
  elif 'kulaklik' in id:add('SocketHead',1.08,.92,y=-.35)
  elif 'fiyonk' in id:add('SocketHead',.48,.27,y=.02)
  else:add('SocketHead',.23,.37,x=.34,y=-.04)
 elif slot=='face':
  if 'biyik' in id:add('SocketFace',1,.55,y=-.37)
  else:add('SocketFace',1.1,.88,y=.05)
 elif slot=='hands':
  for side in ['L','R']:add('SocketWrist'+side,.25 if 'bileklik' in id else .43,.12 if 'bileklik' in id else .44,y=.02,hide='' if 'bileklik' in id else 'HandArt'+side)
 elif slot=='feet':
  for side in ['L','R']:add('SocketFoot'+side,1.2,2.0 if 'yayli' in id else 1.4,y=.3,hide='Foot'+side)
 elif slot=='back':add('SocketBack',1.4 if a['characterId']=='pofuk' else .82,.95 if a['characterId']=='pofuk' else .8,x=-.28,y=-.22 if a['characterId']=='pofuk' else -.1,order=1)
 elif slot=='neck':add('SocketNeck',.92,.56,y=-.23)
 elif slot=='ears':
  for side in ['L','R']:add('SocketEar'+side,.15,.22,y=-.12)
 elif slot=='legs':
  for side in ['L','R']:add('SocketLeg'+side,.21,.26)
 elif slot=='body':add('SocketBody',.29 if 'etiketi' in id else .65,.23 if 'etiketi' in id else .62,x=-.12 if 'etiketi' in id else 0,y=-.15 if 'etiketi' in id else 0)
 elif slot=='antenna':
  for side in ['L','R']:add('SocketAntenna'+side,.21,.30)
 bindings.append(dict(id=id,characterId=a['characterId'],slot=slot,parts=parts));a['artStatus']='accessory-v1-runtime-unverified';a['assetKey']='Accessories/'+id
(A/'Resources/Data/accessories.json').write_text(json.dumps(dict(items=bindings),ensure_ascii=False,indent=2)+'\n');(A/'Resources/Data/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
(S/'README.md').write_text('26 editable SVG accessory redraws from S02–S06. Rendering source only; no prices, purchases or ownership are granted by these assets. Bindings in Resources/Data/accessories.json use character sockets, one item per catalog slot.\n')
print('26 accessories and attachment bindings authored')
