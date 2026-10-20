## 2026-10-18 — Önizleme 28: Karakter görüntü kalitesi
Boğa atlası ve 31 aksesuar importunda mipmap + trilinear açıldı; sıkıştırmasız ve NPOT ölçeklemesiz ayarlar korundu. Portreler ve atölye artık gerçek ekran piksel boyutuna göre 1.5× supersampling ile çiziliyor. Canvas ölçeği ve ebeveyn ölçeği köşe koordinatlarından hesaba katılır. En uzun kenar 1536 piksel ve donanım sınırıyla kısıtlıdır. Mipmapped RenderTexture trilinear süzülür; alpha kenarlarında supersampling kullanılır, MSAA=1. Boyut değişimi 0.3 saniyede kontrol edilir ve küçük dalgalanmalarda yeniden tahsis yapılmaz. Gizli portre dokuları serbest bırakılır. Önizleme 27 atlas kesim düzeltmesi korunur.
Kontrol: 32 import ayarı, atlas şeffaflığı/parça sınırları, 31 ürün bağlantısı ve kaynak ayraç kontrolleri geçti. Unity/Metal/Android görsel doğrulaması ve FPS/bellek ölçümü YAPILMADI.

## 2026-10-18 — Önizleme 27: Boğa atlas kesim düzeltmesi
Ekran görüntüsündeki yarım kafa ve kayıp gövde/uzuvlar araştırıldı. Önizleme 26, 1536×1024 kaynak atlas koordinatlarını Unity'nin import edilmiş doku ölçüsüne uyarlamadan kullanıyordu. TextureImporter NPOT boyutlandırması bu ölçüleri değiştirebildiği için kesim yanlış bölgelere kayıyordu. BogaSprites.cs artık gerçek texture.width/height üzerinden normalize koordinat hesaplar. atlas.png.meta içinde npotScale: 0 ayarlandı. Görseller, kıyafetler, hesaplar ve ekonomi değiştirilmedi.
Kontrol: Altı parçanın kaynak sınırları ve şeffaflığı geçti; 1536×1024, 2048×1024, 1024×1024, 768×512 ve 512×256 için UV/sınır aritmetiği doğrulandı. Unity/gerçek cihaz testi bu ortamda yapılmadı.

## 2026-10-18 — Önizleme 26: Boğa
Gönderilen boksör tek ana karakter olarak parçalı rig'e bağlandı. Cinsiyet/karakter geçişleri kaldırıldı; 31 kozmetik ürün korundu. Sunucuda V12 hesap uyarlaması eklendi. Kaynak/atlas kontrolleri ve ShopStore Java derlemesi geçti; Unity/cihaz, canlı sunucu ve DB migration testleri yapılmadı. Ayrıntılar: Docs/ONIZLEME_26_BOGA.md.

## 2026-10-18 — Önizleme 25
İlk açılış isim ekranı yenilendi: sprite panel/kaide, Lilita One tabanlı Türkçe font, canlı plaka, giriş/basış animasyonları ve mobil klavye düzeni. Kayıt/geçiş iş mantığı korundu. Ayrıntılar: Docs/ONIZLEME_25_ILK_ACILIS.md. Kaynak ve varlık kontrolleri geçti; Unity/cihaz testleri yapılmadı.

# V1.2 Önizleme 24 — Ortak insan karakteri ve beş kozmetik slotu

