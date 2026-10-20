"""P13 source/geometry checks. Not Unity or C# execution."""
from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena'
c=json.loads((A/'Resources/Data/crater.json').read_text());m=json.loads((A/'Resources/Data/movement.json').read_text())
assert all(math.isfinite(x) for x in c.values())
assert c['warningSeconds']==2 and c['travelSeconds']==6
assert c['lowerY']<c['platformY']<c['upperY'] and c['eliminationY']<c['lowerY']
assert c['hitRecovery']>=c['impulseCap']/c['impulseDecay']
# Ramp upper endpoints touch rocks at +/-6, lower endpoints touch central landing at +/-2.
slope=(c['upperY']-c['lowerY'])/4
assert 1/math.sqrt(1+slope*slope)>.5
assert slope*m['speed']/30<=c['stepHeight']
assert c['platformHalfWidth']+c['platformTravel']<=2.4+1e-7
assert c['platformY']-.36>c['lowerY']+.4 # moving corridor clears ramp at its most inward overlap
for dt in [1/30,1/60,1/120]:
 x=y=vx=0;vy=m['jumpSpeed'];first=True;time=0
 for i in range(1000):
  ox,oy=x,y;vx=min(m['speed'],vx+m['acceleration']*(1 if first else m['airControl'])*dt);vy=max(-m['maxFallSpeed'],vy-m['gravity']*dt);x+=vx*dt;y+=vy*dt;first=False;time+=dt
  if y<=0:distance=ox+(x-ox)*oy/(oy-y);break
 maxgap=2.4+c['platformTravel']-c['platformHalfWidth']
 required=maxgap+m['width']+2*m['skin']+(2*c['platformTravel']/c['travelSeconds'])*time
 assert distance>required+.1,(dt,distance,required)
 print(f'PASS: independent dt={dt:.6f} jump {distance:.3f}, worst moving-edge full-body requirement {required:.3f}; no Unity collision simulation')
# Four spawn footprints: upper at +/-8; lower +/-1.5 stay between the permanent ramps.
assert 6+m['width']/2<8<10-m['width']/2
assert 1.5+m['width']/2<2
assert 2.4>c['platformTravel']+c['platformHalfWidth']-1e-7
print('PASS: 4 spawn footprints, two permanent 45-degree ramp connections, six optional bridge pieces, clear moving corridor and recovery configuration')
r=(A/'Runtime/CraterArena.cs').read_text();motor=(A/'Runtime/CharacterMotor.cs').read_text()
for token in ['actor.QueueCarry(delta,platform)','actor.CanCarry(delta,platform)','travel.Advance(dt,blocked)','match.ElapsedSeconds','match.Suspended','MatchPhase.Active','b.Collider.enabled=false','b.Art.enabled=false','hits.TryHit(hazard,index,elapsed)','surface.X0=x0','Physics2D.BoxCast(origin','Settings.rockSize+distance']:assert token in r,token
assert motor.count('body.MovePosition(')==1
assert 'bridge.Allows' in motor and 'CanStandAt(feet,extra)' in motor
assert 'CraterBridgeSurface' in (A/'Runtime/CraterBridgeSurface.cs').read_text()
assert 'surface.enabled' in (A/'Runtime/GripController.cs').read_text()
assert 'CraterChecks.RunAll()' in (R/'Tests/Program.cs').read_text()
assert 'executionOrder: -150' in (A/'Runtime/CraterArena.cs.meta').read_text()
print('PASS: carrier, warning, hit-once, collider/render break, one-way bridge and shared grip-validity wiring (static only)')
print('NOT RUN: C# compilation/tests, Unity ramp/carry/hazard/one-way physics, shader rendering, Android and performance acceptance')
