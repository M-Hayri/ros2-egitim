<div class="egitim-soru" data-soru-id="d0-3-hatirla-3" data-tur="hatirla" data-dogru="1" markdown>
İkinci bir teleop ile `turtle2`'yi sürmek için ne gerekir?

1. Teleop'u başlatırken `turtle1` adlarını `--ros-args --remap` ile `turtle2`'ye yönlendirmek.
2. Simülatörü kapatıp yalnızca `turtle2` adlı tek bir kaplumbağayla yeniden başlatmak.
3. Hiçbir şey; ikinci teleop, açık olan yeni kaplumbağayı kendiliğinden bulur.

Teleop her zaman `turtle1` adlarını kullanır. Remap, node başlatılırken bu adları değiştirmenin yoludur; `turtle2` için hem `cmd_vel` topic'i hem de `rotate_absolute` action'ı yönlendirilir.
</div>
