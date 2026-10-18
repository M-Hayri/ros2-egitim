# 0.2 Ortam ve `ros2` komutu

| Tür | Süre | Önkoşul |
| --- | --- | --- |
| Çekirdek | 60 dk | [0.1](0-1-ros2-neden-var.md) |

**Hedef:** Bu dersin sonunda bir terminalde ROS ortamının yüklü olup olmadığını **kontrol eder** ve `source /opt/ros/jazzy/setup.bash` satırının ne yaptığını **açıklarsın**.

## Bağlam

Yeni bir terminal açıyorsun, `ros2` yazıyorsun ve terminal böyle bir komut tanımadığını söylüyor. Oysa ROS bilgisayarda kurulu. Kurulu olan bir şeyi terminal neden bulamıyor?

## Kavram

**Kurulum ile ortam ayrı şeylerdir.** ROS 2'nin dosyaları diskte durur (Jazzy için `/opt/ros/jazzy`), ama bir terminalin onları kullanabilmesi için o terminalin *ortamının* hazırlanması gerekir. ROS 2, çalışma alanlarını (workspace) kabuk ortamı üzerinden birleştirme fikrine dayanır ([Configuring environment](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)).

**`source` ne yapar?** `source dosya` komutu, dosyadaki satırları *bulunduğun kabukta* çalıştırır. `setup.bash` dosyası da ROS 2'nin çalışması için gereken ortam değişkenlerini ayarlar; örneğin `PATH`'e `ros2` komutunun bulunduğu klasörü ekler ve `ROS_DISTRO` gibi değişkenleri tanımlar ([Configuring environment](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)). Resmi dokümanın deyişiyle, setup dosyaları source edilmeden ROS 2 komutlarına erişemez, ROS 2 paketlerini bulamaz ya da kullanamazsın (aynı sayfa).

Bunun iki sonucu var. Birincisi, ayar terminale özeldir: bir terminalde yaptığın `source`, başka bir terminali etkilemez. İkincisi, her yeni terminalde tekrarlanması gerekir; ya elle ya da satır kabuğun açılış betiğine (`~/.bashrc`) eklenerek (aynı sayfa). Bu eğitimin Codespace'inde satır açılış betiklerine zaten eklenmiş durumda ([.devcontainer/post-create.sh](https://github.com/M-Hayri/ros2-egitim/blob/main/.devcontainer/post-create.sh)); yine de neyin otomatik olduğunu bilmek, otomatik olmadığı bir yerde sorunu bulmanı sağlar.

**Underlay ve overlay, ilk bakış.** Temel ROS kurulumu *underlay*'dir. Kendi yazdığın paketleri derleyip onun üstüne yüklediğinde kendi çalışma alanın *overlay* olur; overlay, underlay'in üstüne katman olarak eklenir ([Configuring environment](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)). Bunu Ders 1.3'te kendi paketini derlerken kullanacaksın.

**Ortamı kontrol etmek.** Ortam doğru kurulduysa `ROS_DISTRO` ve `ROS_VERSION` gibi değişkenler tanımlı olur; paket bulma sorunlarında ilk bakılacak yer bunlardır (aynı sayfa).

**İki değişken daha.** `ROS_DOMAIN_ID`: aynı domain'deki node'lar birbirini bulup mesajlaşır, farklı domain'dekiler bulamaz. Varsayılan değer 0'dır; güvenli bir değer seçmek için 0 ile 101 arasında bir sayı yeterlidir ([About domain ID](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html)). `ROS_AUTOMATIC_DISCOVERY_RANGE`: node'ların birbirini ne kadar uzakta arayacağını belirler. Varsayılan `SUBNET`'tir; `LOCALHOST` aramayı aynı makineyle sınırlar, `OFF` keşfi tamamen kapatır ([Improved dynamic discovery](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Improved-Dynamic-Discovery.html)). Aynı ağda birden fazla ekip çalıştığında bu ikisi, birbirinin robotuna yanlışlıkla komut göndermeyi önler.

