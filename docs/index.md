# Mavi Gölge ROS 2 Eğitimi

Bu eğitimi bitiren kişi ROS 2'de node, servis, action ve launch dosyası yazar, başkasının kurduğu bir sistemi okur ve ekip toplantısında aynı terimlerle konuşur. Eğitim ROS 2 Jazzy ve Python ile yürür; kurulum gerekmez, her şey tarayıcıda açılan bir çalışma ortamında çalışır.

## Nasıl çalışır?

Her ders aynı sekiz adımlı ritmi izler:

1. **Bağlam:** Kavramı gerektiren kısa bir sahne.
2. **Kavram:** Kısa bir metin ve tarayıcıda çalışan küçük bir etkileşimli gösterim.
3. **Tahmin et:** Bir komutun ya da kodun ne yapacağını çalıştırmadan önce tahmin edersin.
4. **Çalıştır:** Aynı şeyi gerçek ROS ortamında çalıştırırsın.
5. **İncele:** `ros2` komutlarıyla sistemin içine bakarsın.
6. **Değiştir:** Küçük bir değişiklik yaparsın.
7. **Yap:** Kendi mini görevini yazarsın; otomatik testler kontrol eder.
8. **Hatırla:** Üç kısa soru.

Bazı derslerde bir de **arıza laboratuvarı** vardır: sistem bilerek bozulmuştur, sen belirtiden sebebe gidersin.

## Seviyeler

| Seviye | Konu |
| --- | --- |
| [0](seviye-0/index.md) | Giriş: ortam, turtlesim, rqt |
| [1](seviye-1/index.md) | İletişim: node, topic, paket, kendi mesaj tipin |
| [2](seviye-2/index.md) | Etkileşim: servis, parametre, action |
| [3](seviye-3/index.md) | Sistem kurmak: launch, namespace, kayıt, loglar |
| [4](seviye-4/index.md) | Uzay ve zaman: tf2, ROS zamanı, QoS, keşif |
| [5](seviye-5/index.md) | Araç kutusu: executor, yaşam döngüsü, test, hata ayıklama |
| [6](seviye-6/index.md) | Simülasyon: URDF, Gazebo, ros_gz köprüsü |
| [Bitirme](bitirme/index.md) | Devriye robotu ve sunum |

Her seviye bir **kapıyla** biter: seviyenin çıkış kriteri sağlanmadan sonraki seviyeye geçilmez.

## Yapay zekâ kuralı

Kodu sen yazarsın. Yapay zekâya kod yazdırmak yok. Bir hata mesajını anlamak için yapay zekâya sorduysan, dersin notuna şunu yaz:

> YZ: ne sordum → ne öğrendim

Bunu yazmak puan kaybettirmez. Bu notlar, insanların nerede takıldığını gösterir ve dersleri iyileştirmek için kullanılır. Kaybettiren tek şey, kendi kodunu açıklayamamaktır.

## Lisans

Kod [MIT](https://opensource.org/license/mit), içerik [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) lisanslıdır.
