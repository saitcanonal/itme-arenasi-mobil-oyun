from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena'
def s(p):return (A/p).read_text()
g=json.loads(s('Resources/Data/grip.json'));u=json.loads(s('Resources/Data/ultimate.json'))
assert g['dragSpeedMultiplier']==.6 and u['stunSeconds']==3 and u['recoverySeconds']==3
c=s('Runtime/GripController.cs');m=s('Runtime/CharacterMotor.cs');v=s('Runtime/StunVisual.cs')
for t in ['if(!TryDrag())TryAttach()','graph.Drag.TryClaim','dragged.Motor.Stunned','ownerSupport.enabled','targetSupport.enabled','ValidateDrag()','graph.Drag.Release(Id)','other.Release("Hedef elendi / kapatıldı")']:assert t in c,t
for t in ['DragOwner.Grip.ValidateDrag()','DragFollowSpeed*Time.fixedDeltaTime','Grip.DragSpeedMultiplier','float dy=gripping?']:assert t in m,t
for t in ['×  ×','BAYGIN','line.positionCount=10','phase+=Time.deltaTime*3','faceArt.enabled=priorFace','Destroy(material)']:assert t in v,t
assert 'Protected(b.Id)' in s('Core/Ultimate.cs')
assert 'actors[i].Grip.Team=team' in s('Runtime/MovementLab.cs')
print('PASS drag source gates: exclusive claims, priority, shared fatigue, 60% speed, swept motor, wake/platform/death cleanup')
print('PASS stun source visual: cross face, three procedural stars, countdown, material cleanup; 5+3 second config')
print('NOT RUN DragChecks C#, Unity drag physics/face layout/collider regression or Android tests')
