from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Ellipse
R=Path(__file__).resolve().parents[1];c=json.loads((R/'UnityProject/Assets/ItmeArena/Resources/Data/crater.json').read_text());O=R/'Docs/P13_Visual';O.mkdir(exist_ok=True)
fig,ax=plt.subplots(figsize=(14,8),facecolor='#17101e');ax.set_facecolor('#29121f');ax.set_xlim(-11,11);ax.set_ylim(-6,6.1);ax.set_aspect('equal')
for sign in [-1,1]:
 lo=min(sign*6,sign*10);ax.add_patch(Rectangle((lo,-2.2),4,c['upperY']+2.2,facecolor='#50414f',edgecolor='#a694a6'))
 pts=[(sign*6,c['upperY']),(sign*2,c['lowerY']),(sign*2,c['lowerY']-.6),(sign*6,c['lowerY']-.6)]
 ax.add_patch(Polygon(pts,facecolor='#655064',edgecolor='#b29bb0'))
 for i in range(3):
  x0=sign*(6-i*1.2);x1=sign*(6-(i+1)*1.2);y0=c['upperY']+(c['platformY']-c['upperY'])*i/3;y1=c['upperY']+(c['platformY']-c['upperY'])*(i+1)/3
  ax.add_patch(Polygon([(x0,y0),(x1,y1),(x1,y1-.16),(x0,y0-.16)],facecolor='#ff9c42',edgecolor='#ffc080'))
 ax.text(sign*8,.3,'YAN KAYA',color='#ded0dd',ha='center',fontsize=11)
 ax.text(sign*4,-.8,'KALICI RAMPA',color='#e7d3e5',ha='center',fontsize=10,rotation=45*sign)
ax.add_patch(Rectangle((-5.5,c['lowerY']-.6),11,.6,facecolor='#655064',edgecolor='#b29bb0'))
ax.add_patch(Rectangle((-c['platformHalfWidth'],c['platformY']-.36),c['platformHalfWidth']*2,.36,facecolor='#948293',edgecolor='white'))
ax.annotate('',xy=(-1,1.45),xytext=(1,1.45),arrowprops={'arrowstyle':'<->','color':'#ffdf83','lw':2});ax.text(0,1.75,'Uçtan uca 6 sn',ha='center',color='#ffdf83',fontsize=11)
for i in range(4):
 x=(-8 if i==0 else 8) if i<2 else (-1.5 if i==2 else 1.5);y=c['upperY'] if i<2 else c['lowerY'];ax.add_patch(Rectangle((x-.4,y+.03),.8,1.6,facecolor='#ff9c42' if i%2==0 else '#4cd2b1',edgecolor='white'));ax.text(x,y+1.85,str(i+1),color='white',ha='center',weight='bold')
for x in [-.85,.85]:ax.add_patch(Ellipse((x,c['lowerY']+.035),c['lavaWidth'],.14,facecolor='none',edgecolor='#ffe15b',lw=2,linestyle='--'))
ax.annotate('2 sn uyarı → lav',xy=(.85,c['lowerY']),xytext=(3.6,-3.2),color='#ffe15b',ha='center',arrowprops={'arrowstyle':'->','color':'#ffe15b'})
ax.add_patch(Rectangle((-3-.275,2.8),.55,.55,facecolor='#bc9caa',edgecolor='white'));ax.annotate('Uyarılı kaya',xy=(-3,3.35),xytext=(-3,4.8),color='#dec8d5',ha='center',arrowprops={'arrowstyle':'->','color':'#dec8d5'})
ax.axhspan(-6,c['eliminationY'],color='#bc3813');ax.axhline(c['eliminationY'],color='#ffb94f');ax.text(0,-5.55,'LAV · DÜŞEN ELENİR',color='#ffdcab',ha='center',fontsize=15)
ax.set_title('İTME ARENASI · P13 / KIZIL KRATER',color='white',fontsize=23,pad=20,weight='bold');ax.tick_params(colors='#bba9ba');ax.spines[:].set_color('#72546c')
fig.text(.5,.075,'Turuncu köprüler kırılabilir; kalıcı rampalar ortak alt alana bağlanır. Köprüler alttan geçişe izin verir.',ha='center',color='#e5c4a4',fontsize=11)
fig.text(.5,.035,'Kaynak geometri şemasıdır; Unity ekran görüntüsü veya fizik testi değildir. 3/4 yalnız dört kişilik başlangıçtır.',ha='center',color='#bcaabc',fontsize=10)
fig.subplots_adjust(top=.89,bottom=.14,left=.05,right=.95)
fig.savefig(O/'Crater-layout.png',dpi=140,facecolor=fig.get_facecolor());fig.savefig(O/'Crater-layout.svg',facecolor=fig.get_facecolor())
