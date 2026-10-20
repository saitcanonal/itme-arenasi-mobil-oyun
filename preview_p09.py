from pathlib import Path
import json,math,fitz,re
R=Path(__file__).resolve().parents[1];S=R/'ArtSource/P09';out=R/'Docs/P09_Visual';out.mkdir(exist_ok=True)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1225" viewBox="0 0 1440 1225">','<rect width="1440" height="1225" fill="#171827"/>','<text x="34" y="44" font-family="sans-serif" font-size="28" fill="#fff">KIVILCIM / FIRTINA / KOLI KENAN — P09</text>','<text x="34" y="73" font-family="sans-serif" font-size="15" fill="#acacc3">Editable part artwork • six pose previews • not a Unity runtime capture</text>']
for row,kind in enumerate(['kivilcim','firtina','koli_kenan']):
 for col,state in enumerate(['Idle','Walk','Jump','Push','Grip','Fall']):
  nodes=json.loads((S/(kind+'.rig.json')).read_text());lookup={n['name']:n for n in nodes};p=kind=='pofuk';phase=.9
  lookup['Body']['sy']=1.13 if state=='Jump' and p else 1.08 if state=='Fall' and p else .89 if state=='Push' and p else 1
  lookup['Body']['sx']=1/lookup['Body']['sy']
  for i,side in enumerate(['L','R']):
   sign=-1 if i==0 else 1;shoulder=(lookup['Shoulder'+side]['x']*lookup['Body']['sx'],.9+lookup['Shoulder'+side]['y']*lookup['Body']['sy'])
   end=[sign*(.50),.44];rot=0
   if state=='Walk':end[0]+=math.sin(phase+i*math.pi)*.1;end[1]+=abs(math.sin(phase+i*math.pi))*.07;lookup['Leg'+side]['rot']=math.sin(phase+i*math.pi)*24
   if state in ['Jump','Fall']:end[1]=1.03 if p else 1.3;end[0]*=1.1;rot=-sign*25;lookup['Leg'+side]['rot']=sign*(20 if state=='Jump' else 12)
   if state=='Push':end=[.97,.88+i*.14];rot=-90
   if state=='Grip':end=[.59+i*.08,1.55+(-.03 if i==0 else .09)]
   arm=lookup['Arm'+side];dx=end[0]-shoulder[0];dy=end[1]-shoulder[1];arm.update(x=(end[0]+shoulder[0])/2,y=(end[1]+shoulder[1])/2,sx=math.hypot(dx,dy),sy=.13 if kind=='koli_kenan' else .18,rot=math.degrees(math.atan2(dy,dx)))
   lookup['Hand'+side].update(x=end[0],y=end[1],rot=rot)
   for f in range(3):lookup['Finger'+side+str(f)]['active']=False
  x=24+col*236;y=106+row*365
  svg.append(f'<rect x="{x}" y="{y}" width="222" height="345" rx="18" fill="#24253b"/>')
  svg.append(f'<text x="{x+17}" y="{y+30}" font-family="sans-serif" font-size="18" fill="#50dfc0">{kind.upper()} / {state.upper()}</text>')
  svg.append(f'<g transform="translate({x+106},{y+274}) scale(98,-98)">')
  if state=='Grip':svg.append('<rect x=".52" y="1.61" width=".7" height=".08" rx=".03" fill="#686880"/>')
  for n in sorted(nodes,key=lambda n:n['layer']):
   if not n['sprite'] or not n['active']:continue
   chain=[];v=n
   while v:
    chain.append(v);v=lookup.get(v['parent'])
   transform=' '.join(f'translate({v["x"]} {v["y"]}) rotate({v.get("rot",0)}) scale({v["sx"]} {v["sy"]})' for v in reversed(chain))
   source=S/(n['sprite']+'.svg');source=source if source.exists() else R/'ArtSource/P08'/(n['sprite']+'.svg');art=source.read_text();body=re.sub(r'^.*?<svg[^>]*>','',art).replace('</svg>','')
   svg.append(f'<g transform="{transform}"><g transform="translate(-.5 .5) scale(.01 -.01)">{body}</g></g>')
  svg.append('</g>')
  svg.append(f'<text x="{x+17}" y="{y+321}" font-family="sans-serif" font-size="13" fill="#b1b0c6">Same movement / push / grip stats</text>')
svg.append('</svg>');s=''.join(svg);(out/'P09-pose-board.svg').write_text(s)
d=fitz.open(stream=s.encode(),filetype='svg');pdf=fitz.open(stream=d.convert_to_pdf(),filetype='pdf');pdf[0].get_pixmap(matrix=fitz.Matrix(1.333333,1.333333)).save(str(out/'P09-pose-board.png'))
