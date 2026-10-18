<!--
DERS SAYFASI ŞABLONU
Yeni ders: bu dosyayı docs/seviye-N/ altına "N-M-kisa-ad.md" adıyla kopyala, mkdocs.yml nav'ına ekle.
Kurallar: örnekler nötr olur (araca özgü içerik yok); teori bölümü 800 kelimeyi geçmez;
sayfadaki her komut devcontainer içinde test edilir; resmi doküman yeniden yazılmaz, bağlantı verilir.
Aşağıdaki 13 alanın hepsi doldurulur; kullanılmayan alan silinmez, "Yok" yazılır.
-->

# N.M Ders adı

<!-- 1. Künye -->
| Tür | Süre | Önkoşul |
| --- | --- | --- |
| Çekirdek / Genişletme | 00 dk | N.M, N.M |

<!-- 2. Öğrenme hedefi: tek cümle, ölçülebilir fiil (yazar, çalıştırır, açıklar, bulur…) -->
**Hedef:** Bu dersin sonunda …

## Bağlam

<!-- 3. Nötr sahne, 2–3 cümle -->

## Kavram

<!-- 4. En fazla 800 kelime. Widget varsa tek satırla gömülür:
<div data-egitim-widget="widget-adi"></div>
Mevcut widget'lar ve kullanım: docs/katki/bilesenler.md -->

## Tahmin et

<!-- 5. Çalıştırmadan önce cevaplanan soru. Soru bileşeniyle yazılır (docs/katki/bilesenler.md):
ilk paragraf soru, ilk numaralı liste seçenekler, sonrası açıklama. data-soru-id site genelinde tek. -->

<div class="egitim-soru" data-soru-id="dX-Y-tahmin" data-tur="tahmin" data-dogru="1" markdown>
Soru metni?

1. Doğru seçenek
2. Yanlış seçenek

Açıklama.
</div>

## Çalıştır

<!-- 6. "Codespaces'te aç" bağlantısı ve test edilmiş komutlar -->

```bash
# komutlar
```

## İncele

<!-- 7. ros2 komutları ve 2–3 soru -->

## Değiştir

<!-- 8. İpuçlu küçük görev -->

## Yap

<!-- 9. Mini görev. CI testinin tam olarak neyi kontrol ettiği yazılır. -->

**CI testi şunu kontrol eder:** …

## Arıza laboratuvarı

<!-- 10. Varsa: belirti → hangi komutla baktım → sebep → düzeltme. Yoksa "Yok". -->

## Hatırla

<!-- 11. Üç kısa soru; her biri data-tur="hatirla" olan bir soru bileşeni (kimlikler: dX-Y-hatirla-1, -2, -3). -->

1. …
2. …
3. …

## Resmi doküman

<!-- 12. docs.ros.org/en/jazzy bağlantıları -->

- [Sayfa adı](https://docs.ros.org/en/jazzy/...)

## Sözlüğe eklenenler

<!-- 13. Bu derste ilk kez geçen terimler -->

- …
