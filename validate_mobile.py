from pathlib import Path
import re,sqlite3,csv
R=Path(__file__).resolve().parents[1];A=R/'UnityProject/Assets/ItmeArena'
s=(A/'Runtime/LocalCache.cs').read_text()
def schema(name):return re.findall(r'"([^"\n]+)"',s.split('string[] '+name+'={',1)[1].split('};',1)[0])
db=sqlite3.connect(':memory:')
for name in ['SchemaV1','SchemaV2']:
 for sql in schema(name):db.execute(sql)
db.execute("INSERT INTO settings VALUES('itme.sound.v1',0)");db.execute("INSERT INTO profiles VALUES('development','preserved')");db.commit()
try:
 db.execute('BEGIN IMMEDIATE')
 for sql in schema('SchemaV3'):db.execute(sql)
 db.execute('INSERT INTO nonexistent VALUES(1)')
except sqlite3.DatabaseError:db.rollback()
assert db.execute("SELECT value FROM settings").fetchone()==(0,)
for sql in schema('SchemaV3'):db.execute(sql)
for value in range(3):
 db.execute("INSERT OR REPLACE INTO settings VALUES('itme.quality.v1',?)",(value,))
assert db.execute('SELECT receipt FROM profiles').fetchone()==('preserved',)
for key,val in [('itme.sound.v1',2),('itme.quality.v1',3),('itme.quality.v1',-1)]:
 try:db.execute('INSERT OR REPLACE INTO settings VALUES(?,?)',(key,val));raise AssertionError('invalid setting accepted')
 except sqlite3.IntegrityError:pass
assert db.execute("SELECT value FROM settings WHERE key='itme.sound.v1'").fetchone()==(0,)
print('PASS: actual SQLite v2→v3 migration and DDL rollback preserve settings/profile; quality 0..2 accepted and invalid values rejected')
q=(A/'Runtime/MobileQuality.cs').read_text();assert 'Level==0?30:60' in q and 'fixedDeltaTime' not in q
for n in ['CharacterMotor','PushCombatWorld','BotController']:assert 'using(TickMarker.Auto())' in (A/('Runtime/'+n+'.cs')).read_text()
assert '%MobileQuality.ImpactBudget' in (A/'Runtime/ArenaFeedback.cs').read_text()
atlas=(A/'Editor/MobileBuildTools.cs').read_text()
for group in ['Characters','Accessories','MapPreviews']:
 assert (A/'Resources'/group).is_dir() and '"'+group+'"' in atlas
assert 'BuildOptions.Development' in atlas and 'BuildResult.Succeeded' in atlas
rows=list(csv.DictReader((R/'Docs/P20_CIHAZ_TESTI.csv').open()));assert len(rows)==10
assert all(r['durum']=='yapılmadı' for r in rows)
print('PASS: quality targets/pool quotas, three atlas groups, profiler scopes, development build guard and honest 10-match table (source checks)')
print('NOT RUN: Unity C# compilation, atlas packing, APK, actual device performance, thermal/touch/crash/save-loss acceptance')
