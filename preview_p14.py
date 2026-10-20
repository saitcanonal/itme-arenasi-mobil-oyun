from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import textwrap
R=Path(__file__).resolve().parents[1];O=R/'Docs/P14_Visual';O.mkdir(exist_ok=True)
im=Image.new('RGB',(1280,760),'#1f132e');d=ImageDraw.Draw(im)
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def text(x,y,value,size=17,color='white'):d.text((x,y),value,font=ImageFont.truetype(fontpath,size),fill=color)
def box(x,y,w,h,color):d.rectangle((x,y,x+w,y+h),fill=color)
def button(x,y,w,h,value):
 box(x,y,w,h,'#664587');f=ImageFont.truetype(fontpath,17);b=d.textbbox((0,0),value,font=f);text(x+(w-b[2])/2,y+(h-20)/2,value)
text(40,20,'HARİTA VE TAKIM SEÇ',30);button(1080,22,160,52,'Geri');text(40,68,'4 kişilik yerel test · botlar henüz eklenmedi',17,'#b3e6d9')
for i,(key,name) in enumerate([('merdiven_boslugu','Merdiven Boşluğu'),('kirik_fabrika','Kırık Fabrika'),('kizil_krater','Kızıl Krater')]):
 x=40+i*408;box(x,108,384,202,'#59efc7' if i==0 else '#59406e');box(x+5,113,374,192,'#38294a');img=Image.open(R/('UnityProject/Assets/ItmeArena/Resources/MapPreviews/'+key+'.png')).convert('RGB');img.thumbnail((366,145));im.paste(img,(int(x+9+(366-img.width)/2),117));text(x+17,263,name,22);text(x+323,262,'✓' if i==0 else '',23,'#59efc7')
box(40,330,760,304,'#332147');text(56,340,'TAKIM 1',22,'#ff9e4d');text(436,340,'TAKIM 2',22,'#5ce6c7')
for team,seats in enumerate([['Sato_1 (Sen)','Test katılımcısı 3'],['Test katılımcısı 2','Test katılımcısı 4']]):
 for row,name in enumerate(seats):
  x=48+team*380;y=380+row*80;box(x,y,364,74,'#4a335e');text(x+8,y+3,name);button(x+298,y+4,58,30,'↔');text(x+8,y+36,'Yerel oyuncu' if 'Sen' in name else 'Sabit test katılımcısı',14,'#bfb3d1')
box(824,330,416,366,'#422b57');text(844,346,'Harita: Merdiven Boşluğu',20);text(844,373,"Oyuncular: 4 / 4 · 2'ye 2",20);text(844,400,'Mod: yerel test',20)
msg='Yalnız sen kontrol edersin. Diğer katılımcılar sabit test gövdeleridir; bot/çevrim içi oyuncu değildir.'
for i,line in enumerate(textwrap.wrap(msg,40)):text(844,442+i*23,line,17,'#ffcc80')
button(844,616,376,60,'Başla');button(40,648,270,48,'Takımları değiştir');text(326,662,'Oyuncunun yanındaki ↔ ile takımını değiştir.',16,'#ccc0db')
text(40,727,'Kaynak UI yerleşim şeması · Unity ekran görüntüsü değildir.',16,'#b9a9c9');im.save(O/'Selection-layout.png')
