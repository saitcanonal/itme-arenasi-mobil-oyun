from pathlib import Path
import json,re
r=Path(__file__).resolve().parents[1];u=r/'UnityProject/Assets/ItmeArena';j=r/'Server/src/main/java/com/itmearena/application'
rows=[('pofuk','Yaylı Sıçrayış','İnişte yakındaki rakipleri savur.'),('pofuk','Pofuduk Kalkan','2 saniye darbelere karşı korun.'),('pofuk','Dev Boks Eldiveni','Önündeki rakibe ağır yumruk at.'),('cengel','Kanca Çekişi','Uzun kolunla rakibini kendine çek.'),('cengel','Kol Çarkı','Dönen kollarınla çevreni süpür.'),('cengel','Boynuz Hücumu','İleri atıl, yolundaki rakibi sürükle.'),('kivilcim','Elektrik Çarpması','Yakındaki rakibi 3 saniye bayılt.'),('kivilcim','Kıvılcım Yağmuru','Önüne üç ayrı kıvılcım gönder.'),('kivilcim','Kaynak Işını','1 saniye boyunca ışınla geri it.'),('firtina','Şimşek','Görüşündeki en yakın rakibe şimşek indir.'),('firtina','Rüzgâr Dalgası','Geniş bir alandaki rakipleri geri it.'),('firtina','Fırtına Bulutu','Rakibin üzerine yavaşlatan bulut bırak.'),('koli_kenan','Kutu Fırlatma','Fırlayan kutu rakibe çarpınca bayıltır.'),('koli_kenan','Kırılgan Mod','2 saniye içinde ilk darbeyi yansıt.'),('koli_kenan','TV Parazit','Rakibin yönlerini 0,8 saniye ters çevir.')]
(u/'Resources/Data/powers.json').write_text(json.dumps([dict(index=i,id='power_'+str(i),character=c,name=n,description=d) for i,(c,n,d) in enumerate(rows)],ensure_ascii=False,indent=2))
cs='''using System;
namespace ItmeArena.Core {
// Pure deterministic rules. Actor ids are stable seats 0..7. No Unity dependencies.
public sealed class ArenaPowers {
 public sealed class Actor {public int Id,Team,Facing=1,Power;public double X,Y;public bool Alive,Grounded,CanCast,Request,Disabled;}
 public sealed class Effect {public int Kind,Source,Target,Power;public double X,Y,Force,Stun;}
 public sealed class Shot {public bool Live;public int Source,Power,Direction;public double X,Y,End;}
 public delegate bool Wall(double x,double y,double tx,double ty);
 public readonly Effect[] Effects=new Effect[256];public int Count;
 public readonly Shot[] Shots=new Shot[32];
 public readonly double[] Shield=new double[8],Reflect=new double[8],Slow=new double[8],Jam=new double[8],Immune=new double[8];
 private readonly int[] active=new int[8],direction=new int[8];private readonly double[] until=new double[8],next=new double[8],began=new double[8];
 private readonly bool[] airborne=new bool[8];private readonly bool[,] struck=new bool[8,8];
 private double time;private Actor[] actors;private Wall wall;
 public ArenaPowers(){for(int i=0;i<8;i++)active[i]=-1;for(int i=0;i<32;i++)Shots[i]=new Shot();}
 private void Emit(int kind,int source,int target,int power,double x,double y,double force,double stun){if(Count>=256)return;var e=new Effect();e.Kind=kind;e.Source=source;e.Target=target;e.Power=power;e.X=x;e.Y=y;e.Force=force;e.Stun=stun;Effects[Count++]=e;}
 private Actor Find(int id){foreach(var a in actors)if(a.Id==id)return a;return null;}
 private bool Enemy(Actor a,Actor b){return b.Alive&&a.Id!=b.Id&&a.Team!=b.Team;}
 private double Dist(Actor a,Actor b){return Math.Sqrt((a.X-b.X)*(a.X-b.X)+(a.Y-b.Y)*(a.Y-b.Y));}
 private Actor Nearest(Actor a,double range,bool front){Actor best=null;foreach(var b in actors){double d=Dist(a,b);if(Enemy(a,b)&&d<=range&&(!front||(b.X-a.X)*a.Facing>=0)&&!wall(a.X,a.Y,b.X,b.Y)){if(best==null||d<Dist(a,best)||d==Dist(a,best)&&b.Id<best.Id)best=b;}}return best;}
 private void Hit(Actor a,Actor b,int power,double force,double stun){if(Shield[b.Id]>time)return;if(Reflect[b.Id]>time){Reflect[b.Id]=0;var swap=a;a=b;b=swap;force=-force;if(Shield[b.Id]>time)return;}
  if(Immune[b.Id]>time)stun=0;if(stun>0)Immune[b.Id]=time+stun+3;
  Emit(1,a.Id,b.Id,power,b.X,b.Y,force,stun);
 }
 private void Area(Actor a,int power,double range,double force,bool front,bool once){foreach(var b in actors)if(Enemy(a,b)&&Dist(a,b)<=range&&(!front||(b.X-a.X)*direction[a.Id]>=0)&&!wall(a.X,a.Y,b.X,b.Y)&&(!once||!struck[a.Id,b.Id])){struck[a.Id,b.Id]=true;Hit(a,b,power,(b.X>=a.X?1:-1)*force,0);}}
 private void Fire(Actor a,int power,double y){foreach(var s in Shots)if(!s.Live){s.Live=true;s.Source=a.Id;s.Power=power;s.Direction=a.Facing;s.X=a.X+a.Facing*.6;s.Y=a.Y+y;s.End=time+1.2;return;}}
 public void Step(double now,double dt,Actor[] snapshot,Wall blocked){if(now<time||dt<=0||dt>.1)throw new ArgumentException("Invalid power clock");time=now;actors=snapshot;wall=blocked;Count=0;
  foreach(var a in actors){if(!a.Alive||a.Disabled){active[a.Id]=-1;continue;}if(!a.Request||!a.CanCast||a.Power<0||a.Power>=15)continue;
   int p=a.Power,id=a.Id;var target=Nearest(a,p==3?5:p==9?7:p==11?6:p==14?4:2.8,p==2||p==3);
   if((p==2||p==3||p==6||p==9||p==11||p==14)&&target==null)continue;
   Emit(0,id,id,p,a.X,a.Y,0,0);direction[id]=a.Facing;began[id]=time;for(int k=0;k<8;k++)struck[id,k]=false;
   switch(p){
    case 0:active[id]=p;until[id]=time+2;airborne[id]=false;Emit(2,id,id,p,a.X,a.Y,0,0);break;
    case 1:Shield[id]=time+2;break;
    case 2:Hit(a,target,p,a.Facing*18,0);break;
    case 3:Hit(a,target,p,(a.X>=target.X?1:-1)*11,0);break;
    case 4:active[id]=p;until[id]=time+.8;next[id]=time;break;
    case 5:active[id]=p;until[id]=time+.55;next[id]=time;Emit(2,id,id,p,a.X,a.Y,a.Facing*12,0);break;
    case 6:Hit(a,target,p,a.Facing*3,3);break;
    case 7:Fire(a,p,-.5);Fire(a,p,0);Fire(a,p,.5);break;
    case 8:active[id]=p;until[id]=time+1;next[id]=time;break;
    case 9:Hit(a,target,p,(target.X>=a.X?1:-1)*7,1);break;
    case 10:Area(a,p,5,12,false,true);break;
    case 11:if(Shield[target.Id]<=time){Slow[target.Id]=time+2;Emit(3,id,target.Id,p,target.X,target.Y,0,0);}break;
    case 12:Fire(a,p,0);break;
    case 13:Reflect[id]=time+2;break;
    case 14:if(Shield[target.Id]<=time&&Immune[target.Id]<=time){Jam[target.Id]=time+.8;Immune[target.Id]=time+3.8;Emit(3,id,target.Id,p,target.X,target.Y,0,0);}break;
   }
  }
  foreach(var a in actors){int id=a.Id,p=active[id];if(!a.Alive||a.Disabled||p<0)continue;if(time>=until[id]){active[id]=-1;continue;}
   if(p==0){if(!a.Grounded)airborne[id]=true;if(airborne[id]&&a.Grounded&&time>began[id]+.08){Area(a,p,3.5,13,false,true);Emit(3,id,id,p,a.X,a.Y,0,0);active[id]=-1;}}
   else if(time>=next[id]){next[id]=time+.2;if(p==4)Area(a,p,3,9,false,true);if(p==5)Area(a,p,1.7,6,true,false);if(p==8)Area(a,p,5,3,true,false);}
  }
  foreach(var s in Shots){if(!s.Live)continue;var a=Find(s.Source);double nx=s.X+s.Direction*8*dt;if(a==null||!a.Alive||time>=s.End||wall(s.X,s.Y,nx,s.Y)){s.Live=false;continue;}
   Actor chosen=null;double best=100;foreach(var b in actors)if(Enemy(a,b)&&Math.Abs(b.Y-s.Y)<.8){double cx=Math.Max(Math.Min(s.X,nx),Math.Min(Math.Max(s.X,nx),b.X));double d=Math.Abs(b.X-cx);if(d<.55&&Math.Abs(b.X-s.X)<best){best=Math.Abs(b.X-s.X);chosen=b;}}
   s.X=nx;if(chosen!=null){Hit(a,chosen,s.Power,s.Direction*6,s.Power==12?3:0);s.Live=false;}
  }
 }
}
}
'''
(u/'Core/ArenaPowers.cs').write_text(cs)
# One rule source, mechanical Java port: no separately maintained gameplay constants.
java=cs.replace('using System;\nnamespace ItmeArena.Core {','package com.itmearena.application;\n').rsplit('\n}',1)[0]
java=java.replace('public sealed class ArenaPowers','public final class ArenaPowers').replace('public sealed class ','public static final class ').replace('public readonly ','public final ').replace('private readonly ','private final ').replace('public delegate bool Wall(double x,double y,double tx,double ty);','public interface Wall {boolean test(double x,double y,double tx,double ty);}')
java=java.replace('bool','boolean').replace('booleanean','boolean').replace('new boolean[8,8]','new boolean[8][8]').replace('boolean[,]','boolean[][]')
java=re.sub(r'struck\[([^,\]]+),([^\]]+)\]',r'struck[\1][\2]',java)
java=re.sub(r'foreach\(var (\w+) in ([^)]+)\)',r'for(var \1 : \2)',java)
java=java.replace('wall(','wall.test(').replace('ArgumentException','IllegalArgumentException')
for a,b in [('Math.Sqrt','Math.sqrt'),('Math.Abs','Math.abs'),('Math.Max','Math.max'),('Math.Min','Math.min')]:java=java.replace(a,b)
(j/'ArenaPowers.java').write_text(java)
# Catalog bindings generated together.
entries=',\n'.join(' new PowerDefinition(%d,"power_%d","%s","%s","%s")'%(i,i,c,n,d) for i,(c,n,d) in enumerate(rows))
(u/'Core/PowerCatalog.cs').write_text('''using System;
namespace ItmeArena.Core {
 public sealed class PowerDefinition {public readonly int Index;public readonly string Id,Character,Name,Description;public PowerDefinition(int i,string id,string c,string n,string d){Index=i;Id=id;Character=c;Name=n;Description=d;}}
 public static class PowerCatalog {
 public static readonly PowerDefinition[] All={'''+entries+'''};
 public static PowerDefinition Get(string character,string id){foreach(var p in All)if(p.Character==character&&p.Id==id)return p;foreach(var p in All)if(p.Character==character)return p;return All[0];}
 }
}''')
(j/'PowerCatalog.java').write_text('''package com.itmearena.application;
public final class PowerCatalog {
 public static final String[] Characters={'''+','.join('"'+c+'"' for c,n,d in rows)+'''};
 public static int index(String character,String id){for(int i=0;i<15;i++)if(Characters[i].equals(character)&&("power_"+i).equals(id))return i;for(int i=0;i<15;i++)if(Characters[i].equals(character))return i;return 0;}
 public static boolean valid(String character,String id){return id!=null&&("power_"+index(character,id)).equals(id);}
}''')
