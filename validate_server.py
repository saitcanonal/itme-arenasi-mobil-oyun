from pathlib import Path
import json,xml.etree.ElementTree as ET,re
R=Path(__file__).resolve().parents[1];S=R/'Server'
ET.parse(S/'pom.xml')
sql=(S/'src/main/resources/db/migration/V1__foundation.sql').read_text()
for table in ['accounts','player_profiles','characters','maps','accessories','inventory','wallets','wallet_ledger','match_results','match_participants']:assert 'CREATE TABLE '+table+' (' in sql
assert "CHECK(authority='server')" in sql and 'CHECK(balance>=0)' in sql and 'idempotency_key VARCHAR(120) NOT NULL UNIQUE' in sql
seed=(S/'src/main/resources/db/migration/V2__catalog.sql').read_text()
for table,count in [('characters',5),('maps',3),('accessories',26)]:assert seed.count('INSERT INTO '+table)==count
catalog=json.loads((R/'UnityProject/Assets/ItmeArena/Resources/Data/catalog.json').read_text())
for group in ['characters','maps','accessories']:
 for item in catalog[group]:assert "'"+item['id']+"'" in seed
boundary=(S/'src/main/java/com/itmearena/adapters/http/ApiBoundary.java').read_text()
assert 'req.getMethod().equals("GET")' in boundary and 'req.getQueryString()!=null' in boundary
assert 'ENDPOINT_UNAVAILABLE' in boundary and 'UUID.randomUUID()' in boundary
api=json.loads((R/'Contracts/api-v1.openapi.json').read_text());assert set(api['paths'])=={'/api/v1/catalog','/actuator/health','/api/v1/accounts/anonymous','/api/v1/profile','/api/v1/wallet','/api/v1/matches/{id}/reward','/api/v1/shop/catalog','/api/v1/shop/state','/api/v1/shop/purchase','/api/v1/shop/equip'}
assert not (S/'.env').exists()
assert '${DB_PASSWORD}' in (S/'src/main/resources/application.yml').read_text()
assert '127.0.0.1:8080:8080' in (S/'compose.yml').read_text()
client=(R/'UnityProject/Assets/ItmeArena/Runtime/ServerApiClient.cs').read_text()
for token in ['request.Abort()','request.timeout=8','UnityWebRequest.Get','data.schemaVersion!=1','uri.Scheme!="https"']:assert token in client
print('PASS structural: Maven XML, ten relational models, FK/check/idempotency boundaries, 5/3/26 seed IDs, API allowlist/contracts, environment configuration and Unity HTTP error/cancel path')
print('NOT RUN: Java compile, dependency resolution, PostgreSQL/Flyway execution, Testcontainers, service restart, Unity/Android network integration')