## Uygulanan
- İlk kayıt öncesinde erkek/kadın temel karakter seçimi. İki temel karakter ücretsiz; spor kıyafetli kaslı çizgi film iskeleti, ayrı kafa/gövde/kol/el/bacak/ayak parçaları.
- Eski beş yaratığın seçimi kullanıcı gardırobundan kaldırıldı. Eski kimlikler kayıt geçmişini bozmamak için uyumluluk amacıyla tutuldu; görsel sistem artık insan iskeletini kullanıyor. Eski Fırtına kadın, diğer eski profiller erkek tabana geçirilir; gardıroptan değiştirilebilir.
- Gardıropta ayakkabı, eldiven, yüz/maske, şapka, gövde sekmeleri; anında önizleme, ayrı satın alma/kuşanma. Cinsiyet değiştirirken ortak aksesuarlar korunur. Yetenek düğmesi üç ortak yeteneği açar; cinsiyet güç avantajı sağlamaz.
- 26 P10 aksesuarının kimlikleri ve sahipliği korunarak beş slota taşındı. Çakışan eski slotlardan biri takılı kalır, diğerleri envanterde korunur. Eski bağlama tanımları ArtSource/V1224/legacy_bindings.json içinde arşivlidir.
- İlk beş yeni deneme ürünü: Alev Adımı, Hurda Yumruk, Piksel Bakış, Çöp Kutusu Tacı, Arena Şampiyonu. Koleksiyonda toplam 31 kayıt. 25–30 tamamen yeni ürün veya 50 ürün üretildiği iddia edilmez; ilk beşin görsel değerlendirmesinden sonra genişletilir.
- cosmetics_v2.json: id, slot, sprite, rarity, price, currency, sortingOrder, sabit 512 tuval/merkez anchor, pairMode ve leftSprite. Ayrı sol PNG veya simetrik ayna desteklenir. Altın kullanılır; elmas geri eklenmedi.
- ArtSource/V1224 içinde düzenlenebilir SVG kaynakları ve her slot için PNG şablon. Tools/build_cosmetics_v2.py ile bir kayıt yeni Unity katalog/binding ve sunucu SQL taslağına dönüştürülür.
- Temel karakter atölyesi artık ücretsiz. Ek renk/vücut/yüz seçenekleri ve ürünler altınla açılır. Eski atölye/karakter satın alma kayıtları silinmez; otomatik geçmiş ücret iadesi yapılmaz.

## Kontroller ve sınırlamalar
31 ürünün benzersiz kimliği, beş slot, 512×512 şeffaf PNG, sprite yolları, çift parçalar/katmanlar ve önceki RewardResponse düzeltmesi kontrol edildi. ShopStore ve PowerCatalog Java ile derlendi. StudioService/Controller framework sınır stublarıyla derlendi; Spring veya PostgreSQL entegrasyon testi değildir. C# için yalnızca temel statik kontroller yapıldı; Unity/Android çalıştırma ve gerçek görsel/animasyon kabul testi bu ortamda yapılamadı. Unity menüsüne Itme Arenasi > Validate Human Cosmetics kontrolü eklendi; bu kontrol burada çalıştırılmadı. İnsan varlıkları mevcut hareket motoruna bağlandı; cihazda yürüme, itme, tutunma ve yere düşme sırasında hizalama incelenmeli.

## Sunucu ve kayıt geçişi
Server ile Unity birlikte güncellenmeli. V11__human_cosmetics.sql test veritabanına uygulanmalı; canlı dağıtım yapılmadı. Migration mevcut envanteri korur, karakter tabanını ve takılı slotları dönüştürür. Üretim veritabanında yedek ve migration denemesi olmadan eski ZIP'e geri dönülmemeli. Eski .sql dosyaları değiştirilmedi. Yerel geliştirme satın alımları ayrı yerel cüzdanı kullanır; gerçek sunucu parası oluşturmaz.

## İçerik rehberleri
Docs/YENI_URUN_5_ADIM.md: tam beş satırlık ürün ekleme rehberi.
Docs/URUN_GORSEL_PROMPTLARI.md: beş slot için şablonlu üretim promptları.
Docs/COSMETICS_PRODUCTS_DRAFT.sql: yeni ürün ekleme aracı çıktısı, otomatik canlı uygulama yapmaz.

---

# V1.2 Önizleme 23 — CS1061 derleme hatası düzeltmesi

RewardResponse sınıfına eksik public int recoveryAmount ve public bool recovered alanları eklendi. Önizleme 22'de bu alanlar okunuyor ancak tanımlanmıyordu; ekran görüntüsündeki beş CS1061 hatasının nedeni buydu. Yalnızca bu veri sınıfı düzeltildi; %50 iade ve diğer özellikler korundu.

Kontrol: RewardController.Result sunucu alanları ile C# RewardResponse alanlarının ad ve tür eşleşmesi otomatik doğrulandı (8 alan). RewardStatusView içindeki value alan erişimlerinin tümü sınıf tanımlarıyla karşılaştırıldı. Kaynak farkı tek dosya ile sınırlı; ZIP CRC kontrolü geçti. Unity derlemesi bu ortamda yapılamadı. Sarı uyarılar bu düzeltmenin kapsamı dışındadır.

Kurulum: ZIP'i yeni klasöre çıkar, Unity Hub ile içindeki UnityProject klasörünü aç. Mevcut projede yalnızca düzeltmeyi uygulamak için Unity kapalıyken Assets/ItmeArena/Runtime/RewardStatusView.cs dosyasını bu sürümdeki dosyayla değiştir. Unity'nin derlemesini bekle; hata kalmazsa Safe Mode'dan çık.

