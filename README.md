# İtme Arenası V1 sunucusu — P32 / 0.32.0

Java 17, Spring Boot 3.5.16, PostgreSQL 16.6 ve Flyway V1–V5. Kaynaklar mevcut; bu ortamda tam Maven/Spring/PostgreSQL entegrasyon testi yapılmadı. Tools/run_online_core_tests.py gerçek Java çekirdeğini sınır stublarıyla derler; tam servis kabulünün yerine geçmez.

## Yerel geliştirme

Docker Desktop çalışırken bu klasörde `.env.example` dosyasını `.env` olarak kopyalayın; DB_PASSWORD'u güçlü bir değerle, AUTH_SECRET'i yerelde `openssl rand -base64 32` çıktısıyla doldurun. .env, anahtarlar ve gerçek parolalar paylaşılmaz. AUTH_SECRET ve PostgreSQL volume'ünü yeniden başlatmada koruyun.

```bash
cp .env.example .env
# .env içindeki iki gizli değeri yerel editörde doldurun.
docker compose up --build -d
curl --fail http://localhost:8080/actuator/health
curl --fail http://localhost:8080/api/v1/catalog
```

Compose, DB 5432 ve API 8080 portlarını yalnız 127.0.0.1'e açar. Telefon için geçerli TLS sertifikalı HTTPS/WSS reverse proxy gerekir; bu pakette canlı sunucu kurulmuş değildir. `docker compose down -v` veriyi siler; kullanmayın. Ayrı temiz proje testinde mevcut portları kullanan başka Compose'u durdurun veya ayrı portlar verin; mevcut volume'ü silmeyin.

JDK17 + Maven + Docker ile:

```bash
mvn -B test
mvn -B package
mvn dependency:tree > dependencies.txt
```

Testcontainers gerçek PostgreSQL açar; Docker yokluğu başarı değildir. Host üzerinde jar çalıştırmak için DB_URL/DB_USER/DB_PASSWORD/AUTH_SECRET ortam değişkenlerini dışarıdan sağlayın (.env Maven tarafından otomatik okunmaz), sonra `java -jar target/arena-server-0.32.0.jar`. Dockerfile imaj paketlemesi test atlar; ayrı `mvn test` kabul için gereklidir. Flyway geçmiş migration'ları değiştirmeyin; V1 şema, V2 katalog, V3 oturum, V4 ödül, V5 mağaza/sahiplik birlikte uygulanır.

## Mevcut servisler

- Açık katalog ve health: GET /api/v1/catalog, GET /actuator/health.
- Gerçek anonim hesap: POST /api/v1/accounts/anonymous; Bearer profil: GET /api/v1/profile.
- Bearer cüzdan ve ödül makbuzu: GET /api/v1/wallet, GET /api/v1/matches/{id}/reward. İstemci ödül yaratamaz.
- Bearer mağaza: GET /api/v1/shop/catalog, GET /api/v1/shop/state, POST /api/v1/shop/purchase, POST /api/v1/shop/equip.
- Bearer WebSocket: /ws/v1/lobby; 2/4 kişi oda, 30 Hz sunucu simülasyonu, 10 Hz snapshot, hareket/itme/tutunma/ulti/harita tehlikeleri, kopma/geri dönme, dondurulmuş sonuç.

Sözleşmeler ../Contracts içinde. Çevrimdışı ödül otomatik para değildir; sunucu doğrulaması olmadan bekler. Mağazada gerçek para/ödeme yok; örnek Güç Taşı fiyatları vardır. Hesap silme API'si, gerçek web silme yolu ve yayınlanmış gizlilik politikası henüz yoktur. Sunucu çökmesinden önce kalıcılaşmamış sonuç kuyruğu kaybı açık engeldir. Aktif oda/maçlar restart sonrasında geri yüklenmez.

## Sınırlar

TLS dağıtımı, gerçek çoklu cihaz, JDBC eşzamanlılık, veri yedeği/geri yükleme, servis restart ve yayın ölçeği kabulü bekler. Geçmiş README Docs/History/P31/Server_README.md içinde arşivlidir; tarihsel “yalnız iki GET açık” açıklaması artık geçerli değildir. Final kurulum ve engeller ../Docs/P32_GELISTIRICI_KURULUM.md ve ../Docs/P32_FINAL_RAPOR.md içinde.
