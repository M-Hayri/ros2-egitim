# Seviye 6: Simülasyonu tanımak

Seviye 6 bittiğinde kişi bir robotun URDF tanımını okur, hazır bir robotu Gazebo'da açıp kendi node'uyla ROS üzerinden yönetir ve simülasyon zamanının sisteme etkisini anlatır. Robot bizim değil: amaç ortamı tanımak. Tahmini süre: yaklaşık 6,5 saat (Çekirdek 4,5, Genişletme 2). Başlamadan önce Gazebo'nun Codespaces'teki hızı ölçülür; yetersizse dersler MVSim ya da yerel Docker ile verilir.

!!! note "Bu seviye henüz yazılmadı"
    Ders sayfaları sırayla ekleniyor. Aşağıdaki liste bu seviyede neyin öğretileceğini gösterir.

| Ders | Konu | Tür | Süre | Durum |
| --- | --- | --- | --- | --- |
| 6.1 | URDF ile robot tanımı | Çekirdek | 120 dk | Yazılacak |
| 6.2 | Gazebo'ya giriş | Çekirdek | 75 dk | Yazılacak |
| 6.3 | ros\_gz köprüsü ve simülasyon zamanı | Çekirdek | 75 dk | Yazılacak |
| 6.4 | Hazır bir robotu ROS'tan yönetmek | Genişletme | 120 dk | Yazılacak |

## Seviye çıkış kriteri

6.1'deki URDF ağacı doğru çiziliyor. Hazır robot kişinin kendi launch dosyasıyla, `use_sim_time` açık olarak kalkıyor ve kişinin node'uyla hareket ediyor. Kişi Gazebo ile ROS arasındaki köprüyü tahtaya çizip hangi verinin hangi yöne geçtiğini anlatıyor.
