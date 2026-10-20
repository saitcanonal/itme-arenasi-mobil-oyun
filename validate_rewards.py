"""SQLite transaction/constraint experiment using production SQL strings; NOT a PostgreSQL/JDBC test."""
from pathlib import Path
import json,re,sqlite3,tempfile,concurrent.futures
R=Path(__file__).resolve().parents[1];S=R/'Server/src/main/java/com/itmearena';source=(S/'application/RewardStore.java').read_text()
queries=re.findall(r'"((?:INSERT INTO|UPDATE wallets|SELECT [^"]+ FROM)[^"]*)"',source)
def query(prefix):
 found=[q for q in queries if q.startswith(prefix)];assert len(found)==1,(prefix,found)
 return found[0].replace(' FOR UPDATE','').replace('now()','CURRENT_TIMESTAMP')
with tempfile.TemporaryDirectory() as d:
 path=str(Path(d)/'experiment.db')
 def connect():
  db=sqlite3.connect(path,timeout=10);db.execute('PRAGMA foreign_keys=ON');return db
 with connect() as db:
  db.executescript('''CREATE TABLE wallets(player_id TEXT PRIMARY KEY,balance INTEGER NOT NULL DEFAULT 0 CHECK(balance>=0),revision INTEGER NOT NULL DEFAULT 0);
CREATE TABLE wallet_ledger(id TEXT PRIMARY KEY,player_id TEXT REFERENCES wallets(player_id),delta INTEGER NOT NULL,balance_after INTEGER NOT NULL,reason TEXT,idempotency_key TEXT UNIQUE);
CREATE TABLE match_results(id TEXT PRIMARY KEY,map_id TEXT,winning_team INTEGER,reason TEXT,authority TEXT CHECK(authority='server'),finished_at TEXT,duration_ms INTEGER,result_hash TEXT);
CREATE TABLE match_participants(match_id TEXT REFERENCES match_results(id),player_id TEXT REFERENCES wallets(player_id),team INTEGER,damage INTEGER,eliminated BOOLEAN,PRIMARY KEY(match_id,player_id));''')
  migration=(R/'Server/src/main/resources/db/migration/V4__match_rewards.sql').read_text();migration=migration[migration.index('CREATE TABLE match_rewards'):].replace('now()','CURRENT_TIMESTAMP');db.executescript(migration)
  db.executemany('INSERT INTO wallets(player_id) VALUES(?)',[('a',),('b',)])
 def persist(match,eligible=True,fail=False,fingerprint='hash'):
  with connect() as db:
   db.execute('BEGIN IMMEDIATE') # SQLite serialization substitutes for PG row locks in this experiment.
   db.execute(query('INSERT INTO match_results'),(match,'kirik_fabrika',1,120000,fingerprint))
   assert db.execute(query('SELECT result_hash'),(match,)).fetchone()[0]==fingerprint
   for player in ['a','b']:
    db.execute(query('INSERT INTO match_participants'),(match,player,1 if player=='a' else 2,10,False))
    if db.execute(query('SELECT 1 FROM match_rewards'),(match,player)).fetchone():continue
    if player=='a' and not eligible:db.execute(query('INSERT INTO match_rewards(match_id,player_id,status,amount) '),(match,player));continue
    balance=db.execute(query('SELECT balance FROM wallets'),(player,)).fetchone()[0];after=balance+200;ledger=match+player
    db.execute(query('INSERT INTO wallet_ledger'),(ledger,player,200,after,'match:'+match+':'+player))
    if fail:raise RuntimeError('injected failure after ledger')
    db.execute(query('UPDATE wallets'),(after,player));db.execute(query('INSERT INTO match_rewards(match_id,player_id,status,amount,ledger_id)'),(match,player,200,ledger))
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(lambda _:persist('m1'),range(32)))
 with connect() as db:assert db.execute('SELECT balance FROM wallets WHERE player_id=\'a\'').fetchone()[0]==200;assert db.execute('SELECT count(*) FROM wallet_ledger').fetchone()[0]==2
 try:persist('fail',fail=True)
 except RuntimeError:pass
 else:raise AssertionError('fault injection')
 with connect() as db:assert db.execute('SELECT count(*) FROM match_results WHERE id=\'fail\'').fetchone()[0]==0;assert db.execute('SELECT balance FROM wallets WHERE player_id=\'a\'').fetchone()[0]==200
 try:persist('m1',fingerprint='forged')
 except AssertionError:pass
 else:raise AssertionError('conflict accepted')
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(persist,['m2','m3']))
 persist('m4',eligible=False)
 with connect() as db:assert db.execute('SELECT balance FROM wallets WHERE player_id=\'a\'').fetchone()[0]==600;assert db.execute('SELECT balance FROM wallets WHERE player_id=\'b\'').fetchone()[0]==800;assert db.execute('SELECT status,amount FROM match_rewards WHERE match_id=\'m4\' AND player_id=\'a\'').fetchone()==('ineligible',0)
for token in ['c.setAutoCommit(false)','c.commit()','c.rollback()','FOR UPDATE','ON CONFLICT(id) DO NOTHING','Math.addExact','AMOUNT=300']:assert token in source
controller=(S/'adapters/http/RewardController.java').read_text();assert '@PostMapping' not in controller and 'auth.current(bearer)' in controller
assert 'pending_or_unverified' in source
api=json.loads((R/'Contracts/api-v1.openapi.json').read_text());assert '/api/v1/wallet' in api['paths'] and '/api/v1/matches/{id}/reward' in api['paths']
print('P27 LEGACY SQL ADAPTATION (200-coin fixture, not current pricing): PASS SQLite-only SQL experiment: 32 parallel duplicate submissions, different-match concurrency, injected rollback, result conflict, ineligible zero; source transaction/authority checks')
print('NOT RUN production PostgreSQL locking/Flyway/JDBC concurrent integration test, HTTP auth routes, Unity wallet/reward UI')