---

# V1.2 Önizleme 22 — Video ile %50 yenilgi iadesi

Normal maçta gerçekleşmiş altın kesintisinin veya kaybedilen Challenge giriş bedelinin yarısı iade edilir. 150 → 75, 500 → 250. Tek sayılar aşağı yuvarlanır; sıfır iade için reklam açılmaz. Galibiyet, beraberlik, iade edilmiş/bitmemiş Challenge ve başkasına ait maç uygun değildir. Tutar sunucudaki sonuç ve cüzdan kayıtlarından hesaplanır; istemciden tutar alınmaz.

Maç sonundaki buton VİDEO İZLE · +N ALTIN İADE yazar. İade yalnızca doğrulanmış AdMob SSV tamamlanmasıyla verilir. Yarım bırakılan reklam para vermez. Cüzdan satır kilidi, maç başına granted kontrolü ve işlem kimliği korumaları sürer. Önceden oluşturulan bekleyen telafi reklamının tutarı da grant sırasında yeni kuralla hesaplanır. Daha önce verilmiş iadeler geri alınmaz.

Geliştirme profilindeki yerel kayıp için tutar pasif butonda gösterilir; gerçek hesap/maç/reklam bağlantısı olmadan altın uydurulmaz. Normal 200 altın bonus reklamı değişmedi. Sunucuya bağlı sonuç ekranı telafi uygunluğunu onay gelene kadar yeniler.

Dağıtım: Unity projesiyle birlikte Server sürümü de güncellenmeli. AdMob uygulama/birim kimliği, SDK ve doğrulanmış SSV bağlantısı çalışır olmalı. Bu teslim canlı sunucuya dağıtım yapmadı.

Yapılan test: gerçek RecoveryPolicy.java Java ile derlendi; 0,1,2,149,150,200,300,500 ve negatif girdi için 9 kontrol geçti. Temel kaynak parantez kontrolü, ZIP CRC ve manifest yenilendi. DB entegrasyon testleri 75 altın normal iade, 250 Challenge iadesi, izleme öncesi ödül yok, tekrar callback ve beraberlik için güncellendi; Maven/Docker olmadığı için çalıştırılmadı. Unity/Android, gerçek AdMob ve PostgreSQL entegrasyon testleri yapılmadı.

---

# V1.2 Önizleme 21 — Arena sonuç ekranı

Düz sonuç tablosu; karartılmış çizgi arena arka planı, kupalı sonuç şeridi, turuncu/turkuaz takım kartları, büyük skor rakamları ve ayrı altın alanıyla yenilendi. Başlıklarda kalın ArenaDisplay yazısı, renkli kontur ve ortalı yerleşim kullanılıyor. Sonuç başlığı kazanan takımı bildirir; oyuncunun takımını tahmin ederek kişisel zafer/mağlubiyet yazmaz. Beraberlik başlığı ayrı.

Kupa ve altın simgesi hafif hareketli; yeniden oyna ve ana menü simgeli, renk değişimli ve basma animasyonlu. Mevcut hakem duyurusu korunur. Sunucu ödül doğrulaması, geliştirme altını açıklaması, koşullu reklamla telafi ve çift gezinme kilidi korunur. Ekonomi veya maç sonucu kuralları değişmez.

Doğrulama: değişiklik kapsamı yalnızca MatchResultScreen ve ortak kart yardımcısının küçük boyut sınır düzeltmesi; temel kaynak parantez dengesi, başlıca yerleşim sınırları, ödül/geri dönüş korumalarının varlığı, ZIP CRC ve SHA256 manifesti kontrol edildi. Unity derlemesi/gerçek görüntü testi yapılmadı.

Cihazda doğrulanacak: iki takımın galibiyeti, beraberlik, uzun sonuç/ödül hatası metni, sunucu bekleyen/onaylanan ödül, telafi reklamı uygunluğu, çift tıklama, yeniden oyna/ana menü, güvenli ekran alanı. Gerçek cihaz testleri tamamlandı sayılmamıştır.

---

# V1.2 Önizleme 20 — Maç türü butonları

