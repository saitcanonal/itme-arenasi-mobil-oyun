from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena'
c=json.loads((A/'Resources/Data/stairwell.json').read_text());m=json.loads((A/'Resources/Data/movement.json').read_text())
assert all(math.isfinite(v) for v in c.values())
assert (c['breakAfter'],c['restoreAfter'],c['liftTravelSeconds'])==(1.5,5,4)
assert .2<=c['stepHeight']<=.35 and c['eliminationY']<c['liftBottom']<c['liftTop']
# Check the authored repeated geometry, not a simulation of Unity physics.
s=(A/'Runtime/StairwellArena.cs').read_text()
for token in ['i<20','8.9f-i*.2f','4.8f-i*.2f','5.1f+i*.2f','.8f-i*.2f','i>=7&&i<=11','new Vector2(.205f,.18f)'] :assert token in s,token
assert math.isclose(4.8-19*.2,1) and math.isclose(.8-19*.2,-3)
assert .205+4*.2>m['width']
assert 'sweep.Intersects(body)' in s and 'CanCarry(delta,lift)' in s
assert 'match.Suspended' in s and 'MatchPhase.Active' in s
motor=(A/'Runtime/CharacterMotor.cs').read_text();assert motor.count('body.MovePosition(')==1
assert 'StepHeight<=0' in motor and 'carry=Vector2.zero;carrier=null' in motor
assert 'executionOrder: -150' in (A/'Runtime/StairwellArena.cs.meta').read_text()
assert 'StairwellChecks.RunAll()' in (R/'Tests/Program.cs').read_text()
print('PASS: P11 settings, 80 authored treads, four five-tread gaps wider than body, landing heights, single motor move and safety wiring (structural only).')
print('NOT TESTED: C# execution, collision, carry, stair traversal, timing in Unity, rendering and device input.')
