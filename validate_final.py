"""Final local SQLite migration execution and delivery audit integrity."""
from pathlib import Path
import json,re,sqlite3
R=Path(__file__).resolve().parents[1]
s=(R/'UnityProject/Assets/ItmeArena/Runtime/LocalCache.cs').read_text()
def schema(n):return re.findall(r'"((?:[^"\\]|\\.)*)"',s.split('string[] SchemaV'+str(n)+'={')[1].split('};')[0])
db=sqlite3.connect(':memory:')
for n in [1,2,3]:
 for sql in schema(n):db.execute(sql)
db.execute("INSERT INTO profiles VALUES('production','preserved-profile')")
db.execute("INSERT INTO settings VALUES('itme.quality.v1',2)");db.execute("INSERT INTO settings VALUES('itme.sound.v1',0)");db.commit()
db.execute('BEGIN')
for sql in schema(4):db.execute(sql)
db.rollback()
assert db.execute("SELECT receipt FROM profiles").fetchone()[0]=='preserved-profile'
try:db.execute("INSERT INTO settings VALUES('itme.sound.volume.v1',55)");raise AssertionError('v3 constraint disappeared after rollback')
except sqlite3.IntegrityError:pass
db.rollback()
db.execute('BEGIN')
for sql in schema(4):db.execute(sql)
db.commit()
assert db.execute('SELECT receipt FROM profiles').fetchone()[0]=='preserved-profile'
assert db.execute("SELECT value FROM settings WHERE key='itme.quality.v1'").fetchone()[0]==2
for key in ['itme.sound.volume.v1','itme.music.volume.v1']:
 for value in [0,28,55,75,100]:db.execute('INSERT OR REPLACE INTO settings VALUES(?,?)',(key,value))
 for value in [-1,101]:
  try:db.execute('INSERT OR REPLACE INTO settings VALUES(?,?)',(key,value));raise AssertionError('invalid volume accepted')
  except sqlite3.IntegrityError:pass
for v in [0,1]:db.execute("INSERT OR REPLACE INTO settings VALUES('itme.vibration.v1',?)",(v,))
try:db.execute("INSERT OR REPLACE INTO settings VALUES('itme.vibration.v1',2)");raise AssertionError('invalid haptic accepted')
except sqlite3.IntegrityError:pass
assert 'Default(key)' in s and 'before-v4.bak' in s and 'PRAGMA user_version=4' in s
requirements=json.loads((R/'Docs/requirements.json').read_text());audit=json.loads((R/'Docs/P32_REQUIREMENT_AUDIT.json').read_text())
assert {x['id'] for x in requirements}=={x['id'] for x in audit} and len(audit)==104
for row in audit:
 assert row['sources'] and row['evidence'] and row['remaining']
 for file in row['evidence']:assert (R/file).exists(),file
print('PASS executed SQLite v3→v4: profile/quality/sound retained, 0..100 volumes and boolean haptics enforced.')
print('PASS all 104 requirements have source, existing evidence and explicit remaining acceptance; not a claim of full runtime acceptance.')
