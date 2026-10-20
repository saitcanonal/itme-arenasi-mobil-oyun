"""Source guards and packaging checks, not Unity or signing execution."""
from pathlib import Path
import json,subprocess,csv
R=Path(__file__).resolve().parents[1]
s=(R/'UnityProject/Assets/ItmeArena/Editor/ReleaseBuildTools.cs').read_text()
for term in ['ITME_API_URL','ITME_VERSION_CODE','ITME_KEYSTORE_PATH','ITME_KEY_ALIAS','ITME_KEYSTORE_PASSWORD','ITME_KEY_PASSWORD','finally','BuildOptions.None','BuildOptions.Development','ARM64','IL2CPP','(AndroidSdkVersions)36','cfg.useDevelopmentService=false','cfg.networkArtificialLatencyMs=0','File.WriteAllText(Config,original)']:assert term in s,term
assert 'SetApplicationIdentifier' not in s
assert 'GetApplicationIdentifier' in s
settings=(R/'UnityProject/ProjectSettings/ProjectSettings.asset').read_text();assert 'com.codevacore.itmearenasi.dev' in settings and 'AndroidTargetSdkVersion: 36' in settings
modules=json.loads((R/'UnityProject/Packages/manifest.json').read_text())['dependencies']
assert modules['com.unity.modules.screencapture']=='1.0.0' and modules['com.unity.modules.androidjni']=='1.0.0'
subprocess.run(['bash','-n',str(R/'Tools/build_android_mac.sh')],check=True)
for name in ['P31_DEVICE_TESTS.csv','P31_TEN_MATCHES.csv']:
 rows=list(csv.DictReader((R/'Docs'/name).open()));assert rows and all(x.get('status',x.get('result'))=='NOT_RUN' for x in rows)
for p in R.rglob('*'):
 if p.is_file():assert p.suffix.lower() not in ['.jks','.keystore','.p12','.pfx','.aab','.apk'],p
for x in json.loads((R/'Docs/requirements.json').read_text()):
 if x['stage']>32:assert x['status']=='bekliyor'
print('PASS P31 build guard/source checks, Mac shell syntax, preserved ID, target API36 and explicit JNI/ScreenCapture dependencies.')
print('PASS no signing keys/APK/AAB shipped; device/10-match rows honestly NOT_RUN; P32 pending.')
print('NOT RUN Unity compilation, Android build, signing, 16KB native validation, live server or device tests.')
