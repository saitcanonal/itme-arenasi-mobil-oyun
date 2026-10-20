#!/bin/bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/../Server"
command -v docker >/dev/null || { echo "Docker Desktop kurulu olmalı ve açık olmalı."; exit 1; }
if [ ! -f .env ]; then
 umask 077
 python3 - <<'PY'
from pathlib import Path
import secrets,base64
p=Path('.env')
with p.open('x') as f:
 f.write('DB_PASSWORD='+secrets.token_hex(24)+'\nAUTH_SECRET='+base64.b64encode(secrets.token_bytes(32)).decode()+'\nADMOB_REWARDED_UNIT=\n')
PY
fi
docker compose up --build -d
echo 'Yerel sunucu: http://localhost:8080 — Unity: Itme Arena > Oyna / Bu Mac üzerindeki gerçek sunucu'
echo 'Farklı telefonlardan erişim için HTTPS sunucu kurulumu gerekir. Bu komut internete yayınlamaz.'
