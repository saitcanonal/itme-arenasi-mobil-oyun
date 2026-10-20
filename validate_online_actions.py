from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena';S=R/'Server/src/main/java/com/itmearena/application';w=json.loads((R/'Contracts/networld.json').read_text())
assert w['version']>=2
for k,f in [('push','push'),('grip','grip'),('ultimate','ultimate'),('stairs','stairwell'),('factory','factory'),('crater','crater')]:assert w[k]==json.loads((A/f'Resources/Data/{f}.json').read_text()),k
for m in w['maps']:
 ids=[b['id'] for b in m['boxes']];assert len(ids)==len(set(ids));assert all(b['enabled'] for b in m['boxes'])
 if m['id']=='merdiven_boslugu':assert len({b['group'] for b in m['boxes'] if b['kind']=='fragile'})==4 and sum(b['kind']=='lift' for b in m['boxes'])==1
 if m['id']=='kirik_fabrika':assert sum(b['kind']=='upper' for b in m['boxes'])==2 and sum(b['kind']=='trap' for b in m['boxes'])==2
 if m['id']=='kizil_krater':assert len({b['group'] for b in m['boxes'] if b['kind']=='bridge'})==6 and sum(b['kind']=='moving' for b in m['boxes'])==1
schema=json.loads((R/'Contracts/lobby-v1.schema.json').read_text());assert schema['additionalProperties'] is False
assert {'vertical','push','gripPressed','gripReleased','ultimate'}<=schema['properties'].keys()
assert not {'position','damage','reward','body'}&schema['properties'].keys()
c=(A/'Runtime/OnlineArena.cs').read_text()
for token in ['e.id<=lastEventId','lastEventId=e.id','map.boxes=state.surfaces','input.SetUltimateReady','CanPredict','Control.Grip','Control.Push','Control.Ultimate','DrawHand','stunMarkers','warningFatigue']:assert token in c,token
m=(S/'NetMatch.java').read_text()
for token in ['world.copyArena','actions.attacks(frame)','actions.grips(frame)','hazards.hits()','events.size()>64','damageWinner()']:assert token in m,token
# Conservative wire size estimate using full surface data, 4 actors and max event ring.
for arena in w['maps']:
 message=dict(surfaces=arena['boxes'],actors=[dict(playerId='a'*36,body={'x':-12.123456789,'y':5.123456789},padding='x'*900)]*4,events=[dict(id=999999,tick=999999,kind='surface_restore',source='s'*36,target='t'*36,reason='r'*80,value=999.999)]*64,padding='x'*2000)
 assert len(json.dumps(message).encode())<65536
print('PASS P25 unchanged gameplay settings, stable surface IDs/groups, command authority schema, client event dedup and interaction rendering source gates, conservative snapshot buffer budget')
print('NOT RUN Unity visual/import/compile, actual serialized snapshot transport or Android touch/latency acceptance')
