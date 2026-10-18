# 0.1 ROS 2 neden var

| Tür | Süre | Önkoşul |
| --- | --- | --- |
| Çekirdek | 45 dk | [Hazır mısın?](../hazir-misin.md) |

**Hedef:** Bu dersin sonunda tek parçalı bir robot programı ile node grafiği arasındaki farkı, bir parçanın çöktüğü bir örnek üzerinden iki cümleyle **açıklarsın**.

## Bağlam

Bir depoda paket taşıyan küçük bir teslimat robotu düşün. Kamerası görüntü alıyor, bir parça bu görüntüde engel arıyor, bir başkası yol planlıyor, motor sürücü tekerlekleri döndürüyor ve bir kayıtçı her şeyi diske yazıyor. Kayıtçıdaki küçük bir hata yüzünden robotun yolda durması mantıklı mı?

## Kavram

**ROS 2 bir ara katmandır.** Resmi tanıma göre ROS 2, farklı süreçler (çalışan programlar) arasında mesaj alışverişini sağlayan bir yayınla/abone ol mekanizmasına dayanır ([Basic concepts](https://docs.ros.org/en/jazzy/Concepts/Basic.html)). Kısacası robot yazılımını tek bir dev program olarak değil, birbiriyle mesajlaşan küçük programlar olarak yazmanın altyapısını verir.

**Node.** Bu küçük programların her birine *node* denir. Node, ROS grafiğinin bir katılımcısıdır ve her node'un *tek bir mantıksal iş* yapması önerilir ([About nodes](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Nodes.html); aynı öneri [Understanding nodes](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html) eğitiminde de geçer). Node'lar aynı süreçte, farklı süreçlerde ya da farklı makinelerde çalışıp birbirleriyle konuşabilir (aynı sayfa).

**ROS grafiği.** Bir ROS sistemindeki node'ların ve aralarındaki iletişim bağlantılarının oluşturduğu ağa *ROS grafiği* denir ([Basic concepts](https://docs.ros.org/en/jazzy/Concepts/Basic.html)). Toplantıda tahtaya çizeceğimiz şey budur: kutular node'lar, oklar aralarında akan veri.

**Neden parçalara bölüyoruz?** Aşağıdaki gösterimde aynı robot iki biçimde yazılmış. Solda her şey tek bir süreçte, sağda beş ayrı süreçte. Bir parçayı çökert ve iki modelde neyin durduğuna, neyi yeniden başlatabildiğine bak. <!-- kaynaksız: gösterimin nasıl kullanılacağını anlatıyor; teknik iddia içermiyor -->

<div data-egitim-widget="tek-program-node-grafigi"></div>

Burada gördüğün yalıtım ROS'un değil, işletim sisteminin bir özelliği: ayrı süreçlerden biri çöktüğünde ötekiler kapanmaz. ROS bu yalıtımı kullanılabilir kılan şeyi sağlar: süreçlerin birbirini bulması ve mesajlaşması. Çöken node'dan veri bekleyenler ise çalışmaya devam eder ama yeni mesaj alamaz. Robotun sürmesi, bu yüzden sürüş zincirindeki her node'un ayakta olmasına bağlıdır; kayıtçı o zincirde değildir. ROS 2'de birden fazla node'u tek süreçte toplamak da mümkündür ve o zaman bu yalıtım kalkar; bunu Ders 5.4'te göreceksin ([About composition](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Composition.html)).

**İstemci kütüphanesi.** Node'ları bir *istemci kütüphanesi* ile yazarsın: Python için `rclpy`, C++ için `rclcpp`. İkisi de aynı ortak çekirdeğin (`rcl`) üzerine kuruludur. Farklı dillerde yazılmış node'lar birbirine mesaj gönderebilir, çünkü her kütüphane aynı arabirim dosyalarından kendi dilinde kod üretir ([About client libraries](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Client-Libraries.html)). Bu eğitimde Python, yani `rclpy` kullanıyoruz.

**DDS, tek cümleyle.** Node'ların birbirini bulması, verinin paketlenmesi ve taşınması için ROS 2 alttaki ara katman olarak DDS/RTPS kullanır ([About different middleware vendors](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Different-Middleware-Vendors.html)). Seviye 4'e kadar bununla doğrudan uğraşmayacaksın.

**Dağıtım ve LTS.** Bir ROS *dağıtımı* (distro), sürümlenmiş bir ROS paketleri kümesidir; Ubuntu sürümlerine benzer ([Distributions](https://docs.ros.org/en/jazzy/Releases.html)). Her yıl Mayıs'ta yeni bir dağıtım çıkar. Çift yıllarda çıkanlar uzun süreli destekli (LTS) sürümlerdir ve yaklaşık beş yıl desteklenir; tek yıllarda çıkanlar 1,5 yıl desteklenir ([Release schedule](https://docs.ros.org/en/jazzy/The-ROS2-Project/Release-Schedule.html)). Bu eğitimin kullandığı Jazzy Jalisco, Mayıs 2024'te çıkan bir LTS dağıtımıdır ve desteği Mayıs 2029'da biter ([Distributions](https://docs.ros.org/en/jazzy/Releases.html)).

## Tahmin et

<div class="egitim-soru" data-soru-id="d0-1-tahmin" data-tur="tahmin" data-dogru="2" markdown>
Çalıştır adımında iki node açacaksın: kaplumbağa simülatörü (`turtlesim_node`) ve kaplumbağaya kare çizdiren `draw_square`. Kare çizen node'u kapatırsan simülatöre ne olur?

1. Simülatör de kapanır; ikisi aynı sistemin parçası.
2. Simülatör açık kalır; yalnızca kaplumbağaya yeni komut gelmez.
3. Simülatör hata verip yeniden başlar.

İki node ayrı süreçlerde çalışıyor; birini kapatmak ötekini kapatmaz. Simülatör çalışmaya devam eder, yalnızca kaplumbağayı süren komutlar kesilir. Gösterimdeki "veri gelmiyor" durumu tam olarak budur.
</div>

## Çalıştır

Codespace'in açık değilse [Başlamadan önce](../baslarken.md) sayfasındaki adımlarla aç. Terminalde simülatörü başlat; kaplumbağa penceresi 6080 portundaki masaüstünde açılır:

<!-- test: arka-plan; hazir: ros2 node list; desen: ^/turtlesim$; sure: 60 -->
```bash
ros2 run turtlesim turtlesim_node
```

Bu terminal artık simülatöre ayrıldı. Terminal panelindeki **+** düğmesiyle ikinci bir terminal aç ve kare çizen node'u başlat:

<!-- test: arka-plan; hazir: ros2 node list; desen: ^/draw_square$; sure: 60 -->
```bash
ros2 run turtlesim draw_square
```

Kaplumbağa kare çizmeye başlar.

## İncele

Üçüncü bir terminalde çalışan node'ları listele:

<!-- test: otomatik; desen: ^/turtlesim$; desen: ^/draw_square$ -->
```bash
ros2 node list
```

İki satır görmelisin: `/draw_square` ve `/turtlesim`. Şimdi `draw_square`'in çalıştığı ikinci terminale geç, **Ctrl+C** ile kapat ve listeyi yeniden al:

<!-- test: elle; neden: önceki adımda Ctrl+C gerekir -->
```bash title="Test edilmedi · önce draw_square'i Ctrl+C ile kapat"
ros2 node list
```

Kendine sor:

1. Liste kaç satır oldu? Kaplumbağa penceresi hâlâ açık mı?
2. Kaplumbağa neden durdu, ama simülatör neden kapanmadı?
3. Gösterimdeki beş node'dan hangisi `draw_square`'e, hangisi `turtlesim_node`'a benziyor?

## Değiştir

Kapattığın `draw_square`'i aynı terminalde yeniden başlat:

<!-- test: elle; neden: önceki adımda Ctrl+C gerekir -->
```bash title="Test edilmedi · önce draw_square'i Ctrl+C ile kapat"
ros2 run turtlesim draw_square
```

İpucu: simülatörü hiç kapatmadın. Yalnızca çöken (burada: kapattığın) node'u yeniden başlatmak yetti. Gösterimdeki node grafiği panelinde bir node'u çökertip kendi düğmesiyle yeniden başlatarak aynı şeyi gör, sonra tek program panelinde aynısını dene.

## Yap

Kendi seçtiğin nötr bir robot için (örneğin bir süpürge robotu ya da bir sera sulama sistemi) 4–6 node'luk bir grafik çiz: kutular node'lar, oklar aralarında akan veri. Sonra iki şeyi işaretle: hangi node çökerse robot asıl işini yapamaz, hangisi çökerse yapmaya devam eder?

**Bu derste CI testi yok.** Kavram dersi olduğu için yazılacak kod yok. Kontrolü Hatırla soruları ve seviye sonundaki canlı gösterim yapar; çizimini o gösterime getir.

## Arıza laboratuvarı

Bu derste yok. Kavram dersi; ilk arıza laboratuvarı Ders 0.2'de.

## Hatırla

--8<-- "d0-1-hatirla-1.md"

--8<-- "d0-1-hatirla-2.md"

--8<-- "d0-1-hatirla-3.md"

## Resmi doküman

- [Basic concepts](https://docs.ros.org/en/jazzy/Concepts/Basic.html)
- [About nodes](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Nodes.html)
- [Understanding nodes](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html) (Ders 1.1'in konusu)
- [About client libraries](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Client-Libraries.html)
- [About different middleware vendors](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Different-Middleware-Vendors.html)
- [Distributions](https://docs.ros.org/en/jazzy/Releases.html) ve [Release schedule](https://docs.ros.org/en/jazzy/The-ROS2-Project/Release-Schedule.html)
- İleri okuma: [About composition](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Composition.html) (Ders 5.4)

## Sözlüğe eklenenler

- **Node:** ROS grafiğinin bir katılımcısı; tek bir mantıksal iş yapan program.
- **ROS grafiği:** Node'lar ve aralarındaki iletişim bağlantılarından oluşan ağ.
- **İstemci kütüphanesi:** Node yazmak için kullanılan kütüphane; Python'da `rclpy`, C++'ta `rclcpp`.
- **Ara katman (DDS):** Node'ların birbirini bulmasını ve veriyi taşımayı sağlayan alt katman.
- **Dağıtım (distro):** Sürümlenmiş ROS paketleri kümesi; örneğin Jazzy Jalisco.
- **LTS:** Uzun süreli destekli dağıtım; çift yıllarda çıkar, yaklaşık beş yıl desteklenir.
