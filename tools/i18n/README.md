# Rehberin EN / RU sürümleri

- `site/index.html` Türkçe rehberdir (ana kaynak). `site/en/` ve `site/ru/` buradaki dosyalarla üretilir.
- `units.json` / `marked.html`: Türkçe sayfadan çıkarılan metin parçaları (dil seçici eklenmeden önceki hâli).
- `en.py`, `ru.py`: parça numarasına göre çeviriler, görsel alt metinleri ve JS metinleri.
- `build.py en ru`: EN/RU sayfalarını yeniden üretir. `arch.py en ru`: mimari diyagramını SVG olarak üretir (`rsvg-convert` ile PNG'ye çevrilip `site/assets/architecture-<dil>.png` olarak kopyalanır).

Türkçe rehberde metin değişirse aynı değişikliği `en.py` ve `ru.py`'de de yapın; parça numaraları `units.json`'dadır.
