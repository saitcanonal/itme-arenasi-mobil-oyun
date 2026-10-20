## 2026-10-18 — Önizleme 27: Boğa atlas kesim düzeltmesi
Ekran görüntüsündeki yarım kafa ve kayıp gövde/uzuvlar araştırıldı. Önizleme 26, 1536×1024 kaynak atlas koordinatlarını Unity'nin import edilmiş doku ölçüsüne uyarlamadan kullanıyordu. TextureImporter NPOT boyutlandırması bu ölçüleri değiştirebildiği için kesim yanlış bölgelere kayıyordu. BogaSprites.cs artık gerçek texture.width/height üzerinden normalize koordinat hesaplar. atlas.png.meta içinde npotScale: 0 ayarlandı. Görseller, kıyafetler, hesaplar ve ekonomi değiştirilmedi.
Kontrol: Altı parçanın kaynak sınırları ve şeffaflığı geçti; 1536×1024, 2048×1024, 1024×1024, 768×512 ve 512×256 için UV/sınır aritmetiği doğrulandı. Unity/gerçek cihaz testi bu ortamda yapılmadı.

# V1.2 Önizleme 4 — Harita penceresi düzeltmesi

Küçük kalan modalın iç içe Canvas ölçekleme hatası giderildi; önizleme büyütüldü, kapanışta tıklama engeli anında kaldırılır. Unity cihaz kabulü bekliyor. Ayrıntı: **Docs/V124_HARITA_DUZELTMESI.md**.

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

Düzeltildi: inputlegacy manifest, altı oyuncu sonuç sınırı, kamera takibinin sıfırlanması, ulti çubuk genişliği ve profil iptal kaynağı yaşam döngüsü. Açık: Unity/tam sunucu/cihaz kabulü, AdMob kurulumu, halka açık sunucu; Docs/V11_TESLIM.md.

---

## Önceki aşamaların tarihsel kaydı

# Hatalar — P32

Kapatıldı: P30 ses düzeyi/titreşim anahtarları yerel depoda tanınmıyordu; SQLite v4 geçişi ve varsayılan/aralık normalizasyonu eklendi. Eski profil ve ayar koruma testi çalıştırıldı. Eski sunucu README/kapsam açıklamaları güncellendi.

Açık: gerçek derleme/cihaz/tam sunucu; görsel geçici dekorlar; hesap silme/politika; ödül çökme kurtarması; üretim isim değişimi ve çevrimdışı aksesuar eşitliği. Tam liste Docs/P32_FINAL_RAPOR.md.
