# Seviye 3: Sistem kurmak

Seviye 3 bittiğinde kişi birden fazla node'u tek komutla, YAML parametreleri ve namespace'lerle ayağa kaldırır, sistemin verisini kaydedip tekrar oynatır ve logları okuyarak sorunu bulur. Tahmini süre: 7 saat (Çekirdek 5, Genişletme 2).

!!! note "Bu seviye henüz yazılmadı"
    Ders sayfaları sırayla ekleniyor. Aşağıdaki liste bu seviyede neyin öğretileceğini gösterir.

| Ders | Konu | Tür | Süre | Durum |
| --- | --- | --- | --- | --- |
| 3.1 | Launch dosyalarına giriş | Çekirdek | 90 dk | Yazılacak |
| 3.2 | Substitution ve olay işleyiciler | Genişletme | 60 dk | Yazılacak |
| 3.3 | Namespace, remap ve YAML parametreleri | Çekirdek | 90 dk | Yazılacak |
| 3.4 | Kayıt ve tekrar oynatma | Çekirdek | 75 dk | Yazılacak |
| 3.5 | Loglar ve rqt\_console | Çekirdek | 45 dk | Yazılacak |
| 3.6 | Paket geliştirme alışkanlıkları | Genişletme | 60 dk | Yazılacak |

## Seviye çıkış kriteri

3.3 ve 3.4'ün CI testleri yeşil. Tek bir `ros2 launch` komutu en az üç node'u, iki namespace ve YAML parametreleriyle başlatıyor. Kişi koordinatörün verdiği yabancı bir launch dosyasını okuyup hangi node'un hangi adla ve hangi parametrelerle başlayacağını önceden söylüyor.
