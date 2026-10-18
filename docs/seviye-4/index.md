# Seviye 4: Uzay ve zaman

Seviye 4 bittiğinde kişi koordinat çerçevelerini tf2 ile yayınlar ve sorgular, ROS zamanını doğru kullanır, bir QoS uyumsuzluğunu teşhis eder ve verinin ağda nasıl bulunduğunu anlatır. En yoğun seviye bu. Tahmini süre: yaklaşık 9 saat (Çekirdek 6, Genişletme 2,5). Nötr senaryo: tf2 eğitimlerinin klasik lider ve takipçi kaplumbağası.

!!! note "Bu seviye henüz yazılmadı"
    Ders sayfaları sırayla ekleniyor. Aşağıdaki liste bu seviyede neyin öğretileceğini gösterir.

| Ders | Konu | Tür | Süre | Durum |
| --- | --- | --- | --- | --- |
| 4.1 | Çerçeveler ve dönüşümler | Çekirdek | 90 dk | Yazılacak |
| 4.2 | Kuaterniyonlar | Çekirdek | 45 dk | Yazılacak |
| 4.3 | tf2 yayınlamak ve dinlemek | Çekirdek | 120 dk | Yazılacak |
| 4.4 | ROS zamanı ve tf2'de zaman | Çekirdek | 60 dk | Yazılacak |
| 4.5 | Görselleştirme: RViz ve Foxglove | Çekirdek | 60 dk | Yazılacak |
| 4.6 | Hizmet kalitesi: QoS | Genişletme | 90 dk | Yazılacak |
| 4.7 | Keşif ve ağ | Genişletme | 60 dk | Yazılacak |

## Seviye çıkış kriteri

4.3'ün CI testi yeşil. Kişi `view_frames` çıktısındaki ağacı tahtaya çizip her bağlantıyı kimin yayınladığını söylüyor. Koordinatörün verdiği bir kuaterniyonu kabaca hangi yöne baktığıyla yorumluyor.
