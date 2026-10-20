"""P29 source/contracts/lifecycle checks; not Unity execution."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena/Runtime'
def read(n):return (A/n).read_text()
result=read('MatchResultScreen.cs');lab=read('MovementLab.cs');online=read('OnlineArena.cs');lobby=read('LobbyPanel.cs');menu=read('MainMenuScreen.cs')
assert 'long damage1,long damage2' in result
assert 'long team1Damage,team2Damage' in lab
for term in ['team1Remaining','team2Remaining','team1Damage','team2Damage','reason']:assert term in online
for term in ['if(resultScreen==null)','input.SetPaused(true)','HomeRequested?.Invoke()','Closed=null;ReplayRequested=null;HomeRequested=null;']:assert term in lab
for term in ['Task.WhenAny(ack.Task,timeout)','await ack.Task','arena?.ExitPending()','arena?.ExitFailed(status.text)','code.text=""','arena.gameObject.SetActive(false)','if(exiting)']:assert term in lobby
assert 'Received=null;Failed=null' in read('LobbyTransport.cs')
assert 'history.Clear();leave=replay=home=null' in online
assert 'movementLab.HomeRequested+=' in menu and 'request?.Replay()' in menu
assert 'RewardStatusView' in result and 'PostAuthenticatedAsync' not in result
assert 'p29-flow.csv' in read('FlowDiagnostics.cs')
for row in json.loads((R/'Docs/requirements.json').read_text()):
 if row['stage']>32:assert row['status']=='bekliyor'
print('PASS P29 result fields, local/online exit/replay fences, read-only reward display, cleanup and P30 gate (source checks).')
print('NOT RUN Unity/C# compilation, actual UI navigation, mobile safe-area or device memory profiling.')
