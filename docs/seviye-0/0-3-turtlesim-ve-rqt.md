# 0.3 Turtlesim ve rqt

| Tür | Süre | Önkoşul |
| --- | --- | --- |
| Çekirdek | 60 dk | [0.2](0-2-ortam-ve-ros2.md) |

**Hedef:** Bu dersin sonunda turtlesim'i klavyeyle **sürer**, rqt ile `/spawn` servisini **çağırarak** ikinci bir kaplumbağa ekler ve onu remap ile **sürersin**.

## Açılış: tekrar

Ders 0.1'den iki soru. Cevapların kaydedilmez; daha önce cevaplamış olsan da boş gelir.

<div class="egitim-tekrar" markdown>
--8<-- "d0-1-hatirla-1.md"

--8<-- "d0-1-hatirla-2.md"
</div>

## Bağlam

Gerçek bir robotu sürmeden önce, ROS'un parçalarını tehlikesiz bir oyuncakla tanımak istiyorsun: komut gönderen bir node, komutu uygulayan bir simülatör ve sistemin içine bakmanı sağlayan araçlar. Turtlesim tam olarak bunun için yazılmış.

## Kavram

**Turtlesim.** ROS 2'yi öğrenmek için yazılmış hafif bir simülatördür; ROS 2'nin en temel düzeyde ne yaptığını gösterir ([Using turtlesim, ros2, and rqt](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html)).

**`ros2 run <paket> <çalıştırılabilir>`.** ROS'ta yazılım *paketler* hâlinde dağıtılır ve bir paketin içinde bir ya da birden fazla *çalıştırılabilir* program bulunabilir. `ros2 run` önce paketin, sonra çalıştırılabilirin adını alır. `turtlesim` paketinin çalıştırılabilirleri `ros2 pkg executables turtlesim` ile listelenir: `draw_square`, `mimic`, `turtle_teleop_key`, `turtlesim_node` (aynı sayfa). Yani `ros2 run turtlesim turtlesim_node` komutunda `turtlesim` paket, `turtlesim_node` o paketteki program.

**Teleop.** `turtle_teleop_key` klavyeyi dinleyen ve kaplumbağaya hız komutu gönderen bir node'dur. Bir ok tuşuna basınca kaplumbağa kısa bir mesafe gidip durur. Resmi doküman bunun gerekçesini şöyle açıklıyor: bağlantı koptuğunda bir robotun son komutu uygulamaya devam etmesi istenmez (aynı sayfa).

**`ros2` ve `rqt`.** `ros2` komutu bir ROS sistemini yönetmek, içine bakmak ve onunla etkileşmek için kullanılır. `rqt` ise ROS 2'nin grafik arayüz aracıdır. rqt'de yapılan her şey komut satırından da yapılabilir; rqt yalnızca daha rahat bir yol sunar (aynı sayfa).

**Servis, ilk bakış.** Turtlesim bazı işlerini servis olarak sunar: `/spawn` yeni bir kaplumbağa ekler, `/turtle1/set_pen` kalemin rengini ve kalınlığını değiştirir (aynı sayfa). Servisleri Ders 2.1'de ayrıntılı göreceksin; bu derste yalnızca rqt'den çağıracaksın.

**Remap.** İkinci bir teleop başlatırsan o da `turtle1`'i sürer, çünkü komutlarını yine `turtle1/cmd_vel` adına gönderir. Bir node'un kullandığı adları değiştirmenin yolu *remap*tir. ROS'a özgü bütün argümanlar `--ros-args` bayrağından sonra yazılır ve adlar `--remap eski:=yeni` (kısaca `-r`) ile değiştirilir ([Passing ROS arguments to nodes](https://docs.ros.org/en/jazzy/How-To-Guides/Node-arguments.html)). İkinci kaplumbağayı sürmek için teleop'un hem `cmd_vel` topic'ini hem de `rotate_absolute` action'ını `turtle2`'ye yönlendirmek gerekir ([Using turtlesim, ros2, and rqt](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html)).

## Tahmin et

<div class="egitim-soru" data-soru-id="d0-3-tahmin" data-tur="tahmin" data-dogru="1" markdown>
rqt ile `turtle2` adında ikinci bir kaplumbağa ekledin. Şimdi yeni bir terminalde hiçbir argüman vermeden ikinci bir `ros2 run turtlesim turtle_teleop_key` başlatıyorsun. Bu yeni teleop hangi kaplumbağayı sürer?

1. `turtle1`'i; ilk teleop ile aynı kaplumbağayı.
2. `turtle2`'yi; yeni teleop yeni kaplumbağayı bulur.
3. İkisini birden.

Teleop komutlarını her zaman `turtle1/cmd_vel` adına gönderir; kaç tane açtığın bunu değiştirmez. `turtle2`'yi sürmek için adı remap ile değiştirmek gerekir. Bu dersin Yap adımı tam olarak bu.
</div>

## Çalıştır

Codespace'in açık değilse [Başlamadan önce](../baslarken.md) sayfasındaki adımlarla aç. Önce `turtlesim` paketinin çalıştırılabilirlerine bak:

<!-- test: otomatik; desen: ^turtlesim turtlesim_node$; desen: ^turtlesim turtle_teleop_key$; desen: ^turtlesim draw_square$; desen: ^turtlesim mimic$ -->
```bash
ros2 pkg executables turtlesim
```

Simülatörü başlat. Kaplumbağa penceresi 6080 portundaki masaüstünde açılır:

