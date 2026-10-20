from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];S=R/'Server';A=R/'UnityProject/Assets/ItmeArena'
a=(S/'src/main/java/com/itmearena/application/AnonymousAuth.java').read_text()
for token in ['@Transactional','pg_advisory_xact_lock','FOR UPDATE','REGISTRATION_CONFLICT','expires_at>now()',"a.status='active'",'HmacSHA256','AUTH_SECRET','hash(bearer.substring(7))']:assert token in a,token
assert 'token_hash CHAR(64) NOT NULL UNIQUE' in (S/'src/main/resources/db/migration/V3__anonymous_sessions.sql').read_text()
v=(R/'UnityProject/Assets/Plugins/Android/SessionVault.java').read_text()
for token in ['AndroidKeyStore','AES/GCM/NoPadding','getNoBackupFilesDir','f.finishWrite(out)','f.failWrite(out)']:assert token in v
c=(A/'Runtime/ProductionRegistrationService.cs').read_text()
assert c.index('SecureSessionStore.Save(s)')<c.index('await Send<AnonymousResponse>')
for token in ['RandomNumberGenerator.Create','request.redirectLimit=0','request.Abort()','if(e.Status!=401)throw','SecureSessionStore.Save(s);','return Remember(result.profile);']:assert token in c,token
f=(A/'Runtime/FirstLaunchScreen.cs').read_text()
assert 'new ProductionRegistrationService(config.apiBaseUrl)' in f and 'await service.GetCurrentAsync' in f and 'current.playerId!=receipt.profile.playerId' in f
assert not json.loads((A/'Resources/Data/onboarding.json').read_text())['useDevelopmentService']
api=json.loads((R/'Contracts/api-v1.openapi.json').read_text());assert '/api/v1/accounts/anonymous' in api['paths'] and '/api/v1/profile' in api['paths']
assert 'public class RegistrationServiceException' in (A/'Core/OnboardingFlow.cs').read_text()
print('PASS source gates: serializable anonymous registration, token hash/expiry, protected profile, Android encrypted atomic secret storage, pre-request persistence, real first-launch binding and versioned contract')
print('NOT RUN Java/C#/Android plugin compilation, PostgreSQL concurrency, HTTPS session flow, Keystore device persistence or recovery acceptance')
