# HSK5_SC031–SC040 — fiziksel WebP denetimi (2026-10-10)

Kaynak: `uysalayhan23/newChinese` / `main` Git tree, GitHub tarafından döndürülen mevcut blob SHA değerleri. **Bu belge yeni görüntü üretildiği ya da yüklendiği anlamına gelmez.**

## Fiziksel durum

Toplam 10 sahne × 5 zorunlu WebP = **50 dosya**. Repo tree içinde **37/50 fiziksel dosya mevcut**, **13 WebP dosyası eksik**. SC031 preview 256×455 olduğundan mevcut sayılsa bile 720×1280 kalite kriterini geçmez. Dolayısıyla **14 çıktı/kalite onarım kalemi** vardır (13 eksik dosya + 1 uygunsuz mevcut preview).

| Sahne | Fiziksel asset | Eksik veya yeniden üretilecek | Ek kalite engeli |
| --- | ---: | --- | --- |
| HSK5_SC031 | 5/5 | preview yeniden üretilecek | 256×455 preview; 720×1280 gerekli |
| HSK5_SC032 | 4/5 | preview | 540×960 Neighborhood BG; gerçek HD kaynak gerekli |
| HSK5_SC033 | 3/5 | char_liu_mei, preview | Liu Mei `face_right` canonical kaynak gerekir |
| HSK5_SC034 | 4/5 | preview | canonical BG/CHAR_A/CHAR_B/FG hazır |
| HSK5_SC035 | 3/5 | char_liu_mei, preview | 540×960 Neighborhood BG ve Liu Mei `face_right` |
| HSK5_SC036 | 4/5 | preview | canonical BG/CHAR_A/CHAR_B/FG hazır |
| HSK5_SC037 | 3/5 | char_liu_mei, preview | Liu Mei `face_right` canonical kaynak gerekir |
| HSK5_SC038 | 4/5 | preview | 540×960 Neighborhood BG; gerçek HD kaynak gerekli |
| HSK5_SC039 | 3/5 | char_liu_mei, preview | Liu Mei `face_right` canonical kaynak gerekir |
| HSK5_SC040 | 4/5 | preview | canonical BG/CHAR_A/CHAR_B/FG hazır |

## Teknik ve kimlik kilitleri

- SC031/034/040: Community Center BG blob `6ba20dfb8423743e855c90dcd4212a17a866e9b7`, 941×1672.
- SC036: City Park BG blob `d6dc8b286b482c84716db61f550b2aafa08aec5c`, 768×1365.
- SC032/035/038: Neighborhood BG blob `b3dc36b60ee3b552f398ef5707e2e9992eab0eff`, 540×960, yukarı ölçekleme **yasak**.
- Zhang Wei approved blob `44a7a521b7fa64466111c30f6830904081c3767d`; Chen Yu approved blob `ee14b09ae3c8cc4f5e539a54884798900f2ad85b`.
- Repozitörde adı `liu_mei` olan görsel dosyaların SHA taramasında yalnız `eea4742918bf5b78f222b54631de8f71a4c824a7` ve `042f301cc718d74440126553e0e307d94566c267` canonical kaynakları tespit edildi; her ikisi de önceki sahne manifestlerinde `face_left` olarak kullanılıyor. `face_right` onayı verilmedi.

## İşlem kapısı

GitHub connector ile repo **okuma ve yazma mümkün**; ancak görüntü işleyicisinin çalıştığı konteyner GitHub'a DNS/TCP erişemiyor. Doğrudan indirme ile `raw.githubusercontent.com` bağlantısı başarısız oldu. Bu nedenle bu oturumda fiziksel dört-katmanlı kompozit WebP üretimi ve GitHub'a binary preview upload **tamamlanmadı**.

Kaynak dosyalar yerelde erişilebilir bir checkout'ta işlenebildiğinde `tools/prepare_hsk5_sc031_sc040.py` ile SC031/034/036/040 preview'ları hazırlanabilir. Gerçek görüntü QA'sı sonrası `tools/compose_hsk5_sc031_sc040.py --accept` kalite ve kaynak provenance kanıtı ister. **Sahne kapatma sonuçları şu an 0/10 görsel, 10/10 ses**; commitlerde `[skip ci]` kullanılır ve GitHub Actions çalıştırılmaz.
