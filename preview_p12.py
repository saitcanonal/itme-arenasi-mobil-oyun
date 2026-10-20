from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
R=Path(__file__).resolve().parents[1];f=json.loads((R/'UnityProject/Assets/ItmeArena/Resources/Data/factory.json').read_text())
O=R/'Docs/P12_Visual';O.mkdir(exist_ok=True)
fig,axes=plt.subplots(1,2,figsize=(15,7),facecolor='#171320')
for ax,after in zip(axes,[False,True]):
 ax.set_facecolor('#37271f');ax.set_xlim(-9.7,9.7);ax.set_ylim(-6.4,5.8);ax.set_aspect('equal');ax.tick_params(colors='#b8afa9');ax.spines[:].set_color('#645049')
 ax.set_title('BAŞLANGIÇ • 0–35 saniye' if not after else 'ÇÖKÜŞ SONRASI • örnek 43. saniye',color='white',fontsize=13,pad=15)
 for side in [-1,1]:
  lo,hi=sorted([side*f['halfGap'],side*f['outerEdge']]);width=hi-lo
  ax.add_patch(Rectangle((lo,f['upperY']-.36),width,.36,facecolor='#a47b5a' if not after else 'none',edgecolor='#d8ae7e',linestyle='--' if after else '-',alpha=.4 if after else 1))
  spans=[(f['halfGap'],f['trapCenter']-f['trapWidth']/2),(f['trapCenter']+f['trapWidth']/2,f['outerEdge'])]
  for a,b in spans:
   left,right=sorted([side*a,side*b]);ax.add_patch(Rectangle((left,f['lowerY']-.36),right-left,.36,facecolor='#a47b5a',edgecolor='#d8ae7e'))
  tx=side*f['trapCenter']-f['trapWidth']/2
  opened=after and side==-1
  ax.add_patch(Rectangle((tx,f['lowerY']-.36),f['trapWidth'],.36,facecolor='none' if opened else '#ed9d48',edgecolor='#ffc973',linestyle='--' if opened else '-'))
  ax.text(side*f['trapCenter'],f['lowerY']-.85,'AÇIK ↓' if opened else 'KAPAK',color='#ffce80',ha='center',fontsize=10)
  if after:
   ax.annotate('',xy=(side*6.5,f['lowerY']+.25),xytext=(side*6.5,f['upperY']-.6),arrowprops={'arrowstyle':'->','color':'#ffc973','lw':2})
 for i in range(4):
  x=-6.5 if i%2==0 else 6.5;y=(f['upperY'] if i<2 and not after else f['lowerY'])
  if after and i>=2:continue
  ax.add_patch(Rectangle((x-.4,y+.03),.8,1.6,facecolor='#ff963f' if i%2==0 else '#54d4b4',edgecolor='white',alpha=.9))
  ax.text(x,y+1.9,str(i+1),ha='center',color='white',weight='bold')
 ax.axhspan(-6.4,f['eliminationY'],color='#100e0e');ax.axhline(f['eliminationY'],color='#f6bc33',linestyle='--');ax.text(0,-6.2,'ELENME ÇUKURU',color='#f6bc33',ha='center',fontsize=11)
 ax.annotate('',xy=(-f['halfGap'],.7),xytext=(f['halfGap'],.7),arrowprops={'arrowstyle':'<->','color':'#eeeeee'})
 ax.text(0,1.02,'2 birim',color='white',ha='center',fontsize=10)
 ax.set_xlabel('Unity birimi',color='#b8afa9')
fig.suptitle('İTME ARENASI · P12 / KIRIK FABRİKA',color='white',fontsize=22,y=.98,weight='bold')
fig.text(.5,.07,'35 sn: çöküş uyarısı  →  40 sn: üst kat çöker  →  42 sn: ilk kapak açılır',color='#ffcc88',ha='center',fontsize=13)
fig.text(.5,.025,'Kaynak geometri şemasıdır; Unity ekran görüntüsü veya fizik testi değildir. 3/4 başlangıçları yalnız dört kişilik düzende kullanılır.',color='#bab1b9',ha='center',fontsize=10)
fig.subplots_adjust(top=.88,bottom=.18,wspace=.12)
fig.savefig(O/'Factory-layout.png',dpi=140,facecolor=fig.get_facecolor());fig.savefig(O/'Factory-layout.svg',facecolor=fig.get_facecolor())
