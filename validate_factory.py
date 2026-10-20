"""Source geometry + independent movement calculation; NOT C# execution or Unity physics."""
from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena'
f=json.loads((A/'Resources/Data/factory.json').read_text());m=json.loads((A/'Resources/Data/movement.json').read_text())
assert all(math.isfinite(x) for x in f.values())
assert f['collapseAt']==25 and f['collapseWarning']==5 and f['trapWarning']==2
assert f['eliminationY']<f['lowerY']<f['upperY']
assert f['halfGap']<f['trapCenter']-f['trapWidth']/2<f['trapCenter']+f['trapWidth']/2<f['outerEdge']
for dt in [1/30,1/60,1/120]:
 x=y=vx=0;vy=m['jumpSpeed'];first=True
 for i in range(1000):
  oldx,oldy=x,y
  rate=m['acceleration']*(1 if first else m['airControl'])
  vx=min(m['speed'],vx+rate*dt);vy=max(-m['maxFallSpeed'],vy-m['gravity']*dt)
  x+=vx*dt;y+=vy*dt;first=False
  if y<=0:
   distance=oldx+(x-oldx)*oldy/(oldy-y);break
 required=2*f['halfGap']+m['width']+2*m['skin']
 assert distance>required+.1,(dt,distance,required)
 assert distance>f['trapWidth']+m['width']+2*m['skin']+.1
 print(f'PASS: independent jump calculation dt={dt:.6f}: rest-start full-body range {distance:.3f}, center crossing {required:.3f}, margin {distance-required:.3f}; no collision simulation')
# Upper footprint is fully covered below before traps open. Spawn x is outside trap.
assert f['halfGap']+m['width']/2<6.5<f['outerEdge']-m['width']/2
assert abs(6.5-f['trapCenter'])>(f['trapWidth']+m['width'])/2
assert f['upperY']-.36-f['lowerY']>m['standingHeight']+m['jumpSpeed']**2/(2*m['gravity'])+.1
fall=math.sqrt(2*(f['upperY']-f['lowerY'])/m['gravity'])
assert fall<f['trapWarning']
print(f'PASS: all 4 spawn supports/clearance by geometry; upper/lower footprint coverage; ideal vertical fall {fall:.3f}s before earliest trap opens')
r=(A/'Runtime/FactoryArena.cs').read_text();core=(A/'Core/FactoryRules.cs').read_text()
for token in ['platform.enabled=false','traps[e.Side].enabled=false','SetRender(traps[e.Side],false)','traps[e.Side].enabled=true','SetRender(traps[e.Side],true)','match.ElapsedSeconds,match.CurrentTick','match.Suspended','MatchPhase.Active','body.Intersects(trapVolumes[side])']:assert token in r,token
assert 'Sequence,Tick' in core and 'AtSeconds' in core and 'tick<=lastTick' in core
assert 'surface.enabled' in (A/'Runtime/GripController.cs').read_text()
assert 'executionOrder: -150' in (A/'Runtime/FactoryArena.cs.meta').read_text()
assert 'FactoryChecks.RunAll()' in (R/'Tests/Program.cs').read_text()
print('PASS: warning/event/clock/collider/render/restore/grip gates structurally present')
print('NOT TESTED: C# compilation or execution; Unity collision, animation, timing, UI and Android device acceptance')