**`ros2` komut ağacı.** `ros2`, bir ROS sistemini incelemek ve onunla etkileşmek için ana giriş noktasıdır; `node`, `topic`, `service` gibi alt komutları vardır ve tam liste `ros2 --help` ile görülür ([Introspection with command line tools](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Command-Line-Tools.html)).

## Tahmin et

<div class="egitim-soru" data-soru-id="d0-2-tahmin" data-tur="tahmin" data-dogru="3" markdown>
Ortam değişkenleri temizlenmiş ve açılış betiğini okumayan yeni bir kabuk açıp orada `ros2 --help` yazarsan ne olur?

1. Yardım metni normal şekilde çıkar; ROS diskte kurulu.
2. `ros2` çalışır ama paket listesi boş gelir.
3. Kabuk `ros2` adında bir komut bulamadığını söyler.

ROS diskte kurulu olsa da, kabuğun `ros2`'yi bulabilmesi için `PATH`'in ayarlanmış olması gerekir; bunu `source /opt/ros/jazzy/setup.bash` yapar. Bu kabukta yapılmadığı için komut bulunamaz. Arıza laboratuvarında bunu kendin üreteceksin.
</div>

## Çalıştır

Codespace'in açık değilse [Başlamadan önce](../baslarken.md) sayfasındaki adımlarla aç. Terminalde ortam kontrol betiğini çalıştır:

<!-- test: otomatik; desen: ^\[TAMAM\] ROS_DISTRO = jazzy$; desen: ^Sonuç: ortam hazır\.$ -->
```bash
bash scripts/ortam_kontrol.sh
```

Yedi satırın hepsi `[TAMAM]` olmalı. Betik ROS'u kendisi yüklemez; yalnızca bu terminalin ortamını denetler. Sonra ROS'un ayarladığı değişkenlere bak:

<!-- test: otomatik; desen: ^ROS_DISTRO=jazzy$; desen: ^ROS_VERSION=2$ -->
```bash
printenv | grep -i ROS
```

`ROS_DISTRO=jazzy` ve `ROS_VERSION=2` satırlarını bul. Son olarak komut ağacını aç:

<!-- test: otomatik; desen: ^usage: ros2 -->
```bash
ros2 --help
```

## İncele

İki keşif değişkeninin bu terminaldeki değerine bak. Tanımlı değilse varsayılan geçerlidir:

<!-- test: otomatik; desen: ^ROS_DOMAIN_ID=; desen: ^ROS_AUTOMATIC_DISCOVERY_RANGE= -->
```bash
echo "ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-tanımsız (varsayılan 0)}"
echo "ROS_AUTOMATIC_DISCOVERY_RANGE=${ROS_AUTOMATIC_DISCOVERY_RANGE:-tanımsız (varsayılan SUBNET)}"
```

`ros2` komutunun bulunduğu yeri ve hangi klasörden geldiğini gör:

<!-- test: otomatik; desen: ^/opt/ros/jazzy/bin/ros2$ -->
```bash
command -v ros2
```

Kendine sor:

1. `ros2 --help` çıktısındaki alt komutlardan hangisini 0.1'de zaten kullandın?
2. `command -v ros2` çıktısındaki klasörü `PATH`'e kim ekledi?
3. Codespace'te yeni açtığın her terminalde neden ayrıca `source` yazman gerekmiyor?

## Değiştir

Ortam değişkenlerinin terminale özel olduğunu gör. Bu terminalde domain kimliğini değiştir:

<!-- test: otomatik; terminal: degistir; desen: ^7$ -->
```bash
export ROS_DOMAIN_ID=7
printenv ROS_DOMAIN_ID
```

Şimdi **yeni bir terminal** aç ve aynı değişkene bak:

<!-- test: otomatik; terminal: yeni; cikis: 1 -->
```bash
printenv ROS_DOMAIN_ID
```

