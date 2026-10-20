# Lobby V1

Endpoint: /ws/v1/lobby; Authorization: Bearer <P22 token>. Komut şeması lobby-v1.schema.json. Sunucu mesajı `{protocolVersion:1,type,error,room}`. type: connected/pong/room/error/closed/left. room yalnız room olayında vardır; diğerlerinde null.

Snapshot: code,hostId,mapId,phase (LOBBY/STARTED),capacity,revision,expiresAtMs (Unix ms),players[]. Player: playerId,nickname,characterId,team,consent. Token/kayıt anahtarı snapshot içinde yoktur. Başarısız join veya yetkisiz komutta room=null.

Hatalar: ROOM_NOT_FOUND, ROOM_FULL, MATCH_STARTED, INVALID_CODE, INVALID_CAPACITY, ALREADY_IN_ROOM, NOT_IN_ROOM, HOST_ONLY, NOT_MEMBER, INVALID_MAP, INVALID_TEAM, INVALID_TEAMS, ROOM_NOT_FULL, CONSENT_REQUIRED, RATE_LIMIT, INVALID_COMMAND, SERVER_BUSY, CODE_EXHAUSTED. Kapanış: HOST_LEFT, ROOM_EXPIRED, PLAYER_LEFT_AFTER_START. Kimlik/sıra bağlantı hataları socket kapanışıyla da bildirilebilir. ALREADY_CONNECTED aynı hesabın ikinci socket'ini engeller.

## P24

Event ayrıca match alanı taşır: protocolVersion,matchId,worldHash,mapId,tick,phase (COUNTDOWN/ACTIVE/FINISHED),remainingMs,winner,actors,rejectedInputs,droppedTicks,simulationMs,tickRate,snapshotEvery. Actor: playerId,characterId,team,acknowledged,body. Body: x,y,vx,vy,buffer,coyote,grounded,crouched,jumpLocked,alive. state olayında room null olabilir. input komutu inputSequence/clientTick/horizontal/jump/crouch/matchId taşır; konum ve hız alanı yoktur. INVALID_INPUT kendi maç snapshot'ını geri verebilir, başka odayı vermez.

## P25 extension
Input adds vertical [-1,1], push, gripPressed, gripReleased, ultimate. No client target/body/damage fields. World version=2/hash must match. Snapshot adds full surfaces, hazards, events and actor interaction state. Event ring max64, monotonic IDs scoped to match; duplicates are visual-only and ignored. Server outgoing buffer128KiB, Unity bounded receive64KiB; incoming commands stay2KiB. See Docs/P25_CEVRIMICI_ETKILESIM.md.

## P26 connection lifecycle
Authenticated reconnect automatically resumes a matching active-room lease and sends a full room+match event. Actor adds connected and reconnectRemaining (seconds). No client resume player ID/token is trusted in command data. Grace expires to elimination; never respawn. Active same-account connection takeover sends replaced/SESSION_REPLACED to previous transport; old commands/close cannot affect new transport. Pong adds replySequence matching the ping command sequence. Server restart loses memory matches and sends ordinary connected; client reports missing previous match. World version3/hash gates clients. Policy and exact limits: Docs/P26_AG_DAYANIKLILIGI.md.


P29: Snapshot.result FINISHED öncesi null; bitişte winner, team1Remaining, team2Remaining, team1Damage, team2Damage, reason içerir. Nedenler: simultaneous_elimination, team_eliminated, equal_damage, damage_tiebreak, equal_survivors_provisional, more_survivors. İstemci sunucuyla birlikte güncellenmelidir. leave odası olmayan bağlı oturum için de left döndürür. Sonuç görünümü ödül üretmez.