<!-- test: arka-plan; hazir: ros2 node list; desen: ^/turtlesim$; sure: 60 -->
```bash
ros2 run turtlesim turtlesim_node
```

İkinci bir terminal aç ve teleop'u başlat. Kaplumbağayı ok tuşlarıyla sürmek için bu terminal etkin (seçili) olmalı:

<!-- test: elle; neden: klavye gerekir -->
```bash title="Test edilmedi · klavye gerekir"
ros2 run turtlesim turtle_teleop_key
```

## İncele

Üçüncü bir terminalde sistemin içine bak. Teleop açıksa node listesinde `/teleop_turtle` da görünür:

<!-- test: otomatik; desen: ^/turtlesim$ -->
```bash
ros2 node list
```

<!-- test: otomatik; desen: ^/turtle1/cmd_vel$; desen: ^/turtle1/pose$ -->
```bash
ros2 topic list
```

<!-- test: otomatik; desen: ^/spawn$; desen: ^/turtle1/set_pen$ -->
```bash
ros2 service list
```

<!-- test: otomatik; desen: ^/turtle1/rotate_absolute$ -->
```bash
ros2 action list
```

Kendine sor:

1. Teleop'u kapatıp açtığında node listesinde ne değişiyor?
2. `/turtle1/cmd_vel` adındaki `turtle1` neyi anlatıyor?
3. Servis listesindeki hangi ad yeni bir kaplumbağa eklemeye benziyor?

## Değiştir

rqt'yi aç. Grafik arayüz olduğu için pencere 6080 portundaki masaüstünde açılır:

<!-- test: elle; neden: grafik arayüz gerekir -->
```bash title="Test edilmedi · grafik arayüz gerekir"
rqt
```

1. Menüden **Plugins → Services → Service Caller**'ı seç. Menüde **Services** görünmüyorsa rqt'yi kapatıp `rqt --force-discover` ile yeniden aç.
2. **Service** listesinin solundaki yenile düğmesine bas ve listeden `/spawn`'ı seç.
3. **Expression** sütununda `name` için `'turtle2'`, `x` için `1.0`, `y` için `1.0` yaz ve **Call**'a bas. Yeni kaplumbağa belirir.
4. İpucu: aynı yolla `/turtle1/set_pen` servisini seç, `r` değerini `255`, `width` değerini `5` yap ve çağır. Teleop terminaline dönüp ok tuşlarına bastığında `turtle1`'in kalın kırmızı bir iz bıraktığını görürsün.

Servis listesini yenilediğinde `/turtle2/...` adlarının da geldiğini gör.

## Yap

`turtle2`'yi kendi teleop'unla sür. Yeni bir terminalde, teleop'un hem hız topic'ini hem de dönme action'ını `turtle2`'ye yönlendir:

<!-- test: elle; neden: klavye gerekir -->
```bash title="Test edilmedi · klavye gerekir"
ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=turtle2/cmd_vel --remap turtle1/rotate_absolute:=turtle2/rotate_absolute
```

Bu terminal etkinken ok tuşları `turtle2`'yi, öteki teleop terminali etkinken `turtle1`'i sürer. Bitirdiğinde teleop terminallerinde `q`, simülatör terminalinde **Ctrl+C** ile kapat.

**Bu derste CI testi yok.** Klavye ve grafik arayüz gerektiriyor. Kontrol, seviye sonundaki canlı gösterimde: koordinatörün önünde iki kaplumbağayı iki ayrı teleop ile sürüyorsun.

## Arıza laboratuvarı

**Belirti.** rqt'de **Call**'a bastın ama yeni kaplumbağa çıkmadı.

**Hangi komutla baktım?** Arızayı kendin üret: Service Caller'da `/spawn`'ı `name` alanına `'turtle1'` yazarak çağır, sonra simülatörün çalıştığı terminale bak.

**Sebep.** Terminalde `A turtle named [turtle1] already exists` hatası görünür. Aynı adla ikinci bir kaplumbağa eklenemez ([Using turtlesim, ros2, and rqt](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html)).

**Düzeltme.** Benzersiz bir ad ver (`'turtle3'`) ve tekrar çağır. Ders: bir arayüzde "hiçbir şey olmadı" gördüğünde, hatanın çoğu zaman o işi yapan node'un terminalinde yazdığını unutma.

## Hatırla

--8<-- "d0-3-hatirla-1.md"

--8<-- "d0-3-hatirla-2.md"

--8<-- "d0-3-hatirla-3.md"

## Resmi doküman

- [Using turtlesim, ros2, and rqt](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html)
- [Passing ROS arguments to nodes via the command-line](https://docs.ros.org/en/jazzy/How-To-Guides/Node-arguments.html)

## Sözlüğe eklenenler

- **Paket:** ROS yazılımının dağıtım birimi; içinde bir ya da birden fazla çalıştırılabilir bulunabilir.
- **Çalıştırılabilir (executable):** Bir paketteki, `ros2 run <paket> <çalıştırılabilir>` ile başlatılan program.
- **Turtlesim:** ROS 2'yi öğrenmek için yazılmış hafif simülatör.
- **Teleop:** Klavyeden (ya da başka bir girdiden) robota hız komutu gönderen node.
- **rqt:** ROS 2'nin grafik arayüz aracı; komut satırında yapılabilen işleri pencereden yapar.
- **Remap:** Bir node'un kullandığı bir adı (topic, servis, action) başlatırken değiştirmek: `--ros-args --remap eski:=yeni`.