NASIL OYNAMAK İSTERSİN penceresi simgeli ve açıklamalı kartlarla yenilendi. Tek oyunculu: turuncu savaşçı miğferi; çok oyunculu: turkuaz takım arması; Challenge: mor kupa; geri: ok simgesi. Daha büyük kalın ArenaDisplay başlıkları, altın renkli konturlu yazılar, dokunma/üzerine gelme/seçim renkleri, basma ölçek animasyonu ve hafif simge hareketi eklendi. Efekt tercihi simge hareketine uygulanır.

Kapsam: MainMenuScreen içindeki maç türü penceresi, yeni ModeChoiceStyle yardımcı dosyası ve bu yazıların genel tipografi tarafından ezilmemesi için sınırlı işaretleyici kontrolü. Diğer ekranlar, ağ erişimi koşulu, maç giriş efekti, fiyatlar ve buton işlevleri korunur.

Yapılan doğrulama: değişen dosya kapsamı, temel C# parantez dengesi, dört kartın panel sınırları, simge/font dosyalarının varlığı, mevcut ağ/tek oyunculu/Challenge yönlendirmelerinin varlığı ve ZIP CRC. Bu kontroller derleme veya ekran testi değildir.

Yapılmayan: Unity derlemesi, Android gerçek cihaz dokunma ve görsel testi. Cihazda dört butonun açılışı, çevrim dışı çok oyunculu pasifliği, Türkçe karakterlerin görünümü, küçük ekran ve efekt kapalı/açık davranışı kontrol edilmeli.

---

# V1.2 Önizleme 19 — Merkezden darbe ile maç girişi

Eski kayan iki renkli alan ve sürekli konfeti kaldırıldı. Yaklaşık 1,65 saniyelik geçişte 0,18. saniyede tek darbe sesi, merkezden yayılan yıldız patlama ve kısa çizgiler; büyüyüp oturan MAÇ BAŞLIYOR başlığı bulunuyor. Takım karakterleri korunuyor; darbe anında kısa geri tepme yapıyor. Döngüsel flaş ve ekran sarsıntısı yok.

Geçiş sırasında müzik duraklıyor, efekt sesi kullanıcının ses ayarına uyuyor. Geçiş bitince veya nesne kapanınca müzik tutma sayacı bırakılıyor; müzik tercihi değiştirilmeden normal ses yönetimi sürüyor. Duraklatma/odak kaybı kuralları korunuyor. Ses özgün olarak sentezlenen 0,65 saniyelik mono PCM WAV dosyasıdır.

Kontroller: değişen kapsam yalnızca VersusIntro.cs, ArenaAudio.cs ve yeni ses/meta; kaynakların temel parantez dengesi, tek darbe tetikleyicisi, OnDisable temizliği ve WAV örnek sayısı doğrulandı. ZIP CRC ve SHA256 manifesti yenilendi. Bu kontroller Unity derlemesi veya gerçek ses/görüntü testi değildir.

Unity ve Android çalıştırma testleri yapılmadı. Cihazda: ilk maç/tekrar maç, müzik kapalı/açık, efekt sesi kapalı/açık, geçişte uygulamayı arka plana alma, iki farklı ekran oranı ve maça tek geçiş doğrulanmalı.

---

# V1.2 Önizleme 18 — Takım hazırlık ekranı

Seçili harita üstte ortalandı ve 568×248 çerçeveye taşındı. Altında turuncu/turkuaz takım kartları, daha büyük hareketli karakter portreleri, okunaklı isimler ve hareketli VS görseli yer alıyor. Başlatma, harita değiştirme ve takım değiştirme düğmeleri ayrı alanlarda; ortalanmış renkli yazılar, yuvarlak çerçeveler ve dokunma animasyonu kullanılıyor.

Yalnızca SelectionScreen.cs değişti. Harita seçici, fiyatlar, ana menü, canlı oda arayüzü, sunucu, maç ve ekonomi kuralları korunuyor. Bu ekran yerel maç hazırlık ekranıdır; canlı çok oyunculu oda ekranı değişmedi.

Doğrulama: kaynak kapsamı karşılaştırıldı; temel parantez dengesi, mevcut başlatma/harita/geri dönüş korumalarının varlığı ve ana yerleşim sınırları denetlendi. Paket manifesti yeniden oluşturuldu ve ZIP CRC kontrolü yapıldı.

