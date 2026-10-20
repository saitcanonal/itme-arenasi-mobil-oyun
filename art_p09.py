from pathlib import Path
import json,uuid,subprocess,fitz
R=Path(__file__).resolve().parents[1]
A=R/'UnityProject/Assets/ItmeArena';S=R/'ArtSource/P09';S.mkdir(parents=True,exist_ok=True)
D=A/'Resources/Characters';D.mkdir(parents=True,exist_ok=True)
def guid(p):return uuid.uuid5(uuid.NAMESPACE_URL,'itme-v1/'+str(p.relative_to(R/'UnityProject/Assets'))).hex
def ellipse(cx,cy,rx,ry,c):return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}"/>'
def path(d,c,stroke='',width=4):return f'<path d="{d}" fill="{c}"'+(f' stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '')+'/>'
assets={
'kivilcim_body':'<rect x="13" y="2" width="74" height="95" rx="29" fill="#ffe286"/>'+path('M10 35 L22 35 L22 4 L31 4 L31 37 L69 37 L69 4 L78 4 L78 35 L90 35 L88 76 Q83 98 50 98 Q17 98 12 76 Z','#2eaaa2')+'<rect x="36" y="55" width="28" height="24" rx="6" fill="#2eaaa2" stroke="#208981" stroke-width="3"/>'+ellipse(26,37,3,4,'#ffdb43')+ellipse(74,37,3,4,'#ffdb43'),
'kivilcim_head':ellipse(50,52,47,47,'#ce377c')+ellipse(50,55,40,39,'#efb28d')+path('M8 38 Q10 0 50 4 Q90 0 92 39 L50 22 Z','#ce377c')+ellipse(11,64,6,23,'#ce377c')+ellipse(89,64,6,23,'#ce377c'),
'kivilcim_hair':ellipse(22,34,19,22,'#ce377c')+ellipse(78,34,19,22,'#ce377c'),
'kivilcim_face':ellipse(26,37,19,24,'#29273d')+ellipse(26,37,16,20,'white')+ellipse(31,39,8,11,'#201d31')+ellipse(34,34,2,3,'white')+path('M62 37 Q80 20 95 35 M7 8 Q26 -1 44 6 M62 5 Q81 -4 97 7','none','#29273d',4)+path('M23 72 L89 72 Q57 111 23 72','#652c2c','#39212d',3)+path('M28 75 L84 75 L80 82 L32 82 Z','white')+ellipse(64,88,13,6,'#ff648d')+ellipse(5,65,7,8,'#ef8a8a')+ellipse(96,65,7,8,'#ef8a8a'),
'firtina_body':path('M20 5 L33 0 L67 0 L80 5 L97 94 Q50 110 3 94 Z','#f16b48')+path('M22 74 Q50 87 78 74 L82 97 L18 97 Z','#c75b40')+path('M40 4 L38 39 M61 4 L63 39','none','#fff7e8',3)+ellipse(38,40,3,4,'#fff7e8')+ellipse(63,40,3,4,'#fff7e8'),
'firtina_head':ellipse(50,53,43,44,'#ca9064'),
'firtina_hair':ellipse(22,54,20,23,'#433047')+ellipse(78,54,20,23,'#433047')+ellipse(24,28,21,22,'#433047')+ellipse(76,28,21,22,'#433047')+ellipse(38,19,23,20,'#433047')+ellipse(62,20,23,20,'#433047')+ellipse(50,37,27,21,'#433047'),
'firtina_face':ellipse(29,39,19,24,'#29273d')+ellipse(29,39,16,21,'white')+ellipse(72,39,19,24,'#29273d')+ellipse(72,39,16,21,'white')+ellipse(33,41,8,12,'#444052')+ellipse(76,41,8,12,'#444052')+ellipse(35,37,3,4,'white')+ellipse(78,37,3,4,'white')+path('M11 12 Q27 2 44 10 M58 2 Q78 -8 92 6','none','#29273d',5)+path('M31 80 Q58 103 88 72','none','#432719',4)+ellipse(9,68,8,9,'#df7b7a')+ellipse(92,68,8,9,'#df7b7a'),
'koli_kenan_body':'<rect x="9" y="2" width="82" height="96" rx="5" fill="#c58e52" stroke="#55371f" stroke-width="4"/><rect x="44" y="2" width="12" height="44" fill="#ecd29a"/>'+ellipse(24,48,6,7,'none')+'<rect x="62" y="67" width="19" height="23" rx="2" fill="white"/>'+path('M71 85 L71 71 M65 77 L71 71 L77 77','none','#29273d',2),
'koli_kenan_head':'<rect x="2" y="8" width="96" height="86" rx="14" fill="#5e819e" stroke="#2e4457" stroke-width="4"/><rect x="11" y="18" width="78" height="62" rx="10" fill="#aacfc4" stroke="#293447" stroke-width="3"/>'+path('M18 25 H82 M18 68 H82','none','#8aafa6',2)+ellipse(82,86,2,2,'#2e4457')+ellipse(90,86,2,2,'#2e4457'),
'koli_kenan_face':'<rect x="6" y="35" width="38" height="30" rx="4" fill="white" stroke="#29273d" stroke-width="4"/><rect x="56" y="35" width="38" height="30" rx="4" fill="white" stroke="#29273d" stroke-width="4"/>'+ellipse(27,49,8,11,'#201d31')+ellipse(76,49,8,11,'#201d31')+path('M3 17 L46 31 M54 31 L97 17 M32 81 H70','none','#29273d',6),
'antenna':path('M25 95 L5 10 M75 95 L95 10','none','#282538',6)+ellipse(5,10,5,7,'#e53250')+ellipse(95,10,5,7,'#e53250'),
'bow':path('M5 4 L49 39 L95 4 L95 96 L49 62 L5 96 Z','#ff5192')+ellipse(50,50,12,17,'#df357c'),
'lightning':path('M51 3 L82 3 L59 39 L89 39 L18 99 L40 54 L11 54 Z','#ffdb43','#e5a800',3),
'fragile':'<rect x="0" y="0" width="100" height="100" rx="8" fill="#d83c37"/>'+path('M25 17 H75 L56 45 V72 H72 V81 H28 V72 H44 V45 Z','white'),
}
for k,color in [('kivilcim','#efb28d'),('firtina','#f16b48'),('koli_kenan','#29273d')]:
 assets[k+'_arm']='<rect x="0" y="30" width="100" height="40" rx="20" fill="'+color+'"/>'
 assets[k+'_leg']='<rect x="25" y="0" width="50" height="100" rx="16" fill="'+color+'"/>'
 assets[k+'_hand']=ellipse(50,50,42,44,('#ca9064' if k=='firtina' else color) if k!='koli_kenan' else '#f6c72e')
 assets[k+'_foot']=ellipse(50,61,48,27,'#fff7f5')+ellipse(50,48,48,27,{'kivilcim':'#e53250','firtina':'#6265ff','koli_kenan':'#29273d'}[k])
assets['koli_kenan_arm']=assets['koli_kenan_arm'].replace('fill="#29273d"','fill="#474459"')
assets['koli_kenan_leg']=assets['koli_kenan_leg'].replace('fill="#29273d"','fill="#474459"')
assets['antenna']=assets['antenna'].replace('#282538','#595368')
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
 nodes=[]
 def n(name,parent='VisualRoot',pos=(0,0),scale=(1,1),sprite=None,layer=3,active=True):
  nodes.append(dict(name=name,parent=parent if nodes else None,x=pos[0],y=pos[1],sx=scale[0],sy=scale[1],sprite=sprite,layer=layer,active=active))
 k=kind=='kivilcim';f=kind=='firtina';tv=kind=='koli_kenan'
 n('VisualRoot');n('Body',pos=(0,.9))
 n('BodyArt','Body',pos=(0,-.26),scale=(.67,.55) if k else (.84,.60) if f else (.68,.68),sprite=kind+'_body')
 n('Head','Body',pos=(0,.33))
 n('HeadArt','Head',scale=(.96,.90) if k else (.91,.85) if f else (.94,.65),sprite=kind+'_head',layer=4)
 n('Face','Head',pos=(0,-.04),scale=(.66,.48) if not tv else (.65,.36),sprite=kind+'_face',layer=6)
 if k:n('Hair','Head',pos=(0,.37),scale=(1.13,.90),sprite=kind+'_hair',layer=3)
 if f:n('Hair','Head',pos=(0,.37),scale=(1.23,.91),sprite=kind+'_hair',layer=5)
 if tv:n('Antenna','Head',pos=(0,.44),scale=(.59,.37),sprite='antenna',layer=3)
 for side,x in [('L',-.27),('R',.27)]:
  n('Shoulder'+side,'Body',pos=(x,-.14))
  n('Arm'+side,pos=(x*1.5,.62),scale=(.44,.18) if not tv else (.5,.08),sprite=kind+'_arm',layer=2 if side=='L' else 5)
  n('Hand'+side,pos=(x*1.85,.44))
  n('HandArt'+side,'Hand'+side,scale=(.22,.24) if not tv else (.34,.37),sprite=kind+'_hand',layer=6)
  for i in range(3):n('Finger'+side+str(i),'Hand'+side,pos=(-.1+i*.09,.14),scale=(.105,.2),sprite='curl',layer=7,active=False)
  n('SocketWrist'+side,'Hand'+side)
  n('Leg'+side,pos=(x*.6,.3))
  n('LegArt'+side,'Leg'+side,pos=(0,-.08),scale=(.23,.32) if k else (.18,.25) if f else (.14,.47),sprite=kind+'_leg',layer=2)
  n('Foot'+side,'Leg'+side,pos=(0,-.22),scale=(.32,.18),sprite=kind+'_foot');n('SocketFoot'+side,'Foot'+side)
 n('SocketHead','Head',pos=(0,.46));n('SocketFace','Face');n('SocketBack','Body',pos=(0,-.2));n('SocketWaist','Body',pos=(0,-.48))
 n('DemoAccessory','SocketHead',pos=(0,0) if k else (.35,-.04) if f else (0,.04),scale=(.47,.25) if k else (.23,.37) if f else (.8,.4),sprite='bow' if k else 'lightning' if f else 'helmet',layer=8,active=False)
 n('DemoWrist','SocketWristR',scale=(.12,.12),sprite='socket_marker',layer=8,active=False)
 return nodes
for kind in ['kivilcim','firtina','koli_kenan']:
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
(S/'README.md').write_text('P09 editable vector sources. SVG files are original part-by-part redraws of S04/S05/S06. PNG exports use PyMuPDF SVG-to-PDF raster rendering with alpha. 256 px/sprite unit. Rig JSON records prefab bind transforms, parent, sorting layer and visibility. Prefabs are editable directly in Unity. No colliders, gameplay scripts or stats in visual prefabs. Demo accessories disabled by default; not inventory ownership.\n')
print('Art parts and editable prefabs created')
