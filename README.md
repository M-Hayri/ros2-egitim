# Mavi Gölge ROS 2 Eğitimi

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/M-Hayri/ros2-egitim)

ROS 2'yi uygulayarak öğrenmek için açık kaynak, etkileşimli bir eğitim. Mavi Gölge yazılım ekibi için hazırlandı; herkesin kullanımına açık.

- **Site:** https://M-Hayri.github.io/ros2-egitim/
- **ROS sürümü:** ROS 2 Jazzy, Python (rclpy)
- **Çalışma ortamı:** GitHub Codespaces (kurulum yok, tarayıcıda Linux + ROS 2 + masaüstü)

## Hızlı başlangıç

1. Yukarıdaki **Open in GitHub Codespaces** düğmesine bas. İlk açılış birkaç dakika sürer.
2. Terminalde ortamı kontrol et:

   ```bash
   bash scripts/ortam_kontrol.sh
   ```

3. **Ports** sekmesinde **6080** portunu tarayıcıda aç (masaüstü parolası: `ros`).
4. Kaplumbağayı çalıştır:

   ```bash
   ros2 run turtlesim turtlesim_node
   ```

Kendi bilgisayarında çalışmak istersen: Docker ve VS Code **Dev Containers** eklentisi kur, depoyu klonla, VS Code'da aç ve "Reopen in Container" de.

## Yapay zekâ kuralı

Kodu sen yazarsın; yapay zekâya kod yazdırmak yok. Bir hata mesajını anlamak için yapay zekâya sorduysan, dersin notuna `YZ: ne sordum → ne öğrendim` biçiminde yaz. Bunu yazmak puan kaybettirmez; kaybettiren, kendi kodunu açıklayamamaktır.

## Depo düzeni

```
.devcontainer/        Çalışma ortamı: ROS 2 Jazzy, turtlesim, rqt, noVNC masaüstü
.github/workflows/    build.yml (devcontainer içinde derleme ve testler),
                      content.yml (içerik denetimi), pages.yml (site yayını)
docs/                 Sitenin içeriği (MkDocs Material)
  seviye-0/ … seviye-6/, bitirme/, sozluk/, widgets/
dersler/              Her dersin başlangıç paketi ve testleri (çözüm kodu burada tutulmaz)
ariza-lab/            Bilerek bozulmuş örnekler
sablonlar/            Ders sayfası şablonu
scripts/              Ortam kontrolü ve CI betikleri
```

## Siteyi yerelde derlemek

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

## Katkı

Yeni ders `sablonlar/ders-sablonu.md` kopyalanarak yazılır. Örnekler nötr olur, her komut devcontainer içinde test edilir, teori bölümü 800 kelimeyi geçmez.

## Lisans

Kod [MIT](LICENSE), içerik (`docs/` altındaki metinler ve görseller) [CC BY 4.0](LICENSE-CONTENT) lisanslıdır.
