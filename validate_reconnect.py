from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];S=R/'Server/src/main/java/com/itmearena';A=R/'UnityProject/Assets/ItmeArena/Runtime'
w=json.loads((R/'Contracts/networld.json').read_text());c=w['reconnect'];assert w['version']==3 and 1<=c['graceSeconds']<=120 and 0<c['heartbeatSeconds']<c['idleSeconds'] and c['maxInputAgeTicks']==15
checks={S/'application/LobbyRegistry.java':['leases.remove(player)','out.addAll(detach(previous))','r.match.reconnect(player)','reconnect_timeout','voluntary_leave','HOST_LEFT','cmd.sequence()))'],S/'application/NetMatch.java':['p.ack=p.received','p.inputs.clear()','!p.connected','tick-input.clientTick()<=world.reconnect.maxInputAgeTicks','p.connected,p.connected?0'],S/'application/OutboundMailbox.java':['controls.size()>=32','latest=item','coalesced++','inFlightMs'],S/'adapters/websocket/LobbySocket.java':['new ArrayBlockingQueue<>(4000)','inFlightMs()>3000','@PreDestroy','rooms.idleSeconds()*1000'],A/'LobbyPanel.cs':['recoveryUntil','StopRecovery','OnApplicationPause','token.Register(()=>candidate.Dispose())','e.type=="connected"&&recovering'],A/'LobbyTransport.cs':['waitingSends)>8','wait.CancelAfter(2000)','timeout.CancelAfter(2000)','e.replySequence==pingSequence'],A/'OnlineArena.cs':['inputSequence=Array.Find(initial.actors','p26-network.csv','pending.Clear();outgoing.Clear();']}
for p,tokens in checks.items():
 s=p.read_text()
 for token in tokens:assert token in s,(p.name,token)
assert not any(x['status']!='bekliyor' for x in json.loads((R/'Docs/requirements.json').read_text()) if x['stage']>32)
print('PASS P26 config, authenticated same-actor reconnect, queue/epoch guards, timeout policy, background/retry UI and RTT source checks')
print('NOT RUN full Spring/WebSocket, Unity/C# build, real multi-device/mobile network acceptance')
