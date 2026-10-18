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

`data-tur` üç değer alır: `tahmin` (Tahmin et adımı), `hatirla` (Hatırla adımı) ve `yoklama` (ders dışı öz yoklama, örneğin "Hazır mısın?" sayfası). Cevaplar not etkisi olmayan öz yoklamadır; yalnızca kişinin kendi tarayıcısında tutulur. Tarayıcı depolaması kapalıysa soru yine çalışır, yalnızca cevabı hatırlamaz.

### Örnek: tahmin sorusu

<div class="egitim-soru" data-soru-id="katalog-tahmin" data-tur="tahmin" data-dogru="2" markdown>
Teslimat robotunun beş node'undan `kamera` çökerse öteki dört node ne yapar?

1. Hepsi hemen durur; tek bir node çökünce ROS bütün sistemi kapatır.
2. Kendi süreçlerinde çalışmaya devam eder; kameradan veri bekleyenlere veri gelmez.
3. Kamera kendiliğinden yeniden başlar; öteki node'lar hiçbir şey fark etmez.

Node'lar ayrı süreçlerde çalıştığı için birinin çökmesi ötekileri kapatmaz. Ama kameranın yayınladığı veriyi dinleyen node'lar artık yeni mesaj almaz. Yeniden başlatma kendiliğinden olmaz; bunu launch dosyasında ayrıca istemek gerekir (Seviye 3).
</div>

### Örnek: hatırlama sorusu (soru bankasından)

Hatırla soruları sonraki derslerin açılışında yeniden sorulduğu için sayfaya yazılmaz, `sorular/` klasöründe kendi dosyasında durur. Dosya, kimliği ve doğru cevabıyla birlikte soru div'inin tamamını taşır. Sayfaya derleme anında tek satırla eklenir; tarayıcıda ağ isteği olmaz. Dosya yoksa `mkdocs build --strict` düşer.

```text
;--8<-- "katalog-hatirla.md"
```

--8<-- "katalog-hatirla.md"

## Tekrar sorusu

Her ders, kendisinden iki önceki dersin hatırla sorularından ikisiyle açılır (0.3, 0.1'den; 1.1, 0.2'den). Aynı soru dosyası `egitim-tekrar` kabının içine eklenir. Kabın içindeki soru, kayıtlı cevapla dolu gelmez ve cevabı kaydetmez; asıl dersteki kayıt değişmez. Aşağıda, yukarıdaki sorunun tekrar hâli var: yukarıda cevap verip sayfayı yenilesen bile bu kutu boş gelir.

```html
<div class="egitim-tekrar" markdown>
;--8<-- "katalog-hatirla.md"
</div>
```

<div class="egitim-tekrar" markdown>
--8<-- "katalog-hatirla.md"
</div>
