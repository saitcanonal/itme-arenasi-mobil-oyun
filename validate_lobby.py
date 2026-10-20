from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];S=R/'Server';A=R/'UnityProject/Assets/ItmeArena'
r=(S/'src/main/java/com/itmearena/application/LobbyRegistry.java').read_text()
for token in ['synchronized List<Delivery> command','synchronized List<Delivery> detach','r.members.size()>=r.capacity','random.nextInt(90000)','retired.containsKey(candidate)','clock.getAsLong()+600000','++r.count>10','ROOM_FULL','ROOM_NOT_FOUND','MATCH_STARTED','CONSENT_REQUIRED','HOST_LEFT','allMatch(Player::consent)']:
 assert token in r,token
socket=(S/'src/main/java/com/itmearena/adapters/websocket/LobbySocket.java').read_text()
for token in ['auth.current','setTextMessageSizeLimit(2048)','ConcurrentWebSocketSessionDecorator','@Scheduled','rooms.detach','rooms.expire']:assert token in socket
client=(A/'Runtime/LobbyTransport.cs').read_text();panel=(A/'Runtime/LobbyPanel.cs').read_text()
assert 'SemaphoreSlim(1,1)' in client and 'socket.Abort()' in client and 'buffer=new byte[65536]' in client
assert 'epoch==generation' in panel and 'ReferenceEquals(transport,candidate)' in panel
assert 'P26' in panel and 'LobbyPanel' in (A/'Runtime/MainMenuScreen.cs').read_text()
contract=json.loads((R/'Contracts/lobby-v1.schema.json').read_text());assert set(contract['properties']['type']['enum'])=={'create','join','leave','map','team','consent','start','ping','input'}
assert (S/'src/test/java/com/itmearena/LobbyRegistryTest.java').is_file() and (S/'src/test/java/com/itmearena/LobbyWebSocketTest.java').is_file()
print('PASS source gates: room capacity/sequence serialization, collision/TTL/rate, host/membership/consent, authenticated WS adapter, Unity single-send lifecycle and P25 distinction')
print('NOT RUN: Java unit/integration tests, real WS handshake, two-device lobby, Android IL2CPP or load acceptance')
