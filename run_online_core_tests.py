"""Compile REAL core sources with transport/JSON-load-only boundary stubs, never full Spring server."""
from pathlib import Path
import json,subprocess,tempfile
R=Path(__file__).resolve().parents[1];S=R/'Server/src/main/java/com/itmearena/application'
w=json.loads((R/'Contracts/networld.json').read_text())
with tempfile.TemporaryDirectory(prefix='itme-p25-core-') as tmp:
 d=Path(tmp);files=[]
 def put(name,text):
  p=d/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);files.append(str(p))
 put('org/springframework/stereotype/Component.java','package org.springframework.stereotype;public @interface Component {}')
 put('org/springframework/beans/factory/annotation/Value.java','package org.springframework.beans.factory.annotation;public @interface Value {String value();}')
 put('com/fasterxml/jackson/databind/ObjectMapper.java','package com.fasterxml.jackson.databind;public class ObjectMapper {public <T>T readValue(byte[] b,Class<T> c){throw new UnsupportedOperationException("JSON load not under test");}}')
 put('com/itmearena/application/AnonymousAuth.java','package com.itmearena.application;public class AnonymousAuth {public static String hash(String s){throw new UnsupportedOperationException();}}')
 lines=['package com.itmearena.application;import java.util.*;final class Fixture {static NetWorld world(){var w=new NetWorld();']
 def literal(v):return json.dumps(v)
 for k,v in w.items():
  if k=='maps':continue
  if isinstance(v,dict):
   lines.append(f'w.{k}=new NetWorld.{k.title()}Settings();')
   for field,val in v.items():lines.append(f'w.{k}.{field}={literal(val)};')
  else:lines.append(f'w.{k}={literal(v)};')
 lines+=['w.hash="test-world";w.maps=new ArrayList<>();']
 for arena in w['maps']:
  lines+=['{var a=new NetWorld.Arena();',f'a.id={literal(arena["id"])};a.eliminationY={arena["eliminationY"]};a.boxes=new ArrayList<>();a.spawns=new ArrayList<>();']
  for b in arena['boxes']:
   lines+=['{var b=new NetWorld.Box();']+[f'b.{k}={literal(v)};' for k,v in b.items()]+['a.boxes.add(b);}']
  for spawn in arena['spawns']:lines +=['{var p=new NetWorld.Spawn();']+[f'p.{k}={v};' for k,v in spawn.items()]+['a.spawns.add(p);}']
  lines+=['w.maps.add(a);}']
 lines+=['return w;}}'];put('com/itmearena/application/Fixture.java','\n'.join(lines))
 for name in ['NamePolicy','ChallengeStore','ShopStore','CompletedMatch','RewardStore','OutboundMailbox','LobbyRegistry','AuthFailure','NetWorld','NetMotion','NetMatch','NetActions','NetHazards']:files.append(str(S/(name+'.java')))
 files.append(str(R/'Tools/fixtures/OnlineCoreScenarios.java'))
 files.append(str(R/'Tools/fixtures/ChallengeScenarios.java'))
 files.append(str(R/'Tools/fixtures/DownedDragScenarios.java'))
 files.append(str(R/'Tools/fixtures/FreeNameScenarios.java'))
 files.append(str(R/'Tools/fixtures/V12Scenarios.java'))
 files.append(str(R/'Tools/fixtures/MapAccessScenarios.java'))
 files.append(str(R/'Tools/fixtures/ReconnectScenarios.java'))
 files.append(str(R/'Tools/fixtures/RewardScenarios.java'))
 files.append(str(R/'Tools/fixtures/ShopScenarios.java'))
 files.append(str(R/'Tools/fixtures/ResultFlowScenarios.java'))
 files.append(str(R/'Tools/fixtures/LoopbackMailboxProbe.java'))
 classes=d/'classes';classes.mkdir()
 subprocess.run(['java','-m','jdk.compiler/com.sun.tools.javac.Main','-d',str(classes),*files],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.OnlineCoreScenarios'],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.ReconnectScenarios'],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.LoopbackMailboxProbe',str(R/'Docs/P26_TCP_LOOPBACK.csv')],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.RewardScenarios'],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.ShopScenarios'],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.ResultFlowScenarios'],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.ChallengeScenarios'],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.DownedDragScenarios'],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.FreeNameScenarios'],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.V12Scenarios'],check=True)
 subprocess.run(['java','-ea','-cp',str(classes),'com.itmearena.application.MapAccessScenarios'],check=True)
print('PASS production Java core compilation and executed scenarios; fixture generated from exact shared JSON.')
print('NOT RUN full Spring/Jackson/WebSocket/PostgreSQL server integration, Unity/C#, Android or multi-client transport.')
