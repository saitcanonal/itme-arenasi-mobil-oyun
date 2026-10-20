from pathlib import Path
import wave,struct,math
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena'
for name,duration in [('push',.18),('fall',.38),('click',.08),('music',64*60/144)]:
 p=A/('Resources/Audio/'+name+'.wav')
 with wave.open(str(p)) as w:
  assert w.getnchannels()==(2 if name=="music" else 1) and w.getsampwidth()==2 and w.getframerate()==22050
  values=struct.unpack('<'+'h'*(w.getnframes()*w.getnchannels()),w.readframes(w.getnframes()));assert abs(len(values)/w.getnchannels()/22050-duration)<.001
  peak=max(abs(v) for v in values);assert 0<peak<32767 and (name=="music" or abs(values[0])<100 and abs(values[-1])<100)
  rms=math.sqrt(sum(v*v for v in values)/len(values));assert rms>50
 assert 'AudioImporter:' in Path(str(p)+'.meta').read_text()
 print('PASS PCM',name,'duration',duration,'peak',peak,'rms',round(rms,1))
def s(p):return (A/p).read_text()
f=s('Runtime/ArenaFeedback.cs');audio=s('Runtime/ArenaAudio.cs');at=s('Runtime/ArenaAtmosphere.cs');menu=s('Runtime/MainMenuScreen.cs')
for token in ['new Dot[48]','cursor++%MobileQuality.ImpactBudget','combat.HitConfirmed-=Hit','shakeLeft=.12f','scale=.06f','Play("fall")','match.Suspended']:assert token in f,token
assert 'new AudioSource[4]' in audio and 'source.Stop()' in audio and 'OnApplicationFocus' in audio and 'gameplayPaused' in audio
assert 'new SpriteRenderer[32]' in at and 'sr.sortingOrder=-15' in at and 'Collider' not in at
for key in ['itme.sound.v1','itme.music.v1','itme.shake.v1']:assert key in audio and key in menu
assert 'labCamera.transform.localPosition=new Vector3(0,0,-10)' in s('Runtime/MovementLab.cs')
print('PASS fixed 48 impact / 32 atmosphere / 4 SFX capacities, collider-free backgrounds, toggles, pause and camera reset source gates')
print('NOT RUN Unity import/audio listening/rendering, Android sound/shake/FPS/10 match leak acceptance')