Unity derlemesi, gerçek ekran görüntüsü ve Android dokunma testi bu ortamda çalıştırılamadı. Bunlar başarılı olarak işaretlenmedi. Unity'de harita seç → takım ekranı → takım değiştir → haritayı değiştir → maç başlat → tekrar oyna akışı ve uzun oyuncu adları cihazda kontrol edilmeli.

---

## V1.2 Önizleme 17 — 18 Ekim 2026
Harita seçimi tek büyük ortalanmış önizlemeye çevrildi. Büyük ok/X, renkli hareketli başlık, altın rozeti, tek seç/kilidi aç düğmesi. Alt küçük kartlar ve Hediye/Test altını satırı kaldırıldı. Harita önizlemeleri detaylandırıldı. Fiyatlar ve oynanış korundu. Kaynak/görsel kontrolleri geçti; Unity/Android testi yapılmadı. Ayrıntı: Docs/V1217_HARITA_SECIMI.md.

## V1.2 Önizleme 16 — 17 Ekim 2026
1v1 yerel, 1v1/2v2 çevrim içi; 3v3/4v4/dengesiz PvP kapalı. Lig/Takım Yakında. Elmas ve günlük kart kapalı. 15 ayrı karakter ultisi, ikon/efekt, kuşanma ve Java sunucu kuralı eklendi; ulti satışı yok. Altın paketleri korundu. 51 izole Java doğrulaması geçti; Unity/Android/gerçek sunucu kabul testi yapılmadı. Ayrıntı: Docs/V1216_KAPSAM_VE_ULTILER.md.

# 1.2-preview.15 — Dükkân ve maç seçenekleri

200 altın/10 elmas reklam akışı, fiyat taslaklı altın dükkânı ve yeni maç seçimleri. Gerçek para satın alma henüz bağlı değil. Ayrıntılar: Docs/V1215_DUKKAN_MAC_SECIMI.md. Unity/cihaz ve sunucu çalıştırma testleri yapılmadı.

# 1.2-preview.14 — Gardırop ve avatar

Simgeli büyük kategoriler, karakter amblemi, ayarlar dişlisi ve kare profil avatarı. Ayrıntılar: Docs/V1214_GARDIROP_AVATAR.md. Kaynak kontrolleri geçti; Unity/cihaz testi yapılmadı.

# 1.2-preview.13 — Giriş ve kişisel karşılama

Karakter seçimsiz grafiti giriş, büyük giriş düğmesi, isimli karşılama ve yeni ana menü yerleşimi. Ayrıntılar: Docs/V1213_GIRIS_KARSILAMA.md. Kaynak kontrolleri geçti; Unity/cihaz testi yapılmadı.

# 1.2-preview.12 — Lig rozetleri ve grafiti menü

Yeni lig rozetleri, Maç Oyna/VS, takım amblemi, hareketli logo ve yüksek çözünürlüklü karakterler. Ayrıntılar: Docs/V1212_MENU_LIG_GORSELLERI.md. Kaynak kontrolleri geçti; Unity/cihaz testi yapılmadı.

# 1.2-preview.11 — Görsel tuşlar ve maç sonu hakemi

Maç kontrolleri resimli simgelere dönüştürüldü. Maç sonunda 2,8 saniyelik dövüş hakemi duyurusu eklendi. Ayrıntılar: Docs/V1211_GORSEL_TUSLAR_HAKEM.md. Kaynak kontrolleri geçti; Unity/cihaz testi yapılmadı.

# 1.2-preview.10 — Mola ayarları

Tutun sağ alta taşındı. Ana menü ve pause ortak ayar panelini kullanır. Ayrıntılar: Docs/V1210_MOLA_AYARLARI.md. Kaynak kontrolleri geçti; Unity/cihaz testi yapılmadı.

# V1.2 Önizleme 9 — Maç tuşları ve bildirimler

Tutun sağ üste taşındı, sol oklar büyütüldü; maç tuşlarının şekli ve yazıları yenilendi. İşaretli sabit metinler animasyonlu geçici bildirim oldu. Ayrıntılar: **Docs/V129_TUS_BILDIRIM.md**.

---

# V1.2 Önizleme 8 — Maç ekranı

Küçük ve ortalı tuşlar, yeni kontrol yerleşimi, ortada süre ve sağ üstte mola simgesi. Ayrıntı ve test sınırları: **Docs/V128_MAC_EKRANI.md**.

---

# V1.2 Önizleme 7 — Çizgi film arena

