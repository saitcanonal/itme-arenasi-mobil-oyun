from pathlib import Path
import wave,math,random,struct,uuid
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena/Resources/Audio';A.mkdir(exist_ok=True)
Path(str(A)+'.meta').write_text('fileFormatVersion: 2\nguid: '+uuid.uuid5(uuid.NAMESPACE_URL,'itme-v1/ItmeArena/Resources/Audio').hex+'\nfolderAsset: yes\nDefaultImporter:\n  externalObjects: {}\n  userData: \n  assetBundleName: \n  assetBundleVariant: \n')
rate=22050
for name,duration in [('push',.18),('fall',.38),('click',.08),('music',8)]:
 rng=random.Random(1801);data=[]
 for i in range(int(duration*rate)):
  t=i/rate;fade=min(1,t/.006)*min(1,(duration-t)/.012)
  if name=='push':v=(.55*math.sin(2*math.pi*(100*t-120*t*t))+.16*rng.uniform(-1,1))*math.exp(-t*22)
  elif name=='fall':v=.32*math.sin(2*math.pi*(650*t-650*t*t))*math.exp(-t*7)
  elif name=='click':v=.24*math.sin(2*math.pi*880*t)*math.exp(-t*50)
  else:
   notes=[220,261.6256,329.6276,261.6256,196,246.9417,293.6648,246.9417];n=notes[int(t*2)%8];local=t%.5
   env=math.sin(math.pi*local/.5)**2
   v=.16*env*(math.sin(2*math.pi*n*local)+.25*math.sin(2*math.pi*n*2*local))
  data.append(int(max(-.95,min(.95,v*fade))*32767))
 p=A/(name+'.wav')
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(struct.pack('<'+'h'*len(data),*data))
 Path(str(p)+'.meta').write_text('fileFormatVersion: 2\nguid: '+uuid.uuid5(uuid.NAMESPACE_URL,'itme-v1/ItmeArena/Resources/Audio/'+p.name).hex+'\nAudioImporter:\n  externalObjects: {}\n  serializedVersion: 7\n  defaultSettings:\n    serializedVersion: 2\n    loadType: 0\n    sampleRateSetting: 0\n    sampleRateOverride: 22050\n    compressionFormat: 1\n    quality: 0.7\n    conversionMode: 0\n  platformSettingOverrides: {}\n  forceToMono: 1\n  normalize: 0\n  preloadAudioData: 1\n  loadInBackground: 0\n  ambisonic: 0\n  3D: 0\n  userData: \n  assetBundleName: \n  assetBundleVariant: \n')