İpucu: komut hiçbir şey yazmaz ve başarısız çıkar (çıkış kodu 1), çünkü değişken yeni terminalde tanımlı değil. `export` yalnızca o kabuğu ve ondan başlatılan programları etkiler. Kalıcı olsun istersen satırı `~/.bashrc`'ye eklemen gerekir; bu eğitimde buna ihtiyacın yok.

## Yap

Ortam kontrol betiğini iki farklı terminalde çalıştır: biri normal Codespace terminali, diğeri Arıza laboratuvarındaki temiz kabuk. Sonuçları yan yana koy ve iki cümleyle yaz: aradaki fark neydi, onu ne yarattı?

**Bu derste senin yazdığın kod için CI testi yok.** Kontrol, ortam kontrol betiğinin kendisi. Betik de CI'da iki yönlü sınanıyor: ROS yüklü kabukta 7/7 yeşil ve çıkış kodu 0, temiz kabukta kırmızı ve sıfırdan farklı çıkış kodu.

## Arıza laboratuvarı

**Belirti.** `ros2` yazınca terminal komutu bulamıyor. Bu arızayı kendin üret. Aşağıdaki ilk satır, ortam değişkenleri temizlenmiş (`env -i`) ve açılış betiğini okumayan (`--norc`) yeni bir kabuk açar; sanki ROS hiç yüklenmemiş bir terminal. İkinci satırı o kabukta çalıştır:

<!-- test: otomatik; terminal: ariza; cikis: 127; desen: ros2: command not found -->
```bash
env -i bash --norc
ros2 --help
```

`ros2: command not found` mesajını görmelisin. Yalnızca `bash --norc` yazmak yetmezdi: o kabuk, açtığın terminalin zaten ayarlanmış değişkenlerini miras alır.

**Hangi komutla baktım?** Aynı kabukta ortam kontrol betiğini çalıştır:

<!-- test: otomatik; terminal: ariza; cikis: 1; desen: ^\[HATA\]  ROS_DISTRO = jazzy$; desen: ^İpucu: bu terminalde ROS ortamı yüklenmemiş -->
```bash
bash scripts/ortam_kontrol.sh
```

**Sebep.** Kontroller kırmızı ve `ROS_DISTRO` tanımsız: bu kabukta ROS'un setup dosyası source edilmemiş.

**Düzeltme.** Aynı kabukta source et ve tekrar dene:

<!-- test: otomatik; terminal: ariza; desen: ^usage: ros2; desen: ^Sonuç: ortam hazır\.$ -->
```bash
source /opt/ros/jazzy/setup.bash
ros2 --help
bash scripts/ortam_kontrol.sh
```

İşin bitince `exit` ile temiz kabuktan çık; normal terminaline dönersin.

## Hatırla

--8<-- "d0-2-hatirla-1.md"

--8<-- "d0-2-hatirla-2.md"

--8<-- "d0-2-hatirla-3.md"

## Resmi doküman

- [Configuring environment](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)
- [About domain ID](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html)
- [Improved dynamic discovery](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Improved-Dynamic-Discovery.html)
- [Introspection with command line tools](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Command-Line-Tools.html)

## Sözlüğe eklenenler

- **Kabuk (shell):** Komutları okuyup çalıştıran program; bu eğitimde `bash`.
- **Ortam değişkeni:** Kabuğun ve ondan başlatılan programların gördüğü ad=değer çifti; örneğin `ROS_DISTRO`.
- **source:** Bir dosyadaki satırları bulunduğun kabukta çalıştırmak; ROS'ta ortamı yüklemenin yolu.
- **Underlay / overlay:** Temel kurulum (underlay) ve onun üstüne katman olarak eklenen kendi çalışma alanın (overlay).
- **ROS_DOMAIN_ID:** Hangi node'ların birbirini bulacağını belirleyen sayı; varsayılan 0.
- **ROS_AUTOMATIC_DISCOVERY_RANGE:** Node'ların birbirini ne kadar uzakta arayacağı; varsayılan `SUBNET`.
