from pathlib import Path
import re
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena'
b=(A/'Runtime/BotController.cs').read_text();c=(A/'Core/BotRules.cs').read_text();lab=(A/'Runtime/MovementLab.cs').read_text()
for token in ['Physics2D.Linecast','<=9','clock.Ready(now)','!match.Flow.IsAlive','roster[i].Team==roster[index].Team','Pulse(Control.Push)','Set(Control.Grip,true)','Pulse(Control.Jump)','stuck>1.4f','index*20-(int)control']:assert token in b,token
for forbidden in ['QueueAttack','ApplyEnvironmentImpulse','ResetPosition','SetFacing','WebSocket','HttpClient']:assert forbidden not in b,forbidden
names=re.findall(r'"([A-Za-z0-9_.]+)"',c);assert len(names)==25 and len(set(names))==25 and all(5<=len(n)<=12 for n in names)
source=(R/'References/S01-text.txt').read_text();assert all(n in source for n in names)
assert 'executionOrder: -100' in (A/'Runtime/BotController.cs.meta').read_text()
for arena in ['StairwellArena','FactoryArena','CraterArena']:assert 'bool WarningAt(Vector2 p)' in (A/('Runtime/'+arena+'.cs')).read_text()
for token in ['if(BotMode)for','ReplayRequested','selectionRequest.NameAt','replay.gameObject.SetActive(true)']:assert token in lab
assert 'VersusIntro.Show' in (A/'Runtime/SelectionScreen.cs').read_text()
print('PASS source wiring: independent bot controls, shared motor/combat/grip, LOS/range, reaction gate, warning queries, replay')
print('PASS all 25 nickname pool entries match S01 and have unique 5–12 character names')
print('NOT RUN C# BotChecks, Unity import/physics/navigation, offline device loop or Android performance')
