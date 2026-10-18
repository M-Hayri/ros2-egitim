# Hazır mısın?

ROS komut satırıyla çalışır ve bu eğitimdeki her görev bir git deposunda yürür. Seviye 0'a başlamadan önce terminalde ve git'te temel hareketleri bilmen gerekiyor. Bu sayfa ayrı bir kurs değil: aşağıdaki beş soru neyi bilmen gerektiğini gösterir, tablo da eksik kalanı nereden tamamlayacağını.

## Öz yoklama

Cevapların yalnızca bu tarayıcıda tutulur, kimse görmez. Takıldığın soru, tablodan hangi kaynağa bakacağını söyler.

<div class="egitim-soru" data-soru-id="hazir-pwd" data-tur="yoklama" data-dogru="2" markdown>
Terminalde `pwd` yazınca ne görürsün?

1. Bulunduğun klasördeki dosyaların listesini.
2. Bulunduğun klasörün tam yolunu.
3. Kullanıcı adını ve parolanın gücünü.

`pwd` (print working directory) bulunduğun klasörün tam yolunu yazar. Dosyaları listeleyen komut `ls`'dir. Kaynak: Missing Semester, 1. ders.
</div>

<div class="egitim-soru" data-soru-id="hazir-cd" data-tur="yoklama" data-dogru="1" markdown>
`cd ..` ne yapar?

1. Bir üst klasöre geçer.
2. Ana klasörüne (home) döner.
3. Son çalıştırdığın komutu geri alır.

`..` her zaman bir üst klasör demektir. Ana klasöre `cd` ya da `cd ~` ile dönülür. Kaynak: Missing Semester, 1. ders.
</div>

<div class="egitim-soru" data-soru-id="hazir-source" data-tur="yoklama" data-dogru="3" markdown>
`ayar.sh` dosyası bir ortam değişkeni tanımlıyor. `bash ayar.sh` ile `source ayar.sh` arasındaki fark ne?

1. Fark yok; ikisi de dosyayı çalıştırır.
2. `source` dosyayı yalnızca okur, çalıştırmaz.
3. `bash ayar.sh` dosyayı ayrı bir kabukta çalıştırır ve değişken o kabukla birlikte kaybolur; `source ayar.sh` dosyayı bulunduğun kabukta çalıştırır ve değişken kalır.

ROS ortamı bu yüzden `source` ile yüklenir; Ders 0.2'nin konusu tam olarak bu. Kaynak: Missing Semester, 2. ders.
</div>

<div class="egitim-soru" data-soru-id="hazir-branch" data-tur="yoklama" data-dogru="2" markdown>
`git branch yeni-dal` komutundan sonra hangi daldasın?

1. `yeni-dal`'da; komut dalı açıp ona geçer.
2. Önceki dalında; komut dalı yalnızca oluşturur.
3. Hiçbir dalda; önce `git commit` yapman gerekir.

`git branch` yeni dalı oluşturur ama sana geçirmez. Geçmek için `git switch yeni-dal` (ya da `git checkout yeni-dal`) kullanılır. Kaynak: Pro Git, 3. bölüm; Learn Git Branching.
</div>

<div class="egitim-soru" data-soru-id="hazir-commit" data-tur="yoklama" data-dogru="1" markdown>
İki dosyayı değiştirdin, yalnızca birine `git add` yaptın ve `git commit -m "mesaj"` yazdın. Commit neyi kaydeder?

1. Yalnızca `git add` ile hazırladığın dosyadaki değişikliği.
2. İki dosyadaki bütün değişiklikleri.
3. Hiçbir şeyi; iki dosyanın da eklenmesi gerekir.

Commit yalnızca hazırlık alanına (staging area) eklenmiş değişiklikleri kaydeder. Öteki dosya değişmiş ama kaydedilmemiş olarak kalır. Kaynak: Pro Git, 2. bölüm.
</div>

## Eksiğini nereden tamamlarsın?

| Kaynak | Ne kadarı | Neden |
| --- | --- | --- |
| [MIT Missing Semester](https://missing.csail.mit.edu/) | İlk iki ders (shell, shell araçları) | Terminalin mantığı |
| [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) | İlk 10 seviye | Terminali oyunla pekiştirmek |
| [Linux Dersleri](https://www.linuxdersleri.net/) | Takılınca başvuru | Türkçe komut referansı |
| [Learn Git Branching](https://learngitbranching.js.org/) | "Main" bölümünün ilk seviyeleri | Branch ve merge mantığı |
| [Pro Git (Türkçe)](https://git-scm.com/book/tr/v2) | İlk 3 bölüm | Başvuru kitabı |

Beşini de doğru cevapladıysan [Başlamadan önce](baslarken.md) sayfasına geç ve çalışma ortamını aç.
