# Başlamadan önce

Eğitime başlamak için iki şey gerekiyor: terminalde ve git'te temel hareketleri bilmek ve çalışma ortamını bir kez açmış olmak.

## 1. Terminal ve git

[Hazır mısın?](hazir-misin.md) sayfasındaki beş soruluk öz yoklamayı yap. Takıldığın yer varsa, aynı sayfadaki kaynak tablosu nereden tamamlayacağını gösterir.

## 2. Çalışma ortamını açmak

Bu eğitimde ROS bilgisayarına kurulmaz. GitHub Codespaces, tarayıcıda içinde ROS 2 Jazzy kurulu bir Linux ortamı açar.

1. Depo sayfasında **Code → Codespaces → Create codespace on main** düğmesine bas. İlk açılış birkaç dakika sürer; ortam bir kez hazırlanır, sonraki açılışlar daha hızlıdır.
2. Ekran açılınca alt panelde bir **Terminal** göreceksin. Ortamı kontrol et:

    <!-- test: otomatik; desen: ^Sonuç: ortam hazır\.$ -->
    ```bash
    bash scripts/ortam_kontrol.sh
    ```

    Yedi satırın hepsi `[TAMAM]` olmalı.

## 3. Masaüstünü açmak (Ports sekmesi)

ROS'un pencereli programları (kaplumbağa simülatörü, rqt) Codespace'in içindeki bir masaüstünde açılır. O masaüstünü tarayıcıda **Ports** sekmesinden görürsün.

!!! warning "Ekran görüntüleri bekleniyor"
    Bu bölümün ekran görüntüleri bir sonraki Codespace oturumunda alınıp eklenecek. O zamana kadar adımları metinden takip et.

1. Alt paneldeki sekmelerden **Ports**'a tıkla. Sekme, Terminal'in yanındadır.
2. Listede **6080** numaralı portu bul; etiketi **Masaüstü (noVNC)**.
3. Satırın üzerine gel ve **tarayıcıda aç** (küre) simgesine bas. Yeni bir sekmede noVNC sayfası açılır.
4. noVNC sayfasında **Connect**'e bas. Parola sorulursa `ros` yaz. Boş bir masaüstü görürsün. **Connect** düğmesi çıkmazsa masaüstü zaten açılmıştır; bir sonraki adıma geç.
5. Codespace sekmesine dön ve terminalde kaplumbağa penceresini aç:

    <!-- test: arka-plan; hazir: ros2 node list; desen: ^/turtlesim$; sure: 60 -->
    ```bash
    ros2 run turtlesim turtlesim_node
    ```

    Pencere, noVNC sekmesindeki masaüstünde görünür. Kapatmak için terminalde **Ctrl+C**.

**Ports sekmesi görünmüyorsa:**

- Alt panel tamamen kapalıysa **Ctrl+`** (ters tırnak) ile aç.
- Panel açık ama **Ports** sekmesi yoksa: **F1**'e bas, açılan kutuya `Ports` yaz ve listeden Ports görünümünü odaklayan komutu seç.
- Codespace açıldıktan kısa süre sonra sağ altta 6080 portuyla ilgili bir bildirim de çıkabilir; oradaki tarayıcıda açma düğmesi de aynı işi yapar.

!!! tip "Kotan"
    Kişisel ücretsiz GitHub hesabı ayda 120 çekirdek-saat Codespaces kullanımı verir. 2 çekirdekli makinede bu yaklaşık 60 saat demektir. İşin bitince Codespace'i durdur; açık bırakılan ortam kotadan yer.

!!! info "Kendi bilgisayarında çalışmak istersen"
    Aynı ortam, Docker kurulu bir bilgisayarda VS Code'un **Dev Containers** eklentisiyle de açılabilir: depoyu klonla, VS Code'da aç, "Reopen in Container" de.
