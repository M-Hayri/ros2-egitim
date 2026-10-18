# Bileşen kataloğu

Bu sayfa ders yazanlar içindir: sitedeki etkileşimli bileşenlerin nasıl gömüldüğünü gösterir ve tarayıcı testleri bu sayfa üzerinde çalışır. Bileşenlerin tamamı tek bir JavaScript dosyasında (`docs/assets/egitim/egitim.js`) ve tek bir stil dosyasında (`docs/assets/egitim/egitim.css`) durur. Harici kütüphane kullanmaz, ağ isteği yapmaz.

## Widget gömmek

Bir widget Markdown sayfasına tek satırla girer:

```html
<div data-egitim-widget="tek-program-node-grafigi"></div>
```

Bilinmeyen bir ad yazılırsa sayfada kırmızı bir hata kutusu çıkar ve konsola hata düşer; tarayıcı testleri bu hatayı yakalar.

### Tek program ve node grafiği (Ders 0.1)

<div data-egitim-widget="tek-program-node-grafigi"></div>

## Soru eklemek

Tahmin ve hatırlama soruları aynı bileşeni kullanır. İlk paragraf soru metnidir, ilk numaralı liste seçeneklerdir, listeden sonraki her şey cevap verildikten sonra görünen açıklamadır. `data-dogru` doğru seçeneğin sırasıdır (1'den başlar). `data-soru-id` site genelinde tek olmalı; cevap tarayıcıda bu kimlikle saklanır.

```html
<div class="egitim-soru" data-soru-id="ornek-tahmin" data-tur="tahmin" data-dogru="2" markdown>
Kamera programı çökerse öteki node'lar ne yapar?

1. Hepsi durur.
2. Kendi süreçlerinde çalışmaya devam eder.
3. Kamera kendiliğinden yeniden başlar.

Açıklama metni buraya.
</div>
```

`data-tur` iki değer alır: `tahmin` (Tahmin et adımı) ve `hatirla` (Hatırla adımı). Cevaplar not etkisi olmayan öz yoklamadır; yalnızca kişinin kendi tarayıcısında tutulur. Tarayıcı depolaması kapalıysa soru yine çalışır, yalnızca cevabı hatırlamaz.

### Örnek: tahmin sorusu

<div class="egitim-soru" data-soru-id="katalog-tahmin" data-tur="tahmin" data-dogru="2" markdown>
Teslimat robotunun beş node'undan `kamera` çökerse öteki dört node ne yapar?

1. Hepsi hemen durur.
2. Kendi süreçlerinde çalışmaya devam eder; kameradan veri bekleyenlere veri gelmez.
3. Kamera kendiliğinden yeniden başlar, kimse fark etmez.

Node'lar ayrı süreçlerde çalıştığı için birinin çökmesi ötekileri kapatmaz. Ama kameranın yayınladığı veriyi dinleyen node'lar artık yeni mesaj almaz. Yeniden başlatma kendiliğinden olmaz; bunu launch dosyasında ayrıca istemek gerekir (Seviye 3).
</div>

### Örnek: hatırlama sorusu

<div class="egitim-soru" data-soru-id="katalog-hatirla" data-tur="hatirla" data-dogru="3" markdown>
Programı küçük node'lara bölmenin en doğrudan kazancı hangisi?

1. Program daha hızlı çalışır.
2. Daha az kod yazılır.
3. Bir parça çökünce ya da değişince ötekiler etkilenmeden kalabilir.
4. Ağ trafiği azalır.
</div>