Yeni çizgi film ringi menüye bağlandı; sahne hareketi, karakter gölgesi, selamlama, renkli yazılar ve buton dokunma sesi eklendi. Ayrıntılar ve test sınırları: **Docs/V127_CIZGI_ARENA.md**.

---

# V1.2 Önizleme 6 — Gardırop ve maç seçimi

Aksesuarlar kategorilere ve ikili ürün sayfalarına ayrıldı. Butonlar küçültüldü; oyuncu sayısı kartlarına başlık ve hareket eklendi. Ayrıntı ve test sınırları: **Docs/V126_GARDIROP.md**.

---

# V1.2 Önizleme 5 — Yeni butonlar ve bölümlü arayüz

Ortak buton biçimi, font, ikonlar ve animasyonlar yenilendi. Ayarlar, profil, maç seçimi ve lig alanları yeniden düzenlendi. Ayrıntı ve test sınırları: **Docs/V125_ARAYUZ.md**. Unity görsel kabulü bekleniyor.

---

# V1.2 Önizleme 4 — Harita penceresi düzeltmesi

Küçük kalan modalın iç içe Canvas ölçekleme hatası giderildi; önizleme büyütüldü, kapanışta tıklama engeli anında kaldırılır. Unity cihaz kabulü bekliyor. Ayrıntı: **Docs/V124_HARITA_DUZELTMESI.md**.

---

# V1.2 Önizleme 3 — Haritalar

Kırık Fabrika ücretsiz; diğer iki harita 1.500’er altın. Büyük harita seçimi, seçim sonrası oyuncu listesi ve sunucu sahiplik denetimi. Ayrıntılar ve test sınırları: **Docs/V123_HARITALAR.md**.

---

# V1.2 Önizleme 2 — Boks ringli menü

Yeni arka plan, küçük resimli alt menü, tam boy karakter kadrajı ve daha uzun bacak/gövde düzeni. Detay ve test sınırları: **Docs/V122_BOKS_MENUSU.md**.

---

# V1.2 Önizleme 1 — çalışma devam ediyor

Menü, karakter oranları, eklemli bayılma animasyonu, basılı tutunma, can sistemi, yeni krater arka planı, kontrol düzenleme, karakter satın alma, lig ve günlük kart altyapısı değiştirildi. **Tüm V1.2 talepleri tamamlanmadı.** Uygulananlar, açık işler ve test sınırları: **Docs/V12_DURUM.md**.

---

# V1.1.4 — Giriş düzeltmesi

Unity Editor varsayılanı artık **YEREL DENEME**. Sunucu kurulmadan isim/karakter seçip bot oyununa girilebilir. Gerçek hesap, çok oyunculu ve reklam sunucusu ayrı gereksinimlerdir. Adımlar ve doğrulamalar: **Docs/V114_GIRIS_BAGLANTISI.md**.

---

# V1.1.3 güncel kayıt

Giriş ekranı, büyük hareketli karakter, ışıklar ve kartlar yenilendi. İsim koşulları kaldırıldı; boş isim Oyuncu olur. Eski kayıt adı ile güncel profil adı ayrıldı; girişte aynı hesabın adı düzenlenebilir. Kurulum ve açık doğrulamalar: **Docs/V113_GIRIS_ISIM.md**.

---

# V1.1.2 güncellemesi — 16 Ekim 2026

Bayılınca devrilme/toz ve baş-el-ayak sürükleme eklendi. 402 Java çekirdek kontrolü ve 25 kaynak denetimi geçti; Unity/Android görsel kabulü açık. Kullanım ve teknik sınırlar: **Docs/V112_BAYILMA_SURUKLEME.md**.

---

# V1.1 güncel kayıt — 2026-10-16

V1.1: arayüz/portre/VS, kamera/tutunma, kolay isim, profil/atölye, yeni maç ekonomisi, 3v3 ve Challenge havuzu, isteğe bağlı SSV reklam adaptörü. Kaynak teslimidir; canlı servis veya APK teslimi değildir.

---

## Önceki aşamaların tarihsel kaydı

# P32 değişiklikleri

SQLite v4 ses/titreşim düzeltmesi; 104 satırlık kaynak/kanıt/kalan denetimi; güncel sunucu README; ayrı oyuncu/geliştirici kurulumları; final engeller; temiz paket doğrulayıcısı; sürüm 0.32.0 ve P32 çıktı adları. Uygulama kimliği, sanat varlıkları, referanslar, sunucu simülasyonu ve PostgreSQL V1–V5 korunur.
