from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena';S=R/'Server'
paths=[R/'Contracts/networld.json',A/'Resources/Data/networld.json',S/'src/main/resources/networld.json']
raw=paths[0].read_bytes();assert all(p.read_bytes()==raw for p in paths)
w=json.loads(raw);assert w['tickRate']==30 and w['snapshotEvery']==3 and w['durationSeconds']==120
assert len(w['maps'])==3
for m in w['maps']:
 assert len(m['spawns'])==4
 for b in m['boxes']:assert b['left']<b['right'] and b['bottom']<b['top']
 for spawn in m['spawns']:
  assert spawn['y']>m['eliminationY']
  assert not any(spawn['x']-w['width']/2<b['right']-1e-6 and spawn['x']+w['width']/2>b['left']+1e-6 and spawn['y']<b['top']-1e-6 and spawn['y']+w['standingHeight']>b['bottom']+1e-6 for b in m['boxes']),('spawn overlap',m['id'],spawn)
java=(S/'src/main/java/com/itmearena/application/NetMotion.java').read_text()
expected=java.replace('package com.itmearena.application;','using System;\nnamespace ItmeArena.Runtime {').replace('public final class NetMotion','public static class NetworkMotion').replace('public static final class Body','[Serializable] public sealed class Body').replace('NetWorld','NetworkWorld').replace('boolean','bool').replace('for(var q:map.boxes)','foreach(var q in map.boxes)').replace('Math.min','Math.Min').replace('Math.max','Math.Max').replace('Math.abs','Math.Abs')+'\n}\n'
assert expected==(A/'Runtime/NetworkMotion.cs').read_text()
m=(S/'src/main/java/com/itmearena/application/NetMatch.java').read_text()
for token in ['Double.isFinite','p.inputs.size()>=world.maxQueue','input.inputSequence()<=p.received','input.clientTick()>tick+world.maxQueue+6','steps<world.maxCatchup','p.ack=input.inputSequence()','b.body.x=spawn.x','world.durationSeconds*1000L','phase.equals("FINISHED")']:assert token in m,token
c=(A/'Runtime/OnlineArena.cs').read_text()
for token in ['pending.RemoveAll','foreach(var c in pending)','Interpolated','SHA256.Create()','p26-network.csv','outgoing.Count>0','world.maxQueue','ArtificialLatencyMs']:assert token in c
print('PASS shared JSON byte identity/SHA256 '+hashlib.sha256(raw).hexdigest())
print('PASS all three map boxes and 12 non-overlapping spawns; Java/C# movement source translation parity; input authority/queue/bounds, prediction/replay/interpolation/metrics source gates')
print('NOT RUN Java/C# compilation, cross-runtime numeric replay, real 2-client snapshot clocks, latency correction measurement, Android network or P20 device acceptance')
