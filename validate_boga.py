from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
import json
r=Path(__file__).resolve().parents[1];a=r/'UnityProject/Assets/ItmeArena';im=Image.open(a/'Resources/Boga/atlas.png');assert im.mode=='RGBA' and im.size==(1536,1024)
rects={'head':(74,24,429,537),'body':(610,26,360,517),'arm':(1204,25,199,519),'glove':(111,647,322,323),'leg':(675,571,185,434),'shoe':(1071,680,415,256)}
for name,(x,y,w,h) in rects.items():
 assert x>=0 and y>=0 and x+w<=im.width and y+h<=im.height
 alpha=im.getchannel('A').crop((x,y,x+w,y+h));bounds=alpha.point(lambda n:255 if n>80 else 0).getbbox()
 assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<w and bounds[3]<h,(name,bounds)
for point in [(0,0),(512,512),(550,700),(1000,500)]:assert im.getpixel(point)[3]==0
c=json.loads((a/'Resources/Data/catalog.json').read_text());assert next(v for v in c['characters'] if v['id']=='human_male')['displayName']=='Boğa'
assert len(c['accessories'])==31
print('PASS: six independent atlas parts, transparent margins, no clipping, canonical Boga identity, 31 retained products. Not a Unity/device test.')
