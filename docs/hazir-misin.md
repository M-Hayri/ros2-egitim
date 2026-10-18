# Hazır mısın?

ROS komut satırıyla çalışır ve bu eğitimdeki her görev bir git deposunda yürür. Seviye 0'a başlamadan önce terminalde ve git'te temel hareketleri bilmen gerekiyor. Bu sayfa ayrı bir kurs değil: aşağıdaki beş soru neyi bilmen gerektiğini gösterir, tablo da eksik kalanı nereden tamamlayacağını.

## Öz yoklama

Cevapların yalnızca bu tarayıcıda tutulur, kimse görmez. Takıldığın soru, tablodan hangi kaynağa bakacağını söyler.

<div class="egitim-soru" data-soru-id="hazir-pwd" data-tur="yoklama" data-dogru="2" markdown>
Terminalde `pwd` yazınca ne görürsün?

1. Bulunduğun klasördeki dosyaların listesini.
2. Bulunduğun klasörün tam yolunu.
3. Kullanıcı adını ve parolanın gücünü.

`pwd` (print working directory) bulunduğun klasörün tam yolunu yazar. Dosyaları listeleyen komut `ls`'dir. Kaynak: [Missing Semester: Introduction to the Shell](https://missing.csail.mit.edu/2026/course-shell/).
</div>

<div class="egitim-soru" data-soru-id="hazir-cd" data-tur="yoklama" data-dogru="1" markdown>
`cd ..` ne yapar?

1. Bir üst klasöre geçer.
2. Ana klasörüne (home) döner.
3. Son çalıştırdığın komutu geri alır.

`..` her zaman bir üst klasör demektir. Ana klasöre `cd` ya da `cd ~` ile dönülür. Kaynak: [Missing Semester: Introduction to the Shell](https://missing.csail.mit.edu/2026/course-shell/).
</div>

<div class="egitim-soru" data-soru-id="hazir-source" data-tur="yoklama" data-dogru="3" markdown>
`ayar.sh` dosyası bir ortam değişkeni tanımlıyor. `bash ayar.sh` ile `source ayar.sh` arasındaki fark ne?

1. Fark yok; ikisi de dosyayı bulunduğun kabukta çalıştırır ve değişken kalır.
2. `bash` değişkeni kalıcı yapar; `source` dosyayı yalnızca okur, çalıştırmaz.
3. `bash` dosyayı ayrı bir kabukta çalıştırır, değişken kaybolur; `source` bulunduğun kabukta çalıştırır.

`source` (kısaca `.`) dosyadaki komutları bulunduğun kabukta okuyup çalıştırır; `bash ayar.sh` ise yeni bir kabuk başlatır ve o kabuk kapanınca değişkeni de götürür. ROS ortamı bu yüzden `source` ile yüklenir; Ders 0.2'nin konusu tam olarak bu. Kaynaklar: [Bash kılavuzu: `.` ve `source`](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html#index-_002e), ortam değişkenleri ve `export` için [Missing Semester: Command-line Environment](https://missing.csail.mit.edu/2026/command-line-environment/).
</div>

<div class="egitim-soru" data-soru-id="hazir-branch" data-tur="yoklama" data-dogru="2" markdown>
`git branch yeni-dal` komutundan sonra hangi daldasın?

1. `yeni-dal`'da; komut dalı açıp ona geçer.
2. Önceki dalında; komut dalı yalnızca oluşturur.
3. Hiçbir dalda; önce `git commit` yapman gerekir.

`git branch` yeni dalı oluşturur ama sana geçirmez. Geçmek için `git switch yeni-dal` (ya da `git checkout yeni-dal`) kullanılır. Kaynak: [Pro Git 3.1: Dallar](https://git-scm.com/book/tr/v2/Git-Dallar%c4%b1-Dallar); alıştırma için [Learn Git Branching](https://learngitbranching.js.org/).
</div>

<div class="egitim-soru" data-soru-id="hazir-commit" data-tur="yoklama" data-dogru="1" markdown>
İki dosyayı değiştirdin, yalnızca birine `git add` yaptın ve `git commit -m "mesaj"` yazdın. Commit neyi kaydeder?

1. Yalnızca `git add` ile hazırladığın dosyadaki değişikliği.
2. İki dosyadaki bütün değişiklikleri.
3. Hiçbir şeyi; iki dosyanın da eklenmesi gerekir.

Commit yalnızca hazırlık alanına (staging area) eklenmiş değişiklikleri kaydeder. Öteki dosya değişmiş ama kaydedilmemiş olarak kalır. Kaynak: [Pro Git 2.2: Değişikliklerin Repoya Kaydedilmesi](https://git-scm.com/book/tr/v2/Git-Temelleri-De%c4%9fi%c5%9fikliklerin-Repoya-Kaydedilmesi).
</div>

## Eksiğini nereden tamamlarsın?

| Kaynak | Ne kadarı | Neden |
| --- | --- | --- |
| [MIT Missing Semester](https://missing.csail.mit.edu/) | [Introduction to the Shell](https://missing.csail.mit.edu/2026/course-shell/) ve [Command-line Environment](https://missing.csail.mit.edu/2026/command-line-environment/) | Terminalin mantığı, ortam değişkenleri |
| [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) | İlk 10 seviye | Terminali oyunla pekiştirmek |
| [Linux Dersleri](https://www.linuxdersleri.net/) | Takılınca başvuru | Türkçe komut referansı |
| [Learn Git Branching](https://learngitbranching.js.org/) | "Main" bölümünün ilk seviyeleri | Branch ve merge mantığı |
| [Pro Git (Türkçe)](https://git-scm.com/book/tr/v2) | İlk 3 bölüm | Başvuru kitabı |

Beşini de doğru cevapladıysan [Başlamadan önce](baslarken.md) sayfasına geç ve çalışma ortamını aç.
