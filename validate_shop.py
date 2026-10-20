"""Production SQL on a SQLite adaptation; PostgreSQL row-lock semantics require ShopStoreTest."""
from pathlib import Path
import json,re,sqlite3,tempfile,concurrent.futures,uuid
R=Path(__file__).resolve().parents[1];S=R/'Server/src/main/java/com/itmearena';A=R/'UnityProject/Assets/ItmeArena'
s=(S/'application/ShopStore.java').read_text();queries=re.findall(r'"((?:SELECT |INSERT INTO |UPDATE |DELETE FROM )[^"\n]+)"',s)
def q(prefix):
 matches=[v for v in queries if v.startswith(prefix)];assert len(matches)==1,(prefix,matches)
 return matches[0].replace(' FOR UPDATE','').replace(' FOR SHARE','').replace('now()','CURRENT_TIMESTAMP')
items=json.loads((A/'Resources/Data/catalog.json').read_text())['accessories']
with tempfile.TemporaryDirectory() as tmp:
 file=str(Path(tmp)/'shop.db')
 def conn():
  db=sqlite3.connect(file,timeout=10);db.row_factory=sqlite3.Row;db.execute('PRAGMA foreign_keys=ON');return db
 with conn() as db:
  db.executescript('''CREATE TABLE characters(id TEXT PRIMARY KEY);
CREATE TABLE accessories(id TEXT PRIMARY KEY,purchasable BOOLEAN DEFAULT false);
CREATE TABLE player_profiles(id TEXT PRIMARY KEY,character_id TEXT REFERENCES characters(id),revision INTEGER DEFAULT 0,updated_at TEXT);
CREATE TABLE wallets(player_id TEXT PRIMARY KEY REFERENCES player_profiles(id),balance INTEGER CHECK(balance>=0),revision INTEGER DEFAULT 0);
CREATE TABLE wallet_ledger(id TEXT PRIMARY KEY,player_id TEXT REFERENCES wallets(player_id),delta INTEGER,balance_after INTEGER,reason TEXT,idempotency_key TEXT UNIQUE);
CREATE TABLE inventory(player_id TEXT REFERENCES player_profiles(id),accessory_id TEXT REFERENCES accessories(id),source_key TEXT UNIQUE,PRIMARY KEY(player_id,accessory_id));''')
  db.executemany('INSERT INTO characters VALUES(?)',[(x,) for x in sorted({a['characterId'] for a in items})]);db.executemany('INSERT INTO accessories(id) VALUES(?)',[(a['id'],) for a in items]);db.executescript((R/'Server/src/main/resources/db/migration/V5__shop_inventory_equipment.sql').read_text().replace('now()','CURRENT_TIMESTAMP'))
  for p,balance in [('a',20000),('b',20000),('poor',0)]:db.execute("INSERT INTO player_profiles(id,character_id) VALUES(?,'pofuk')",(p,));db.execute('INSERT INTO wallets(player_id,balance) VALUES(?,?)',(p,balance))
  products=list(db.execute('SELECT * FROM shop_products'));assert len(products)==27
  for item in items:
   row=db.execute('SELECT * FROM shop_products WHERE id=?',(item['id'],)).fetchone();assert row['price']==item['examplePrice']>=2000 and row['slot']==item['slot'] and row['character_id']==item['characterId']
 def buy(player,request,item='pofuk_baret',price=2000,version=1,fail=False):
  with conn() as db:
   db.execute('BEGIN IMMEDIATE');wallet=db.execute(q('SELECT balance,revision FROM wallets'),(player,)).fetchone();balance=wallet['balance'];old=db.execute(q('SELECT * FROM purchase_requests'),(player,request)).fetchone()
   if old:
    if (old['product_id'],old['quoted_price'],old['quoted_version'])!=(item,price,version):raise ValueError('REQUEST_CONFLICT')
    return old['status']
   product=db.execute(q('SELECT accessory_id,price,version,purchasable,kind'),(item,)).fetchone()
   if not product or product['kind']!='accessory':raise ValueError('INVALID_PRODUCT')
   owned=db.execute(q('SELECT accessory_id FROM inventory WHERE player_id=? AND'),(player,product['accessory_id'])).fetchone();paid=0;ledger=None;status='already_owned' if owned else 'purchased'
   if not owned:
    if not product['purchasable']:raise ValueError('PRODUCT_UNAVAILABLE')
    if (price,version)!=(product['price'],product['version']):raise ValueError('PRICE_CHANGED')
    if balance<price:raise ValueError('INSUFFICIENT_FUNDS')
    paid=price;balance-=price;ledger=str(uuid.uuid4());key='shop:'+player+':'+request
    db.execute(q('INSERT INTO wallet_ledger'),(ledger,player,-price,balance,key));db.execute(q('UPDATE wallets'),(balance,player))
    if fail:raise ValueError('INJECTED')
    db.execute(q('INSERT INTO inventory'),(player,product['accessory_id'],key))
   db.execute(q('INSERT INTO purchase_requests'),(player,request,item,price,version,status,paid,ledger));return status
 key=str(uuid.uuid4())
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(lambda _:buy('a',key),range(32)))
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:assert set(pool.map(lambda _:buy('a',str(uuid.uuid4())),range(32)))=={'already_owned'}
 with conn() as db:assert db.execute('SELECT balance FROM wallets WHERE player_id=\'a\'').fetchone()[0]==18000;assert db.execute('SELECT count(*) FROM wallet_ledger WHERE player_id=\'a\'').fetchone()[0]==1
 for args,code in [(('poor','low'),'INSUFFICIENT_FUNDS'),(('b','stale','pofuk_baret',1999),'PRICE_CHANGED'),(('b','missing','no_item'),'INVALID_PRODUCT'),(('b','ability','ability_common_stun',0),'INVALID_PRODUCT'),(('a',key,'cengel_kafa_bandi'),'REQUEST_CONFLICT')]:
  try:buy(*args)
  except ValueError as e:assert str(e)==code
  else:raise AssertionError(code)
 try:buy('b','rollback',fail=True)
 except ValueError:pass
 with conn() as db:assert db.execute("SELECT balance FROM wallets WHERE player_id='b'").fetchone()[0]==20000;assert db.execute("SELECT count(*) FROM purchase_requests WHERE request_id='rollback'").fetchone()[0]==0
 def equip(player,character,ids,ability='common_stun',revision=0):
  if ability!='common_stun' or len(set(ids))!=len(ids):raise ValueError('INVALID_EQUIPMENT')
  with conn() as db:
   db.execute('BEGIN IMMEDIATE')
   if db.execute(q('SELECT revision FROM player_profiles'),(player,)).fetchone()[0]!=revision:raise ValueError('PROFILE_CHANGED')
   slots={}
   for item in ids:
    row=db.execute(q('SELECT s.slot,s.character_id'),(item,player)).fetchone()
    if row is None:raise ValueError('NOT_OWNED')
    if row['character_id']!=character or row['slot'] in slots:raise ValueError('INVALID_EQUIPMENT')
    slots[row['slot']]=item
   db.execute(q('DELETE FROM equipped_accessories'),(player,))
   for slot,item in slots.items():db.execute(q('INSERT INTO equipped_accessories'),(player,slot,item))
   db.execute(q('INSERT INTO profile_abilities'),(player,ability));db.execute(q('UPDATE player_profiles'),(character,player))
 equip('a','pofuk',['pofuk_baret'])
 for args,code in [(('a','cengel',['pofuk_baret'],'common_stun',1),'INVALID_EQUIPMENT'),(('b','pofuk',['pofuk_baret']),'NOT_OWNED'),(('a','pofuk',[],'fake',1),'INVALID_EQUIPMENT'),(('a','pofuk',[]),'PROFILE_CHANGED')]:
  try:equip(*args)
  except ValueError as e:assert str(e)==code
  else:raise AssertionError(code)
 with conn() as db:assert db.execute("SELECT accessory_id FROM equipped_accessories WHERE player_id='a'").fetchone()[0]=='pofuk_baret'
for token in ['FOR UPDATE','FOR SHARE','c.commit()','c.rollback()','REQUEST_CONFLICT','PRICE_CHANGED','INSUFFICIENT_FUNDS','NOT_OWNED','PROFILE_CHANGED']:assert token in s
client=(A/'Runtime/ShopClient.cs').read_text();assert client.index('SavePending(request)')<client.index('api.PostAuthenticatedAsync<ShopBought>')
for token in ['shop-request-journal.sqlite','expectedPrice=product.price','SavePending(null)']:assert token in client
ui=(A/'Runtime/CharacterCustomizationScreen.cs').read_text();assert 'Dene' in ui and 'Satın al' in ui and 'kuşan' in ui and 'shop.Equip' in ui and 'epoch!=generation' in ui
print('PASS SQLite-only shop experiment: 26 PDF accessory prices/slots, 32 duplicate + 32 distinct-key parallel attempts charged once; insufficient funds, stale quote, unknown/ability product, conflicting key, rollback, ownership/wrong-character/ability/stale-profile checks and reopen persistence')
print('NOT RUN PostgreSQL/JDBC row locks and ShopStoreTest, full Spring API, Unity compile/UI or real mobile purchase/retry acceptance')
