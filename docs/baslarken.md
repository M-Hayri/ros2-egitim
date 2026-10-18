# Başlamadan önce

Eğitime başlamak için iki şey gerekiyor: terminalde rahat hareket edebilmek ve çalışma ortamını bir kez açmış olmak.

## 1. Terminal ve git alışkanlığı

ROS komut satırıyla çalışır. Aşağıdaki kaynaklar Seviye 0'dan önce bitirilmeli:

| Kaynak | Ne kadarı | Neden |
| --- | --- | --- |
| [MIT Missing Semester](https://missing.csail.mit.edu/) | İlk iki ders (shell, shell araçları) | Terminalin mantığı |
| [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) | İlk 10 seviye | Terminali oyunla pekiştirmek |
| [Linux Dersleri](https://www.linuxdersleri.net/) | Takılınca başvuru | Türkçe komut referansı |
| [Learn Git Branching](https://learngitbranching.js.org/) | "Main" bölümünün ilk seviyeleri | Branch ve merge mantığı |
| [Pro Git (Türkçe)](https://git-scm.com/book/tr/v2) | İlk 3 bölüm | Başvuru kitabı |

## 2. Çalışma ortamını açmak

Bu eğitimde ROS bilgisayarına kurulmaz. GitHub Codespaces, tarayıcıda içinde ROS 2 Jazzy kurulu bir Linux ortamı açar.

1. Depo sayfasında **Code → Codespaces → Create codespace on main** düğmesine bas.
2. İlk açılış birkaç dakika sürer; ortam bir kez hazırlanır, sonraki açılışlar daha hızlıdır.
3. Terminal açılınca şunu çalıştır:

    ```bash
    bash scripts/ortam_kontrol.sh
    ```

    Bütün satırlar `[TAMAM]` olmalı.

4. Alt paneldeki **Ports** sekmesinde **6080** numaralı portun yanındaki küre simgesine bas. Tarayıcıda bir masaüstü açılır; parola: `ros`.
5. Terminalde kaplumbağa penceresini aç:

    ```bash
    ros2 run turtlesim turtlesim_node
    ```

    Pencere 6080 portundaki masaüstünde görünür.

!!! tip "Kotan"
    Kişisel ücretsiz GitHub hesabı ayda 120 çekirdek-saat Codespaces kullanımı verir. 2 çekirdekli makinede bu yaklaşık 60 saat demektir. İşin bitince Codespace'i durdur; açık bırakılan ortam kotadan yer.

!!! info "Kendi bilgisayarında çalışmak istersen"
    Aynı ortam, Docker kurulu bir bilgisayarda VS Code'un **Dev Containers** eklentisiyle de açılabilir: depoyu klonla, VS Code'da aç, "Reopen in Container" de.
