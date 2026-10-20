from pathlib import Path
import json,uuid,subprocess,fitz
R=Path(__file__).resolve().parents[1]
A=R/'UnityProject/Assets/ItmeArena';S=R/'ArtSource/P08';S.mkdir(parents=True,exist_ok=True)
D=A/'Resources/Characters';D.mkdir(parents=True,exist_ok=True)
def guid(p):return uuid.uuid5(uuid.NAMESPACE_URL,'itme-v1/'+str(p.relative_to(R/'UnityProject/Assets'))).hex
def ellipse(cx,cy,rx,ry,c):return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}"/>'
def path(d,c,stroke='',width=4):return f'<path d="{d}" fill="{c}"'+(f' stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '')+'/>'
assets={
'pofuk_body':ellipse(50,51,46,47,'#ff8b35')+ellipse(72,57,21,39,'#e77b30')+ellipse(46,70,28,24,'#ffac68')+ellipse(19,57,5,5,'#ff866a'),
'cengel_body':'<rect x="19" y="2" width="62" height="96" rx="31" fill="#b28afa"/>'+ellipse(69,57,12,37,'#a47ae3')+ellipse(50,72,22,22,'#c39efa'),
'pofuk_face':ellipse(29,43,24,30,'#29273d')+ellipse(29,43,20,26,'#fff')+ellipse(36,48,10,12,'#201d31')+ellipse(39,43,3.5,4,'#fff')+ellipse(79,38,17,23,'#29273d')+ellipse(79,38,13,19,'#fff')+ellipse(76,42,7,9,'#201d31')+ellipse(78,39,2.5,3,'#fff')+path('M8 9 Q28 -3 47 10 M66 9 Q79 5 95 15','none','#29273d',4)+path('M19 78 Q52 82 89 70 Q56 111 19 78','#602538','#39212d',4)+'<rect x="55" y="78" width="10" height="12" rx="2" fill="white"/>'+ellipse(76,93,9,6,'#ff698e'),
'cengel_face':ellipse(27,36,22,29,'#29273d')+ellipse(27,36,18,25,'white')+ellipse(73,36,22,29,'#29273d')+ellipse(73,36,18,25,'white')+ellipse(32,27,9,12,'#201d31')+ellipse(78,27,9,12,'#201d31')+path('M3 2 L44 12 M58 12 L96 1','none','#29273d',5)+ellipse(7,72,7,8,'#d678ca')+ellipse(94,72,7,8,'#d678ca')+path('M14 87 L25 98 L36 86 L47 98 L58 86 L69 98 L80 86 L93 96','none','#493021',5),
'pofuk_hand':ellipse(50,56,45,41,'#e53250')+ellipse(20,65,17,22,'#e53250')+'<rect x="19" y="4" width="63" height="18" rx="7" fill="#f5f4fa"/>'+ellipse(29,46,9,16,'#f0657e'),
'cengel_hand':ellipse(50,59,38,34,'#ff9f8e')+path('M19 63 Q2 49 11 39 Q21 33 30 45 M25 34 L25 15 Q28 2 38 15 L39 36 M44 33 L46 9 Q52 0 58 12 L59 36 M65 39 L68 16 Q77 7 80 23 L80 47','#ff9f8e','#ff9f8e',9),
'pofuk_arm':'<rect x="2" y="26" width="96" height="48" rx="24" fill="#ff8b35"/>',
'cengel_arm':'<rect x="2" y="27" width="96" height="46" rx="23" fill="#b28afa"/>',
'pofuk_leg':'<rect x="16" y="0" width="68" height="100" rx="18" fill="#ff8b35"/>',
'cengel_leg':'<rect x="22" y="0" width="56" height="100" rx="26" fill="#b28afa"/>',
'foot':ellipse(50,58,47,29,'#f4f4fb')+ellipse(50,47,47,29,'#292b40'),
'horn':path('M20 94 Q-2 21 51 4 L82 94 Z','#ffda45'),
'curl':path('M8 90 L8 38 Q8 3 42 10 Q69 12 68 40 L68 54','none','#ff9f8e',19),
'helmet':path('M5 89 Q4 26 50 22 Q94 26 95 89 Z','#ffc416')+'<rect x="0" y="87" width="100" height="9" rx="4" fill="#e7a800"/><rect x="45" y="15" width="10" height="76" rx="4" fill="#ffdc60"/>'+ellipse(50,55,4,5,'#e53250'),
'headband':path('M0 35 Q50 62 100 34 L100 65 Q50 90 0 65 Z','#e53250'),
'socket_marker':path('M50 4 L96 50 L50 96 L4 50 Z','#48dec0')}
for name,body in assets.items():
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 100 100">'+body+'</svg>'
 (S/(name+'.svg')).write_text(svg)
 png=D/(name+'.png');doc=fitz.open(stream=svg.encode(),filetype='svg');pdf=fitz.open(stream=doc.convert_to_pdf(),filetype='pdf');pdf[0].get_pixmap(matrix=fitz.Matrix(256/pdf[0].rect.width,256/pdf[0].rect.height),alpha=True).save(str(png))
 (Path(str(png)+'.meta')).write_text(f'''fileFormatVersion: 2
guid: {guid(png)}
TextureImporter:
  serializedVersion: 13
  mipmaps:
    enableMipMap: 0
  isReadable: 0
  textureType: 8
  textureShape: 1
  spriteMode: 1
  spritePixelsToUnits: 256
  spriteMeshType: 1
  alphaIsTransparency: 1
  textureSettings:
    serializedVersion: 2
    filterMode: 1
    aniso: 1
    wrapU: 1
    wrapV: 1
    wrapW: 1
  spritePivot: {{x: 0.5, y: 0.5}}
  spriteBorder: {{x: 0, y: 0, z: 0, w: 0}}
  maxTextureSize: 256
  textureCompression: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
    bones: []
    spriteID: {guid(png)}
    internalID: 0
    vertices: []
    indices:
    edges: []
    weights: []
    secondaryTextures: []
  fileIDToRecycleName:
    21300000: {name}
  externalObjects: {{}}
  userData:
  assetBundleName:
  assetBundleVariant:
''')

def rig(kind):
 p=kind=='pofuk';nodes=[]
 def n(name,parent='VisualRoot',pos=(0,0),scale=(1,1),sprite=None,layer=3,active=True):
  nodes.append(dict(name=name,parent=parent if nodes else None,x=pos[0],y=pos[1],sx=scale[0],sy=scale[1],sprite=sprite,layer=layer,active=active))
 n('VisualRoot');n('Body',pos=(0,.9),scale=(1,1))
 n('BodyArt','Body',scale=(1.27,1.27) if p else (1.05,1.26),sprite=kind+'_body')
 n('Face','Body',pos=(.035,.16),scale=(.76,.55) if p else (.57,.49),sprite=kind+'_face',layer=4)
 for side,x in [('L',-.27),('R',.27)]:
  if not p:n('Horn'+side,'Body',pos=(x, .69),scale=(.16,.3),sprite='horn',layer=2)
  n('Shoulder'+side,'Body',pos=(x*(1.85 if p else 1),.02))
  n('Arm'+side,pos=(x*1.8,.68 if p else .48),scale=(.36,.25) if p else (.78,.19),sprite=kind+'_arm',layer=2 if side=='L' else 5)
  n('Hand'+side,pos=(x*(2.7 if p else 2.05),.47 if p else .19))
  n('HandArt'+side,'Hand'+side,scale=(.43,.43) if p else (.38,.4),sprite=kind+'_hand',layer=6)
  for i in range(3):n('Finger'+side+str(i),'Hand'+side,pos=(-.10+i*.09,.14),scale=(.105,.20),sprite='curl',layer=7,active=False)
  n('SocketWrist'+side,'Hand'+side)
  n('Leg'+side,pos=(x*.67,.3))
  n('LegArt'+side,'Leg'+side,pos=(0,-.08),scale=(.22,.28) if p else (.19,.34),sprite=kind+'_leg',layer=2)
  n('Foot'+side,'Leg'+side,pos=(0,-.22),scale=(.36,.22) if p else (.27,.16),sprite='foot',layer=3)
  n('SocketFoot'+side,'Foot'+side)
 n('SocketHead','Body',pos=(0,.61));n('SocketFace','Face');n('SocketBack','Body',pos=(0,-.05));n('SocketWaist','Body',pos=(0,-.34))
 n('DemoAccessory','SocketHead',pos=(0,.06 if p else -.14),scale=(1.16,.53) if p else (.72,.18),sprite='helmet' if p else 'headband',layer=5,active=False)
 n('DemoWrist','SocketWristR',scale=(.12,.12),sprite='socket_marker',layer=8,active=False)
 return nodes
for kind in ['pofuk','cengel']:
 nodes=rig(kind);(S/(kind+'.rig.json')).write_text(json.dumps(nodes,indent=2)+'\n')
 ids={n['name']:1000+i*10 for i,n in enumerate(nodes)}
 yaml='%YAML 1.1\n%TAG !u! tag:unity3d.com,2011:\n'
 for n in nodes:
  b=ids[n['name']];sprite=n['sprite'];parent=ids[n['parent']]+1 if n['parent'] else 0
  yaml+=f'''--- !u!1 &{b}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {b+1}}}
'''
  if sprite:yaml+=f'  - component: {{fileID: {b+2}}}\n'
  yaml+=f'''  m_Layer: 0
  m_Name: {n['name']}
  m_TagString: Untagged
  m_IsActive: {int(n['active'])}
--- !u!4 &{b+1}
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {b}}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: {n['x']}, y: {n['y']}, z: 0}}
  m_LocalScale: {{x: {n['sx']}, y: {n['sy']}, z: 1}}
  m_ConstrainProportionsScale: 0
'''
  children=[ids[c['name']]+1 for c in nodes if c['parent']==n['name']]
  yaml+='  m_Children:'+ ('\n'+''.join(f'  - {{fileID: {c}}}\n' for c in children) if children else ' []\n')+f'  m_Father: {{fileID: {parent}}}\n'
  if sprite:
   yaml+=f'''--- !u!212 &{b+2}
SpriteRenderer:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: {b}}}
  m_Enabled: 1
  m_CastShadows: 0
  m_ReceiveShadows: 0
  m_Materials:
  - {{fileID: 10754, guid: 0000000000000000f000000000000000, type: 0}}
  m_SortingLayerID: 0
  m_SortingOrder: {n['layer']}
  m_Sprite: {{fileID: 21300000, guid: {guid(D/(sprite+'.png'))}, type: 3}}
  m_Color: {{r: 1, g: 1, b: 1, a: 1}}
  m_FlipX: 0
  m_FlipY: 0
  m_DrawMode: 0
  m_Size: {{x: 1, y: 1}}
  m_MaskInteraction: 0
  m_SpriteSortPoint: 0
'''
 prefab=D/(kind+'.prefab');prefab.write_text(yaml)
 Path(str(prefab)+'.meta').write_text(f'fileFormatVersion: 2\nguid: {guid(prefab)}\nPrefabImporter:\n  externalObjects: {{}}\n  userData:\n  assetBundleName:\n  assetBundleVariant:\n')
# Reproducible source artwork, not flattened PDF pages.
(S/'README.md').write_text('P08 editable vector sources. SVG files are original part-by-part redraws of S02/S03. PNG exports use PyMuPDF SVG-to-PDF raster rendering with alpha. 256 px/sprite unit. Rig JSON records prefab bind transforms, parent, sorting layer and visibility. Prefabs are editable directly in Unity. No colliders, gameplay scripts or stats in visual prefabs. Demo accessories disabled by default; not inventory ownership.\n')
print('Art parts and editable prefabs created')
