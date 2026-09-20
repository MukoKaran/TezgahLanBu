# Tezgah Lan Bu! — Unity 6000.6 ve Mobil Kontrol Tasarımı

## Amaç

`baldis_basics_number_slop_template.zip` içindeki Unity 2018.3.9f1 projesini, oyun adı `Tezgah Lan Bu!` olacak biçimde Unity 6000.6.2f1'e taşımak ve `mobilecontrollfolder.rar` içindeki mobil kontrol sisteminin tamamını projeye eklemek.

## Başarı ölçütleri

- `ProjectVersion.txt` Unity 6000.6.2f1'i hedefler.
- Player Settings içindeki ürün adı `Tezgah Lan Bu!` olur.
- Control Freak 2 paketindeki 176 varlığın tamamı, özgün GUID ve `.meta` dosyaları korunarak aktarılır.
- Android'de joystick ile hareket, sağ dokunmatik alanla yatay bakış, koşma, etkileşim, duraklatma, arkaya bakma ve üç eşya yuvası kullanılabilir.
- Mobilde seçili eşyanın kullanılabilmesi için erişilebilir bir kullanım düğmesi bulunur.
- Masaüstü klavye ve fare girişleri çalışmayı sürdürür.
- `School` ve `TestRoom` sahnelerinde mobil kontrol prefabı doğrudan bağlıdır; çalışma anında `Resources.Load` ile görsel/prefab değiştirilmez.

## Sürüm geçişi

Proje hedefi resmi Unity 6000.6.2f1 sürümüdür. `ProjectVersion.txt`, paket manifesti ve Unity 6'nın artık kabul etmediği eski proje ayarları uyarlanır. Üretilmiş `Library`, `Temp`, IDE proje dosyaları ve kullanıcıya özel önbellekler teslim paketinden çıkarılır; Unity 6000.6.2f1 bunları ilk açılışta yeniden üretir.

Geçiş sırasında sahnelerin büyük ölçekte yeniden serileştirilmesi yapılmaz. Yalnız gereken prefab örnekleri ve bağlantılar YAML'a eklenir. Bu, Unity editörü bulunmayan ortamda gereksiz sahne farklarını ve referans kaybını azaltır.

## Mobil kontrol mimarisi

Verilen paket bütünüyle içe aktarılır. Paket; Control Freak 2 çalışma ve editör kodlarını, örnekleri, debug yardımcılarını, kontrol prefablarını ve görselleri içerir. Kullanıcının seçimi gereği bunların hiçbiri kapsam nedeniyle ayıklanmaz.

`CF2-Rig.prefab` şu girişleri üretir:

- `Strafe` ve `Forward`: sol joystick
- `Mouse X`: sağ dokunmatik bakış alanı
- `Run`: koşma düğmesi
- `Fire1`: etkileşim düğmesi
- `Pause`: duraklatma düğmesi
- `Look Behind`: arkaya bakma düğmesi
- `Alpha1`, `Alpha2`, `Alpha3`: eşya yuvası düğmeleri

Mevcut oyun kodunun çoğu özel `InputManager` üzerinden klavye tuşu okuduğu için yalnız prefab eklemek yeterli değildir. `InputManager`, Control Freak girişlerini mevcut masaüstü eşlemeleriyle birleştirecek şekilde genişletilir. Oyuncu hareketi joystick değerlerini analog olarak kullanır; klavye hareketi önceki davranışını korur. Kamera yatay dönüşü `CF2Input.GetAxis("Mouse X")` üzerinden okunur ve masaüstünde otomatik olarak Unity girişine düşer.

Eşya kullanımı için sağ tarafta, verilen paketin görsel diline uygun bir `Use Item` dokunmatik düğmesi eklenir ve `UseItem` eylemine bağlanır. Etkileşim düğmesi yalnız `Interact` eylemini tetikler; böylece kapı açarken eşya yanlışlıkla kullanılmaz.

## Sahne ve görünürlük davranışı

Mobil rig doğrudan `School` ve `TestRoom` sahnelerine prefab örneği olarak eklenir. Kontrol paneli Android/iOS veya editörde zorlanmış mobil modda görünür; masaüstünde gizli kalır. Var olan UI üstünde doğru çizilmesi için paketteki yüksek canvas sırası korunur.

Duraklatma ve öğrenme ekranlarında oyun giriş kilitleri mevcut `GameControllerScript` akışına uyar. Mobil kontroller, masaüstü girdisini devre dışı bırakmaz.

## Proje kimliği

- Ürün adı: `Tezgah Lan Bu!`
- Proje klasörü ve teslim arşivi: `TezgahLanBu`
- Android paket kimliği mevcut projede tanımlı değilse güvenli varsayılan olarak `com.mukokaran.tezgahlanbu` kullanılır.
- Ekran yönü mevcut yatay kullanım korunarak yataya sabitlenir.

## Hata yönetimi ve uyumluluk

Tam paket aktarımı, Control Freak 2 örnek/editör kodları nedeniyle temiz entegrasyona göre daha yüksek Unity 6 derleme riski taşır. Unity 6 tarafından kaldırılmış API bulunursa davranışı değiştirmeyen en küçük uyumluluk düzeltmesi yapılır; üçüncü taraf kodun kapsam dışı yeniden yazımı yapılmaz.

GUID çakışması veya aynı yola yazma durumunda, projenin mevcut oyun varlıkları korunur ve mobil paketin bağımlı referansları kırılmayacak şekilde çakışma tek tek çözülür.

## Doğrulama

- Unity paketindeki her `pathname`, `asset` ve `asset.meta` çifti sayılır ve hedefte doğrulanır.
- Prefabın başvurduğu script ve görsel GUID'lerinin hedefte bulunduğu kontrol edilir.
- Sahne prefab bağlantıları ve root nesne listeleri YAML düzeyinde doğrulanır.
- C# kaynaklarında eski/çıkarılmış Unity API'leri taranır.
- Ürün adı, sürüm, Android kimliği, yön ve giriş adları otomatik kontrollerle doğrulanır.
- Teslim ZIP'i listelenerek `Library`, `Temp`, `.git` ve IDE önbelleklerinin bulunmadığı doğrulanır.

Bu çalışma ortamında Unity editörü kurulu olmadığından gerçek asset importu, sahne açılışı ve Android derlemesi burada çalıştırılamaz. Son kabul testi Unity 6000.6.2f1 veya aynı sürümü kullanan Unity Build Automation üzerinde yapılmalıdır.
