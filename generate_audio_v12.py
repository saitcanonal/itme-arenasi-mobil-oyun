"""Original 144 BPM, 16-bar instrumental loop. No samples or third-party composition."""
from pathlib import Path
import numpy as np,wave
rate=22050;beat=60/144;duration=64*beat
out=np.zeros((round(duration*rate),2));rng=np.random.default_rng(1202)
def add(at,seconds,signal,pan=0):
 n=round(seconds*rate);t=np.arange(n)/rate;v=signal(t);start=round(at*rate);ix=(np.arange(n)+start)%len(out);out[ix,0]+=v*(.75-pan*.25);out[ix,1]+=v*(.75+pan*.25)
roots=[45,45,41,43]*4
for step in range(128):
 b=step*.5;root=roots[int(b//4)];note=root+[12,19,24,19,15,19,22,19][step%8];freq=440*2**((note-69)/12)
 add(b*beat,.38,lambda t,f=freq:.12*(np.sin(2*np.pi*f*t)+.25*np.sin(4*np.pi*f*t))*np.exp(-t*10)*np.minimum(1,t/.008),(-1 if step%2 else 1)*.6)
for b in range(64):
 f=440*2**((roots[b//4]-69)/12)
 add(b*beat,beat*.8,lambda t,f=f:.18*np.sin(2*np.pi*f*t)*np.minimum(1,t/.01)*np.exp(-t*5))
 add(b*beat,.22,lambda t:.4*np.sin(2*np.pi*(48*t+1.6*(1-np.exp(-t*35))))*np.exp(-t*22))
 if b%2:add(b*beat,.15,lambda t:.13*rng.normal(0,1,len(t))*np.exp(-t*24))
 for k in range(2):add((b+k*.5)*beat,.07,lambda t:.035*rng.normal(0,1,len(t))*np.exp(-t*55),.7)
out=np.tanh(out);out*=.83/max(abs(out).max(),.83)
p=Path(__file__).resolve().parents[1]/'UnityProject/Assets/ItmeArena/Resources/Audio/music.wav'
with wave.open(str(p),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes((out*32767).astype('<i2').tobytes())
print('Original loop',round(duration,2),'seconds; peak',round(float(abs(out).max()),3))
