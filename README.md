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

3. **Ports** sekmesinde **6080** portunu tarayıcıda aç (parola sorulursa: `ros`).
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
  seviye-0/ … seviye-6/, bitirme/, sozluk/, katki/
  assets/egitim/      Widget ve soru bileşenleri: tek JS (egitim.js), tek CSS (egitim.css)
dersler/              Her dersin başlangıç paketi ve testleri (çözüm kodu burada tutulmaz)
ariza-lab/            Bilerek bozulmuş örnekler
sablonlar/            Ders sayfası şablonu
scripts/              Ortam kontrolü ve CI betikleri
sorular/              Soru bankası: hatırla soruları (derleme anında sayfalara eklenir)
tests/tarayici/       Widget, soru bileşeni ve sayfaların tarayıcı testleri (Playwright, Chromium)
tests/icerik/         Ders sayfası şablonu, soru bankası ve komut koşucusu testleri
```

## Siteyi yerelde derlemek

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

Widget ve soru bileşenlerinin tarayıcı testleri (Chromium):

```bash
pip install -r requirements-docs.txt -r requirements-test.txt
python -m playwright install --with-deps chromium
mkdocs build --strict
python -m pytest tests/tarayici -v
```

Ekran görüntüleri `tests/tarayici/ekran/` klasörüne yazılır.

Ders sayfalarındaki her `bash` bloğunun önünde bir test işareti bulunur (`otomatik`, `arka-plan` ya da `elle`; ayrıntı `scripts/icerik_komutlari.py` dosyasının başında). İşaretleri ve sayfa yapısını denetlemek ROS gerektirmez:

```bash
python3 scripts/icerik_komutlari.py --denetle --listele
python -m pytest tests/icerik -v
```

Komutların kendisi CI'da devcontainer içinde çalıştırılır (`scripts/ci_icerik.sh`). Codespace'te de elle çalıştırılabilir:

```bash
python3 scripts/icerik_komutlari.py --calistir
```

## Katkı

Yeni ders `sablonlar/ders-sablonu.md` kopyalanarak yazılır. Örnekler nötr olur, her komut devcontainer içinde test edilir, teori bölümü 800 kelimeyi geçmez.

## Lisans

Kod [MIT](LICENSE), içerik (`docs/` altındaki metinler ve görseller) [CC BY 4.0](LICENSE-CONTENT) lisanslıdır.
