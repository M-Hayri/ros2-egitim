/* Mavi Gölge ROS 2 Eğitimi — widget ve soru bileşenlerinin tek JavaScript dosyası.
 *
 * Harici kütüphane yok, ağ isteği yok. Sayfadaki iki tür öğeyi bulup canlandırır:
 *
 *   Widget (tek satır):
 *     <div data-egitim-widget="tek-program-node-grafigi"></div>
 *
 *   Soru (md_in_html ile Markdown içerik):
 *     <div class="egitim-soru" data-soru-id="d0-1-tahmin" data-tur="tahmin" data-dogru="2" markdown>
 *     Soru metni (ilk paragraf).
 *
 *     1. Seçenek A
 *     2. Seçenek B
 *
 *     Açıklama: cevaptan sonra görünen her şey (ilk listeden sonraki öğeler).
 *     </div>
 *
 * Soru cevapları yalnızca kişinin tarayıcısında (localStorage) tutulur.
 * Depolama engelliyse bileşen yine çalışır, yalnızca cevabı hatırlamaz.
 * Yeni widget eklemek için: widgetKaydet("ad", function (kok) { ... }).
 */
(function () {
  "use strict";

  var SURUM = "1";
  var ONEK = "mavigolge-egitim:v" + SURUM + ":";
  var widgetler = {};

  /* ---------- Yardımcılar ---------- */

  function ogeYap(etiket, ozellikler, cocuklar) {
    var oge = document.createElement(etiket);
    if (ozellikler) {
      Object.keys(ozellikler).forEach(function (ad) {
        var deger = ozellikler[ad];
        if (deger === null || deger === undefined || deger === false) return;
        if (ad === "metin") oge.textContent = deger;
        else if (ad === "sinif") oge.className = deger;
        else oge.setAttribute(ad, deger === true ? "" : String(deger));
      });
    }
    (cocuklar || []).forEach(function (cocuk) {
      if (cocuk === null || cocuk === undefined) return;
      oge.appendChild(typeof cocuk === "string" ? document.createTextNode(cocuk) : cocuk);
    });
    return oge;
  }

  var SVG_NS = "http://www.w3.org/2000/svg";

  function svgYap(etiket, ozellikler, cocuklar) {
    var oge = document.createElementNS(SVG_NS, etiket);
    Object.keys(ozellikler || {}).forEach(function (ad) {
      if (ad === "metin") oge.textContent = ozellikler[ad];
      else oge.setAttribute(ad, String(ozellikler[ad]));
    });
    (cocuklar || []).forEach(function (cocuk) {
      oge.appendChild(cocuk);
    });
    return oge;
  }

  function hataGoster(kok, mesaj) {
    console.error("[egitim] " + mesaj);
    kok.textContent = "";
    kok.classList.add("eg-kutu", "eg-hata");
    kok.setAttribute("role", "alert");
    kok.textContent = "Bu bileşen yüklenemedi: " + mesaj;
  }

  /* ---------- Depolama: her erişim try/catch içinde ---------- */

  var depo = {
    oku: function (anahtar) {
      try {
        var ham = window.localStorage.getItem(ONEK + anahtar);
        return ham === null ? null : JSON.parse(ham);
      } catch (e) {
        return null;
      }
    },
    yaz: function (anahtar, deger) {
      try {
        window.localStorage.setItem(ONEK + anahtar, JSON.stringify(deger));
        return true;
      } catch (e) {
        return false;
      }
    },
    sil: function (anahtar) {
      try {
        window.localStorage.removeItem(ONEK + anahtar);
      } catch (e) {
        /* depolama kapalı: silinecek bir şey de yok */
      }
    },
  };

  /* ---------- Soru bileşeni ---------- */

  var TUR_ETIKETI = { tahmin: "Tahmin et", hatirla: "Hatırla" };
  var HARFLER = "ABCDEFGH";
  var gorulenSoruKimlikleri = {};

  function soruKur(kok) {
    var kimlik = kok.getAttribute("data-soru-id");
    var tur = kok.getAttribute("data-tur") || "tahmin";
    var dogru = parseInt(kok.getAttribute("data-dogru"), 10);

    if (!kimlik) return hataGoster(kok, "data-soru-id eksik.");
    if (gorulenSoruKimlikleri[kimlik]) {
      return hataGoster(kok, "Aynı sayfada iki kez kullanılan soru kimliği: " + kimlik);
    }
    gorulenSoruKimlikleri[kimlik] = true;
    if (!TUR_ETIKETI[tur]) return hataGoster(kok, "Bilinmeyen soru türü: " + tur);

    var cocuklar = Array.prototype.slice.call(kok.children);
    var listeSirasi = -1;
    for (var i = 0; i < cocuklar.length; i++) {
      if (cocuklar[i].tagName === "OL") {
        listeSirasi = i;
        break;
      }
    }
    if (listeSirasi < 1) {
      return hataGoster(kok, kimlik + ": önce soru metni, sonra numaralı seçenek listesi olmalı.");
    }
    var secenekler = Array.prototype.slice.call(cocuklar[listeSirasi].children);
    if (isNaN(dogru) || dogru < 1 || dogru > secenekler.length) {
      return hataGoster(kok, kimlik + ": data-dogru 1 ile " + secenekler.length + " arasında olmalı.");
    }

    var soruMetni = ogeYap("div", { sinif: "eg-soru-metni", id: "eg-soru-" + kimlik });
    cocuklar.slice(0, listeSirasi).forEach(function (oge) {
      soruMetni.appendChild(oge);
    });
    var aciklama = ogeYap("div", { sinif: "eg-aciklama", hidden: true });
    cocuklar.slice(listeSirasi + 1).forEach(function (oge) {
      aciklama.appendChild(oge);
    });

    var grup = ogeYap("div", {
      sinif: "eg-secenekler",
      role: "group",
      "aria-labelledby": "eg-soru-" + kimlik,
    });
    var dugmeler = secenekler.map(function (li, sira) {
      var icerik = ogeYap("span");
      while (li.firstChild) icerik.appendChild(li.firstChild);
      var dugme = ogeYap(
        "button",
        { type: "button", sinif: "eg-dugme eg-secenek", "data-secenek": sira + 1 },
        [ogeYap("span", { sinif: "eg-secenek-harf", metin: HARFLER.charAt(sira) + ")" }), icerik]
      );
      grup.appendChild(dugme);
      return dugme;
    });

    var geriBildirim = ogeYap("p", { sinif: "eg-geri-bildirim", "aria-live": "polite" });
    var tekrar = ogeYap("button", {
      type: "button",
      sinif: "eg-dugme",
      hidden: true,
      metin: "Tekrar dene",
      "data-tekrar": true,
    });
    var not = ogeYap("p", { sinif: "eg-not" });

    kok.textContent = "";
    kok.classList.add("eg-kutu", "eg-soru");
    kok.appendChild(ogeYap("span", { sinif: "eg-etiket", metin: TUR_ETIKETI[tur] }));
    [soruMetni, grup, geriBildirim, aciklama, tekrar, not].forEach(function (oge) {
      kok.appendChild(oge);
    });

    function goster(secim) {
      var dogruMu = secim === dogru;
      dugmeler.forEach(function (dugme, sira) {
        var no = sira + 1;
        dugme.disabled = true;
        dugme.setAttribute("aria-pressed", no === secim ? "true" : "false");
        if (no === dogru) dugme.setAttribute("data-sonuc", "dogru");
        else if (no === secim) dugme.setAttribute("data-sonuc", "yanlis");
        else dugme.removeAttribute("data-sonuc");
      });
      kok.setAttribute("data-sonuc", dogruMu ? "dogru" : "yanlis");
      geriBildirim.setAttribute("data-sonuc", dogruMu ? "dogru" : "yanlis");
      geriBildirim.textContent = dogruMu
        ? "Doğru."
        : "Yanlış. Doğru cevap: " + HARFLER.charAt(dogru - 1) + ".";
      if (tur === "tahmin") {
        geriBildirim.textContent += " Şimdi çalıştırıp kendi gözünle gör.";
      }
      aciklama.hidden = aciklama.childNodes.length === 0;
      tekrar.hidden = false;
    }

    function sifirla() {
      dugmeler.forEach(function (dugme) {
        dugme.disabled = false;
        dugme.removeAttribute("aria-pressed");
        dugme.removeAttribute("data-sonuc");
      });
      kok.removeAttribute("data-sonuc");
      geriBildirim.removeAttribute("data-sonuc");
      geriBildirim.textContent = "";
      aciklama.hidden = true;
      tekrar.hidden = true;
      not.textContent = "";
    }

    grup.addEventListener("click", function (olay) {
      var dugme = olay.target.closest("button[data-secenek]");
      if (!dugme || dugme.disabled) return;
      var secim = parseInt(dugme.getAttribute("data-secenek"), 10);
      goster(secim);
      var kaydedildi = depo.yaz("soru:" + kimlik, { secim: secim });
      not.textContent = kaydedildi
        ? "Cevabın yalnızca bu tarayıcıda saklanır."
        : "Tarayıcı depolaması kapalı; cevabın sayfa yenilenince unutulur.";
    });

    tekrar.addEventListener("click", function () {
      depo.sil("soru:" + kimlik);
      sifirla();
      dugmeler[0].focus();
    });

    var kayitli = depo.oku("soru:" + kimlik);
    if (kayitli && kayitli.secim >= 1 && kayitli.secim <= secenekler.length) {
      goster(kayitli.secim);
      not.textContent = "Daha önce verdiğin cevap. Değiştirmek için Tekrar dene.";
    }
  }

  /* ---------- Widget: tek program ve node grafiği (Ders 0.1) ---------- */

  var TNG_PARCALAR = [
    { kimlik: "kamera", ad: "kamera", girdiler: [], x: 2, y: 70 },
    { kimlik: "algilama", ad: "algilama", girdiler: ["kamera"], x: 122, y: 8 },
    { kimlik: "planlayici", ad: "planlayici", girdiler: ["algilama"], x: 242, y: 8 },
    { kimlik: "motor", ad: "motor_surucu", girdiler: ["planlayici"], x: 242, y: 132 },
    { kimlik: "kayitci", ad: "kayitci", girdiler: ["kamera"], x: 122, y: 132 },
  ];
  var TNG_KONULAR = [
    { kaynak: "kamera", hedef: "algilama", ad: "/goruntu", yol: "M98 92 L120 30" },
    { kaynak: "kamera", hedef: "kayitci", ad: "/goruntu", yol: "M98 92 L120 154" },
    { kaynak: "algilama", hedef: "planlayici", ad: "/engeller", yol: "M218 30 L240 30" },
    { kaynak: "planlayici", hedef: "motor", ad: "/hiz_komutu", yol: "M290 52 L290 130" },
  ];
  var DURUM_METNI = {
    calisiyor: "Çalışıyor",
    "veri-geliyor": "Çalışıyor · veri geliyor",
    "veri-gelmiyor": "Çalışıyor · veri gelmiyor",
    durdu: "Durdu",
  };
  var DURUM_KISA = {
    calisiyor: "çalışıyor",
    "veri-geliyor": "çalışıyor",
    "veri-gelmiyor": "veri yok",
    durdu: "durdu",
  };
  var ornekSayaci = 0;

  function parcaBul(kimlik) {
    for (var i = 0; i < TNG_PARCALAR.length; i++) {
      if (TNG_PARCALAR[i].kimlik === kimlik) return TNG_PARCALAR[i];
    }
    return null;
  }

  /* Bir node veri üretiyor mu: süreci ayakta ve tüm girdileri üretiyor. */
  function uretiyor(kimlik, cokenler) {
    if (cokenler[kimlik]) return false;
    return parcaBul(kimlik).girdiler.every(function (girdi) {
      return uretiyor(girdi, cokenler);
    });
  }

  function nodeDurumu(parca, cokenler) {
    if (cokenler[parca.kimlik]) return "durdu";
    if (parca.girdiler.length === 0) return "calisiyor";
    return parca.girdiler.every(function (g) {
      return uretiyor(g, cokenler);
    })
      ? "veri-geliyor"
      : "veri-gelmiyor";
  }

  /* Sürüş zinciri: motor_surucu'dan geriye doğru. Robotun sürmesi için hepsi ayakta olmalı.
     Birden fazla node çökmüşse robot metni motor_surucu'ya en yakın olanı adlandırır. */
  var SURUS_ZINCIRI = ["motor", "planlayici", "algilama", "kamera"];

  function grafRobotMetni(cokenler) {
    var cokenZincir = SURUS_ZINCIRI.filter(function (k) {
      return cokenler[k];
    });
    if (cokenZincir.length === 0) {
      return cokenler.kayitci
        ? { suruyor: true, metin: "Robot sürüyor: kayitci çalışmıyor ama sürüş zincirinde değil." }
        : { suruyor: true, metin: "Robot sürüyor." };
    }
    var ilk = parcaBul(cokenZincir[0]);
    if (ilk.kimlik === "motor") {
      return { suruyor: false, metin: "Robot duruyor: motor_surucu çalışmıyor." };
    }
    return {
      suruyor: false,
      metin: "Robot duruyor: " + ilk.ad + " çalışmıyor, motor_surucu'ya komut gelmiyor.",
    };
  }

  function hareketAzaltilmis() {
    try {
      return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    } catch (e) {
      return false;
    }
  }

  function tekProgramNodeGrafigi(kok) {
    ornekSayaci += 1;
    var okKimligi = "eg-ok-" + ornekSayaci;
    var tekKapali = false; // tek program: bir parça çökünce bütün süreç kapanır
    var cokenler = {}; // node grafiği: yalnızca çöken node'lar
    var secili = "kamera";

    kok.textContent = "";
    kok.classList.add("eg-kutu", "eg-tng");
    kok.appendChild(ogeYap("span", { sinif: "eg-etiket", metin: "Etkileşimli gösterim" }));
    kok.appendChild(
      ogeYap("p", {
        sinif: "eg-not",
        metin:
          "Aynı teslimat robotu iki şekilde yazılmış. Bir parça seç, Çökert'e bas; sonra iki modelde neyin durduğunu ve neyi yeniden başlatabildiğini karşılaştır.",
      })
    );

    /* Kontroller */
    var secim = ogeYap("div", { sinif: "eg-tng-secim", role: "group", "aria-label": "Çökertilecek parça" });
    var secimDugmeleri = {};
    TNG_PARCALAR.forEach(function (parca) {
      var dugme = ogeYap("button", {
        type: "button",
        sinif: "eg-dugme",
        "data-parca": parca.kimlik,
        metin: parca.ad,
      });
      secimDugmeleri[parca.kimlik] = dugme;
      secim.appendChild(dugme);
    });
    var cokert = ogeYap("button", {
      type: "button",
      sinif: "eg-dugme eg-dugme--ana",
      "data-eylem": "cokert",
      metin: "Çökert",
    });
    kok.appendChild(ogeYap("div", { sinif: "eg-tng-kontroller" }, [secim, cokert]));

    /* Sol panel: tek program */
    var tekListe = ogeYap("ul", { sinif: "eg-durum-listesi" });
    var tekSatirlar = {};
    TNG_PARCALAR.forEach(function (parca) {
      var durum = ogeYap("span", { sinif: "eg-durum" });
      var satir = ogeYap("li", { "data-parca": parca.kimlik }, [
        ogeYap("span", { sinif: "eg-parca-adi", metin: parca.ad + "()" }),
        durum,
      ]);
      tekSatirlar[parca.kimlik] = { satir: satir, durum: durum };
      tekListe.appendChild(satir);
    });
    var tekSurec = ogeYap("div", { sinif: "eg-tek-surec" }, [
      ogeYap("p", { sinif: "eg-surec-adi", metin: "süreç: robot_programi" }),
      tekListe,
    ]);
    var tekRobot = ogeYap("p", { sinif: "eg-robot" });
    var tekYeniden = ogeYap("button", {
      type: "button",
      sinif: "eg-dugme",
      "data-eylem": "program-yeniden",
      metin: "Programı yeniden başlat",
    });
    var solPanel = ogeYap("section", { sinif: "eg-panel", "data-model": "tek-program" }, [
      ogeYap("h4", { metin: "Tek program (tek süreç)" }),
      tekSurec,
      tekRobot,
      ogeYap("p", { sinif: "eg-panel-eylem" }, [tekYeniden]),
    ]);

    /* Sağ panel: node grafiği */
    var svg = svgYap("svg", {
      viewBox: "0 0 340 176",
      class: "eg-graf",
      role: "img",
      "aria-label": "Beş node'lu grafik: kamera, algılama ve kayıtçıya; algılama planlayıcıya; planlayıcı motor sürücüye yayın yapar.",
    });
    svg.appendChild(
      svgYap("defs", {}, [
        svgYap(
          "marker",
          {
            id: okKimligi,
            viewBox: "0 0 10 10",
            refX: 9,
            refY: 5,
            markerWidth: 6,
            markerHeight: 6,
            orient: "auto-start-reverse",
          },
          [svgYap("path", { d: "M0 0 L10 5 L0 10 z", class: "eg-graf-ok" })]
        ),
      ])
    );
    var kenarlar = TNG_KONULAR.map(function (konu) {
      var kenar = svgYap(
        "path",
        { d: konu.yol, class: "eg-graf-kenar", "marker-end": "url(#" + okKimligi + ")", "data-kaynak": konu.kaynak },
        [svgYap("title", { metin: konu.ad + " (" + konu.kaynak + " → " + konu.hedef + ")" })]
      );
      svg.appendChild(kenar);
      return { konu: konu, oge: kenar };
    });
    var grafDugumleri = {};
    TNG_PARCALAR.forEach(function (parca) {
      var durumYazisi = svgYap("text", { x: 48, y: 34, class: "eg-graf-durum" });
      var g = svgYap("g", { class: "eg-graf-node", transform: "translate(" + parca.x + " " + parca.y + ")" }, [
        svgYap("rect", { width: 96, height: 44, rx: 8 }),
        svgYap("text", { x: 48, y: 19, metin: parca.ad }),
        durumYazisi,
      ]);
      grafDugumleri[parca.kimlik] = { g: g, yazi: durumYazisi };
      svg.appendChild(g);
    });
    var lejant = ogeYap("p", {
      sinif: "eg-lejant",
      metin: hareketAzaltilmis()
        ? "Oklar: renkli = veri akıyor, soluk gri = veri akmıyor."
        : "Oklar: renkli ve hareketli = veri akıyor, soluk gri = veri akmıyor.",
    });

    var grafListe = ogeYap("ul", { sinif: "eg-durum-listesi" });
    var grafSatirlar = {};
    TNG_PARCALAR.forEach(function (parca) {
      var durum = ogeYap("span", { sinif: "eg-durum" });
      var yeniden = ogeYap("button", {
        type: "button",
        sinif: "eg-dugme eg-dugme--kucuk",
        "data-yeniden": parca.kimlik,
        "aria-label": parca.ad + " node'unu yeniden başlat",
        metin: "Yeniden başlat",
      });
      var satir = ogeYap("li", { "data-parca": parca.kimlik }, [
        ogeYap("span", { sinif: "eg-parca-adi", metin: parca.ad }),
        durum,
        yeniden,
      ]);
      grafSatirlar[parca.kimlik] = { satir: satir, durum: durum, yeniden: yeniden };
      grafListe.appendChild(satir);
    });
    var grafRobot = ogeYap("p", { sinif: "eg-robot" });
    var sagPanel = ogeYap("section", { sinif: "eg-panel", "data-model": "node-grafigi" }, [
      ogeYap("h4", { metin: "Node grafiği (beş ayrı süreç)" }),
      svg,
      lejant,
      grafListe,
      grafRobot,
    ]);

    kok.appendChild(ogeYap("div", { sinif: "eg-tng-paneller" }, [solPanel, sagPanel]));
    var ozet = ogeYap("p", { sinif: "eg-ozet", "aria-live": "polite" });
    kok.appendChild(ozet);
    kok.appendChild(
      ogeYap("p", {
        sinif: "eg-not",
        metin:
          "Burada her node ayrı bir süreçte çalışıyor. ROS 2'de birden fazla node'u tek süreçte toplamak da mümkün; o durumda çökme davranışı değişir (Ders 5.4).",
      })
    );

    function etkilenenler() {
      return TNG_PARCALAR.filter(function (p) {
        return nodeDurumu(p, cokenler) === "veri-gelmiyor";
      }).map(function (p) {
        return p.ad;
      });
    }

    function ciz() {
      TNG_PARCALAR.forEach(function (parca) {
        var tekDurum = tekKapali ? "durdu" : "calisiyor";
        tekSatirlar[parca.kimlik].satir.setAttribute("data-durum", tekDurum);
        tekSatirlar[parca.kimlik].durum.textContent = DURUM_METNI[tekDurum];

        var durum = nodeDurumu(parca, cokenler);
        var satir = grafSatirlar[parca.kimlik];
        satir.satir.setAttribute("data-durum", durum);
        satir.durum.textContent = DURUM_METNI[durum];
        satir.yeniden.disabled = !cokenler[parca.kimlik];
        grafDugumleri[parca.kimlik].g.setAttribute("data-durum", durum);
        grafDugumleri[parca.kimlik].yazi.textContent = DURUM_KISA[durum];

        secimDugmeleri[parca.kimlik].setAttribute("aria-pressed", parca.kimlik === secili ? "true" : "false");
      });
      kenarlar.forEach(function (kenar) {
        kenar.oge.setAttribute("data-akiyor", uretiyor(kenar.konu.kaynak, cokenler) ? "evet" : "hayir");
      });

      tekSurec.setAttribute("data-durum", tekKapali ? "durdu" : "calisiyor");
      tekRobot.setAttribute("data-suruyor", tekKapali ? "hayir" : "evet");
      tekRobot.textContent = tekKapali ? "Robot duruyor: bütün program kapandı." : "Robot sürüyor.";
      tekYeniden.disabled = !tekKapali;

      var robot = grafRobotMetni(cokenler);
      grafRobot.setAttribute("data-suruyor", robot.suruyor ? "evet" : "hayir");
      grafRobot.textContent = robot.metin;

      cokert.disabled = tekKapali && !!cokenler[secili];
    }

    secim.addEventListener("click", function (olay) {
      var dugme = olay.target.closest("button[data-parca]");
      if (!dugme) return;
      secili = dugme.getAttribute("data-parca");
      ciz();
    });

    cokert.addEventListener("click", function () {
      tekKapali = true;
      cokenler[secili] = true;
      ciz();
      var ad = parcaBul(secili).ad;
      var veriYok = etkilenenler();
      ozet.textContent =
        ad + " çöktü. Tek programda bu hata bütün süreci kapattı: beş parçanın beşi durdu ve ancak program baştan başlatılınca geri gelir. " +
        "Node grafiğinde çökme öteki süreçlere yayılmadı: yalnızca " + ad + " durdu" +
        (veriYok.length ? "; " + veriYok.join(", ") + " çalışıyor ama veri alamıyor" : "; öteki node'lar hiç etkilenmedi") +
        ". Orada yalnızca " + ad + " node'unu yeniden başlatman yeter.";
    });

    grafListe.addEventListener("click", function (olay) {
      var dugme = olay.target.closest("button[data-yeniden]");
      if (!dugme || dugme.disabled) return;
      var kimlik = dugme.getAttribute("data-yeniden");
      delete cokenler[kimlik];
      ciz();
      ozet.textContent =
        parcaBul(kimlik).ad + " yeniden başlatıldı; öteki node'lar bu sırada hiç kapanmadı." +
        (tekKapali ? " Tek program hâlâ kapalı: orada tek bir parçayı yeniden başlatmanın yolu yok, bütün program baştan açılmalı." : "");
    });

    tekYeniden.addEventListener("click", function () {
      if (!tekKapali) return;
      tekKapali = false;
      ciz();
      ozet.textContent = "Program baştan başlatıldı: beş parçanın beşi birlikte yeniden açıldı.";
    });

    ciz();
  }

  /* ---------- Kayıt ve başlatma ---------- */

  function widgetKaydet(ad, kur) {
    widgetler[ad] = kur;
  }

  widgetKaydet("tek-program-node-grafigi", tekProgramNodeGrafigi);

  function baslat(kapsam) {
    var alan = kapsam || document;
    Array.prototype.forEach.call(
      alan.querySelectorAll("[data-egitim-widget]:not([data-egitim-hazir])"),
      function (kok) {
        kok.setAttribute("data-egitim-hazir", "");
        var ad = kok.getAttribute("data-egitim-widget");
        var kur = widgetler[ad];
        if (!kur) return hataGoster(kok, "Bilinmeyen widget: " + ad);
        try {
          kur(kok);
        } catch (e) {
          hataGoster(kok, ad + " çalışırken hata: " + e.message);
        }
      }
    );
    Array.prototype.forEach.call(
      alan.querySelectorAll(".egitim-soru:not([data-egitim-hazir])"),
      function (kok) {
        kok.setAttribute("data-egitim-hazir", "");
        try {
          soruKur(kok);
        } catch (e) {
          hataGoster(kok, "Soru çalışırken hata: " + e.message);
        }
      }
    );
  }

  window.Egitim = { surum: SURUM, widgetKaydet: widgetKaydet, baslat: baslat };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      baslat();
    });
  } else {
    baslat();
  }
})();
