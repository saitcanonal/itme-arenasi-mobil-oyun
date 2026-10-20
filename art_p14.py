from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];O=R/'UnityProject/Assets/ItmeArena/Resources/MapPreviews';O.mkdir(parents=True,exist_ok=True)
S=R/'ArtSource/P14';S.mkdir(parents=True,exist_ok=True)
for key in ['merdiven_boslugu','kirik_fabrika','kizil_krater']:
 bg={'merdiven_boslugu':'#262937','kirik_fabrika':'#422b23','kizil_krater':'#321320'}[key]
 shapes=[]
 def rect(x,y,w,h,col):shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}"/>')
 def line(x1,y1,x2,y2,col,width=3):shapes.append(f'<path d="M{x1},{y1}L{x2},{y2}" fill="none" stroke="{col}" stroke-width="{width}"/>')
 def poly(points,col):shapes.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+'" fill="'+col+'"/>')
 rect(0,0,512,288,bg)
 if key=='merdiven_boslugu':
  for x in [28,478]:rect(x,12,5,246,'#626276')
  rect(225,22,62,100,'#a0b8c2');line(256,22,256,122,'#30384b')
  for side in [-1,1]:
   def X(x):return 256+side*x
   for inner,outer,y in [(170,228,62),(56,94,137),(170,228,212)]:rect(min(X(inner),X(outer)),y,outer-inner,7,'#9796a7')
   for i in range(20):
    rect(X(168-i*3.9)-2,65+i*3.6,5,3,'#ff9a43' if 7<=i<=11 else '#aaa7b6')
    rect(X(96+i*3.9)-2,140+i*3.6,5,3,'#ff9a43' if 7<=i<=11 else '#aaa7b6')
  for x in [244,268]:line(x,20,x,231,'#b9b4c3',1)
  rect(233,175,46,18,'#8f91b0');rect(10,257,492,31,'#11111e')
 elif key=='kirik_fabrika':
  for x in [68,206,405]:
   for i in range(3):line(x-28,40+i*10,x+28,40+i*10,'#262023',7)
  for side in [-1,1]:
   a,b=sorted([256+side*23,256+side*218]);rect(a,90,b-a,10,'#ba8a60');rect(a,188,b-a,10,'#ba8a60');tx=256+side*85;rect(tx-14,188,28,10,'#ff9a43')
   for x in range(int(a)+8,int(b),15):rect(x,94,3,3,'#523a32')
  line(179,16,435,16,'#8b6d59',4);line(340,16,340,62,'#a49bb3',2);rect(335,61,10,7,'#a49bb3');rect(10,257,492,31,'#120d0b')
 else:
  for sign in [-1,1]:
   poly([(256+sign*230,133),(256+sign*172,12),(256+sign*60,133)],'#190d19')
   a,b=sorted([256+sign*135,256+sign*225]);rect(a,88,b-a,125,'#665061')
   poly([(256+sign*135,88),(256+sign*45,198),(256+sign*45,213),(256+sign*135,213)],'#80657b')
   line(256+sign*135,88,256+sign*54,139,'#ff9b42',6)
  rect(132,198,248,15,'#80657b');rect(225,140,62,9,'#b59bad');line(238,127,274,127,'#ffdc63',3)
  rect(0,254,512,34,'#e74d16');line(0,254,512,254,'#ffbe57',4)
  for x in [237,275]:shapes.append(f'<ellipse cx="{x}" cy="197" rx="8" ry="3" fill="none" stroke="#ffe467" stroke-width="2"/>')
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="288" viewBox="0 0 512 288">'+''.join(shapes)+'</svg>'
 (S/(key+'.svg')).write_text(svg)
 import fitz
 doc=fitz.open(stream=svg.encode(),filetype='svg');pdf=fitz.open('pdf',doc.convert_to_pdf());pix=pdf[0].get_pixmap(alpha=False);pix.save(str(O/(key+'.png')))
