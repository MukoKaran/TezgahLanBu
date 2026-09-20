# BALDI'S BASICS NUMBER SLOP TEMPLATE

**Türkçe** | Matematik ekranı olmayan, hit text odaklı bir **Baldi's Basics** template'i. Arkadaşlarına dağıtıp kendi versiyonunu yapmaları için hazırlandı.

**English** | A **Baldi's Basics** template with no math minigame, focused on the hit text system. Share it with your friends so they can make their own version.

---

## Nasıl Oynanır / How to Play

**Türkçe**
- **Hareket:** WASD
- **Koşma:** Shift (enerji bitince koşamazsın)
- **Etkileşim / Defter Al:** E
- **Mouse:** Etrafa bakma
- **Amaç:** Okuldan kaçmak için 7 defteri topla.

**English**
- **Move:** WASD
- **Run:** Shift (stamina runs out, then you can't run)
- **Interact / Pick up notebook:** E
- **Mouse:** Look around
- **Goal:** Collect all 7 notebooks to escape the school.

---

## Bu Template'te Ne Var / What's In This Template

**Türkçe**
- **Hit Text Sistemi:** Defter alınca matematik ekranı yerine ekrana büyük yazı (ve isteğe bağlı PNG) açılır, sallanır ve fade out ile kapanır.
- **Baldi Sistemi:**
  - Baldi cetvelle çok hızlı ve çok sık vurur.
  - Baldi zamanla hızlanır (10 saniyede bir +5 hız).
  - Vuruş sesi uzaklığa göre değişir.
- **Chase Müziği:** Baldi kızınca chase müziği çalar.
- **Oyuncu Hız Çarpanı:** Oyuncu hızı çarpanla arttırılabilir.
- **Enerji İçeceği Modu YOK:** Dümdüz normal Baldi's Basics oyunu.

**English**
- **Hit Text System:** When you grab a notebook, instead of a math minigame, a big text (and optional PNG) appears on screen, shakes, and fades out.
- **Baldi System:**
  - Baldi slaps the ruler very fast and very often.
  - Baldi gets faster over time (+5 speed every 10 seconds).
  - The slap sound changes with distance.
- **Chase Music:** Chase music starts when Baldi gets angry.
- **Player Speed Multiplier:** Player speed can be boosted by a multiplier.
- **NO Energy Drink Mode:** Just a plain, normal Baldi's Basics game.

---

## Nasıl Kurulur / How to Set Up / Open

**Türkçe**
1. Bu klasörü Unity'de aç: **Unity Hub → Add → bu klasörü seç.**
2. Kullanılacak Unity sürümü: **2018.3.9f1**.
3. Proje açılınca **Assets → Scene → School** sahnesini aç.
4. **Play**'e bas.

**English**
1. Open this folder in Unity: **Unity Hub → Add → select this folder.**
2. Unity version required: **2018.3.9f1**.
3. Once opened, open the scene **Assets → Scene → School**.
4. Press **Play**.

---

## Özellik Ayarları / Feature Settings (Unity Inspector)

Sahnede **GameController** objesini seç / Select the **GameController** object in the scene to change:

| Ayar / Setting | Ne İşe Yarar / What it does | Varsayılan / Default |
|---|---|---|
| `Hit Text Message` | Defter alınınca görünecek yazı / Text shown when a notebook is grabbed | "you png/text here" |
| `Hit Image Sprite` | Yazının üstünde görünecek PNG (Sprite olarak import et) / PNG shown above the text (import as Sprite) | Boş (görünmez) / Empty (hidden) |
| `Hit Sound` | Hit text açılırken çalan ses / Sound played when the hit text opens | Otomatik BAL_Hi / Auto BAL_Hi |
| `Hit Text Hold Time` | Yazının tam görünür kalma süresi / Time the text stays fully visible | 3 sn / sec |
| `Hit Text Fade Time` | Yazının kaybolma (fade out) süresi / Fade-out duration | 2.5 sn / sec |
| `Chase Music` | Baldi kızınca çalan müzik (boş = `Resources/Music/chase1.mp3`) / Music when Baldi gets angry (empty = `Resources/Music/chase1.mp3`) | Otomatik / Auto |
| `Notebook Count Max` | Sayacın "/7" kısmındaki değer. Örn. 10 yaparsan "3/10 Notebooks" olur (final de 10 defterde başlar) / The value in the "/7" part of the counter. E.g. 10 gives "3/10 Notebooks" (and the finale starts at 10 notebooks) | 7 |
| `Notebook Count Label` | Sayacın sonuna eklenen kelime. Örn. "Notebooks" yazarsan "3/7 Notebooks" olur / The word shown after the count. E.g. "Notebooks" gives "3/7 Notebooks" | "Notebooks" |

**Player** objesini seç / Select the **Player** object:

| Ayar / Setting | Ne İşe Yarar / What it does | Varsayılan / Default |
|---|---|---|
| `Player Speed Multiplier` | Yürüme ve koşma hızını çarpanla arttırır (2 = 2 kat hız) / Multiplies walk and run speed (2 = double speed) | 1.5 |

**Baldi** objesini seç / Select the **Baldi** object:

| Ayar / Setting | Ne İşe Yarar / What it does | Varsayılan / Default |
|---|---|---|
| `Speed` | Baldi'nin temel hızı / Baldi's base movement speed | 75 |
| `Base Time` | Baldi'nin ilk hareketine kadar geçen süre / Time until Baldi's first move | 3 sn / sec |
| `Slap Move Frames` | Cetvel hamlesi uzunluğu (düşür = hızlı hamle) / Ruler lunge duration (lower = faster lunge) | 10 |
| `Base Speed` | Baldi'nin başlangıç hızı (0 ise 150 yapılır) / Baldi's starting speed (0 = set to 150) | 0 |

---

## Nasıl Düzenlenir / How to Edit / Customize

Kod bilmeden neredeyse her şeyi değiştirebilirsin / Almost everything can be changed without touching code.

### 1. Hit text yazısını değiştir / Change the hit text message

**Türkçe:** **GameController → Hit Text Message** (Inspector). İstediğini yaz, örn. "you png/text here".
**English:** **GameController → Hit Text Message** (Inspector). Write anything, e.g. "you png/text here".

### 2. Hit text görseli (PNG) ekle / Change the hit text image (PNG)

**Türkçe / English:**
1. PNG'yi `Assets` klasörüne sürükle / Drag the PNG into the `Assets` folder.
2. PNG'yi seç → **Texture Type → Sprite (2D and UI)** → **Apply** / Select it → **Texture Type → Sprite (2D and UI)** → **Apply**.
3. **GameController → Hit Image Sprite** alanına sürükle / Drag it into **GameController → Hit Image Sprite**.

PNG yazının üstünde görünür, birlikte sallanır ve söner / The PNG shows above the text, shakes and fades out with it.

### 3. Hit sesini değiştir / Change the hit sound

**Türkçe:** **GameController → Hit Sound** alanına herhangi bir ses dosyası sürükle. Boş bırakılırsa sahnedeki `BAL_Hi` otomatik bulunur.
**English:** Drop any audio file into **GameController → Hit Sound**. If empty, it auto-finds `BAL_Hi` from the scene.

### 4. Hit text süresini ayarla / Make the hit text stay longer / shorter

**Türkçe:** **GameController → Hit Text Hold Time** (tam görünür kalma süresi) ve **Hit Text Fade Time** (sönme süresi).
**English:** **GameController → Hit Text Hold Time** (how long it stays fully visible) and **Hit Text Fade Time** (how long it fades out).

### 5. Baldi zorluğunu değiştir / Change Baldi's difficulty

**Türkçe:** **Baldi** objesini seç ve ayarla / Select **Baldi** and adjust:

- `Speed` / `Base Speed` — Baldi ne kadar hızlı yürür / how fast Baldi walks.
- `Base Time` — ilk hareketine kadar süre / seconds until his first move.
- `Slap Move Frames` — cetvel hamlesi hızı (düşük = daha keskin) / ruler lunge speed (lower = snappier).
- `baldiWait` — vuruşlar arası saniye (düşük = daha sinirli). Varsayılan `0.001` = neredeyse sürekli vurur / seconds between ruler slaps (lower = angrier). Default `0.001` = almost constant slapping.

**Türkçe:** Baldi otomatik hızlanır (+5 / 10 sn). Kapatmak için `Assets/Scripts/NPCFunctions/BaldiScript.cs` aç ve `Update()` içindeki `speedRampTimer` bloğunu sil.
**English:** Baldi automatically gets faster over time (+5 every 10 seconds). To disable that, open `Assets/Scripts/NPCFunctions/BaldiScript.cs` and delete the `speedRampTimer` block in `Update()`.

### 6. Chase müziğini değiştir / Change the chase music

**Türkçe:** **GameController → Chase Music** alanına kendi müziğini sürükle. Ya da `Assets/Resources/Music/chase1.mp3` dosyasını kendi dosyanla değiştir (adı aynı kalmalı).
**English:** Drop your own music into **GameController → Chase Music**. Or replace the file at `Assets/Resources/Music/chase1.mp3` (it must keep that name).

### 7. Oyuncu hızını ayarla / Make the player faster/slower

**Türkçe:** **Player → Player Speed Multiplier** (1.5 = 1.5x). Orijinal hız için 1 yap.
**English:** **Player → Player Speed Multiplier** (1.5 = 1.5x). Set to 1 for the original speed.

### 8. Baldi'nin kızma zamanını değiştir / Change when Baldi gets angry

**Türkçe / English:** `Assets/Scripts/PlayerFunctions/ItemFunctions/NotebookScript.cs` dosyasını aç / Open:

```csharp
if (gc.notebooks >= 2)
{
    gc.GetAngry(1f);
}
```

`gc.notebooks >= 2` = Baldi 2. defterden itibaren kızar. `2` yerine `3` (3. defterden) veya `1` (1. defterden) yazabilirsin. `1f` = her defterin eklediği sinir miktarı / `gc.notebooks >= 2` means Baldi gets angry from the 2nd notebook on. Change `2` to `3` (angry from 3rd) or to `1` (angry from the 1st). The `1f` is how much anger each notebook adds.

### 9. Otomatik hızlanmayı kapat / Turn off Baldi's automatic speed-up

**Türkçe / English:** `Assets/Scripts/NPCFunctions/BaldiScript.cs` → `Update()` içinde / find in `Update()`:

```csharp
speedRampTimer += Time.deltaTime;
if (speedRampTimer >= 10f)
{
    speedRampTimer = 0f;
    baseSpeed += 5f;
    speed = baseSpeed;
}
```

Sil — Baldi sabit hızda kalır / Delete those lines and Baldi keeps a constant speed.

### 10. Notebook sayacı yazısını değiştir / Change the notebook counter text

**Türkçe:** **GameController → Notebook Count Max** alanı "/7" kısmını (kaç defter gerektiği), **Notebook Count Label** alanı sonundaki kelimeyi değiştirir. Örn. Max=10, Label="Kitap" → "3/10 Kitap". Final de kaçıncı defterde başlayacağını değiştirir.
**English:** **GameController → Notebook Count Max** changes the "/7" part (how many notebooks you need), **Notebook Count Label** changes the word after it. E.g. Max=10, Label="Books" → "3/10 Books". It also changes which notebook starts the finale.

### 11. Kod dosyaları nerede / Where the code lives

| Dosya / File | Görevi / Purpose |
|---|---|
| `Assets/Scripts/Core/GameControllerScript.cs` | Hit text, chase müziği, ödüller (quarter, AllNotebooks) / Hit text, chase music, rewards |
| `Assets/Scripts/NPCFunctions/BaldiScript.cs` | Baldi hızı, vuruş, sesler / Baldi speed, slapping, sounds |
| `Assets/Scripts/PlayerFunctions/PlayerScript.cs` | Oyuncu hız çarpanı / Player speed multiplier |
| `Assets/Scripts/PlayerFunctions/ItemFunctions/NotebookScript.cs` | Defter alınınca ne olur / What happens when a notebook is grabbed |
| `Assets/Scripts/Core/UI/ShakingScript.cs` | Ekran/yazı sallanması / Screen/text shaking |
| `Assets/Scripts/NPCFunctions/PrincipalScript.cs` | Müdür davranışı ve gözaltı / Principal behavior and detention |
| `Assets/Scripts/NPCFunctions/PlaytimeScript.cs` | Playtime ve ip atlama oyunu / Playtime and the jump rope game |
| `Assets/Scripts/NPCFunctions/SweepScript.cs` | Gotta Sweep / Gotta Sweep |
| `Assets/Scripts/NPCFunctions/FirstPrizeScript.cs` | 1st Prize kovalama/sarılma / 1st Prize chase/hug |
| `Assets/Scripts/NPCFunctions/CraftersScript.cs` | Arts and Crafters kapı/eşya / Arts and Crafters doors/items |
| `Assets/Scripts/NPCFunctions/BullyScript.cs` | Bully eşya çalma / Bully item stealing |
| `Assets/Resources/Music/` | Chase müzik dosyaları / Chase music files |

> **İpucu / Tip:** Her değişiklikten sonra sahnede **Ctrl+S** yap. Sahnede Inspector'da görünen değerler, kod varsayılanlarını ezer; kod değiştirdiysen Inspector'daki değerleri de sıfırlaman gerekebilir / After any change, always **Ctrl+S** the scene in Unity. Inspector values in the scene override code defaults, so if you change code defaults you may also need to reset the values in the Inspector.

---

## Sorun Giderme / Troubleshooting

| Sorun / Problem | Çözüm / Fix |
|---|---|
| Baldi hareket etmiyor / vurmuyor / Baldi doesn't move or slap | Baldi objesinde `Base Time` düşük (örn. 3) ve `baldiWait` düşük (örn. 0.001) olsun / Make sure `Base Time` is low (e.g. 3) and `baldiWait` is low (e.g. 0.001). |
| Vuruş sesi yok / No slap sound | Baldi objesinde `Slap` alanına `BAL_Slap` atanmış mı kontrol et / Check `Slap` on the Baldi object has `BAL_Slap` assigned. |
| Chase müziği çalmıyor / No chase music | `Resources/Music/chase1.mp3` var mı bak / Make sure `Resources/Music/chase1.mp3` exists. |
| Hit text görünmüyor / Hit text doesn't appear | HUD Canvas altında "Hit-Text" objesi var mı ve `Hit Text Message` boş değil mi kontrol et / Check the "Hit-Text" object exists under the HUD Canvas, and that `Hit Text Message` is not empty. |
| PNG görünmüyor / PNG doesn't show | **Sprite (2D and UI)** olarak import edilip `Hit Image Sprite`'a atanmalı / Make sure it's imported as **Sprite (2D and UI)** and assigned to `Hit Image Sprite`. |
| Oyun başlamıyor / Game doesn't start | **School** sahnesinden Play'e bas (başka sahnede test etme) / Open the **School** scene and press Play (never test from another scene). |
| Her şey çok hızlı / Everything looks too fast | Player objesinde `Player Speed Multiplier` değerini 1 yap / Lower `Player Speed Multiplier` on the Player object to 1. |

---

## Sık Sorulan Sorular / FAQ

**Kendi versiyonumu yapmak için kod bilmem şart mı? / Do I need to touch code to make my own version?**
Hayır. Neredeyse her şey (yazı, görsel, sesler, süreler, hız) Inspector'dan ayarlanabilir / No. Almost everything (text, image, sounds, timings, speed) is adjustable from the Inspector.

**Kendi müziğimi koyabilir miyim? / Can I put my own music?**
Evet. **GameController → Chase Music** alanına ses sürükle, ya da `Resources/Music/chase1.mp3` dosyasını değiştir (adı aynı kalsın) / Yes. Either drop a clip into **GameController → Chase Music**, or replace `Resources/Music/chase1.mp3` with your own file (keep the name).

**Hit text'i kaldırıp matematik oyununu geri getirebilir miyim? / Can I remove the hit text and bring back the math minigame?**
Evet. `Assets/Scripts/PlayerFunctions/ItemFunctions/NotebookScript.cs` içinde / In that file, delete the lines:

```csharp
gc.ShowHitText();
```

ve öğrenme oyunu kısmını geri getir. `MathGameScript.cs` projede duruyor / and restore the learning game part. The math minigame scripts are still in the project.

**Baldi neden bu kadar agresif? / Why is Baldi so aggressive?**
`baldiWait` `GetAngry()` içinde `0.001` yapılıyor (BaldiScript.cs), bu da neredeyse sürekli vurmasını sağlar. Daha sakin bir Baldi için `1f` veya `2f` yap / `baldiWait` is set to `0.001` in `GetAngry()` (inside `BaldiScript.cs`), which makes him slap almost constantly. Raise it to `1f` or `2f` for a calmer Baldi.

**Hit text fontunu / rengini değiştirebilir miyim? / Can I change the hit text font/color?**
Evet. HUD Canvas altındaki "Hit-Text" objesini seç, TMP bileşeninden font/size/renk/outline ayarla — normal bir UI yazısı gibi / Yes. Select the "Hit-Text" object under the HUD Canvas and edit its TMP text component (font, size, color, outline) — just like any other UI text.

---

## Kendi Oyununu Yap (Build / .exe) / Build Your Own Copy

**Türkçe / English:**
1. **School** sahnesini aç / Open the **School** scene.
2. **File → Build Settings**.
3. **School** sahnesini build listesine ekle (yoksa) / Add the **School** scene to the build list (if it's not already there).
4. **PC, Mac & Linux Standalone → Windows** seç / Pick **PC, Mac & Linux Standalone → Windows**.
5. **Build**'e bas ve klasör seç / Click **Build** and choose a folder.
6. Oluşan klasörü arkadaşlarına paylaş / Share the built folder with your friends.

> **Opsiyonel / Optional:** **Player Settings**'ten oyun adını ve ikonunu değiştirebilirsin / In **Player Settings** you can change the game name and icon.

---

## Denemek İçin Fikirler / Ideas to Try

**Türkçe**
- Hit PNG'sini bir meme veya kendi çiziminle değiştir.
- Chase müziğini sevdiğin bir parçayla değiştir.
- Kolay mod için oyuncuyu süper hızlı, Baldi'yi çok yavaş yap.
- Zor mod için Baldi'yi 1. defterden kızdır.
- Her defter seviyesi için farklı hit text mesajı yaz.

**English**
- Replace the hit PNG with a meme or your own drawing.
- Change the chase music to something you like.
- Make the player super fast and Baldi super slow for an easy mode.
- Make Baldi get angry from the 1st notebook for a hard mode.
- Change the hit text message for each level of notebooks.

---

## Sahne Objeleri Rehberi / Scene Objects Guide

**School** sahnesindeki ana objeler / The main things in the **School** scene:

| Obje / Object | Ne İşe Yarar / What it is |
|---|---|
| `GameController` | Oyunun beyni — tüm ayarları tutar (hit text, chase müzik, ödüller) / The brain — holds all settings. |
| `Player` | Sensin. `PlayerScript` (hareket + hız çarpanı) ve kamera bunda / You. Has movement + speed multiplier and the camera. |
| `Baldi` | Ana düşman. Yürür, sesleri duyar, cetvelle vurur / The main enemy. Walks, hears sounds, slaps with a ruler. |
| `Principal of the Thing` | Kuralları çiğneyince (koşma, içme vb.) seni gözaltına alır / Catches you breaking rules and sends you to detention. |
| `Playtime` | Çok yaklaşırsan ip atlama mini oyunu başlatır / Jump rope minigame if you get too close. |
| `Gotta Sweep` | Değerse seni koridorda süpürür / Sweeps you around the hall if it touches you. |
| `1st Prize` | Seni kovalayıp sarılır ve sürükler / Chases and hugs you, dragging you along. |
| `Arts and Crafters` | Eşya vermedikçe kapıları kapatır / Blocks doors until you give it items. |
| `Bully` | Yanından geçerken eşyanı alır / Takes your item when you walk past it. |
| `Notebook` / `Notebooks (...)` | Kaçmak için toplaman gereken 7 defter / The 7 collectibles you need to escape. |
| `Pickup_Quarter` | 1. defterden sonra aldığın çeyreklik ödülü / The quarter reward you get after the 1st notebook. |
| `Hud` | Arayüz (Canvas) — `Hit-Text` objesini içerir / The UI overlay (Canvas) — contains the `Hit-Text` object. |
| `Hit-Text` | Defter alınca çıkan yazı (font/renk burada düzenlenir) / The text that appears when you grab a notebook (edit font/color here). |

> Unity **Hierarchy** (sol üst) penceresinde herhangi bir objeye tıklayıp, sağdaki **Inspector**'dan bileşenlerini görebilir ve değiştirebilirsin / In the Unity Hierarchy (top-left window) you can click any object, then see and change its components in the Inspector on the right.

---

## Hit Text Gradyanı / Hit Text Gradient

**Türkçe:** Hit-Text yazısına renk geçişi (gradyan) eklemek için kod gerekmez:

1. HUD Canvas altındaki **Hit-Text** objesini seç (Hierarchy'de).
2. TMP bileşeninde **Color Gradient** panelini genişlet.
3. **Top Left / Top Right / Bottom Left / Bottom Right** renklerini ayarla.
4. Örnek: siyah-beyaz yapmak için üst iki köşeyi beyaz, alt iki köşeyi siyah yap.

**English:** No code needed to add a color gradient to the hit text:

1. Select the **Hit-Text** object under the HUD Canvas (in the Hierarchy).
2. In the TMP component, expand the **Color Gradient** panel.
3. Set the **Top Left / Top Right / Bottom Left / Bottom Right** colors.
4. Example: to make it black-and-white, set the top two corners white and the bottom two corners black.

> **Not / Note:** Gradyan, TMP objesinin kendisine uygulanır — kodla `hitText.text` değişse bile gradyan korunur / The gradient is applied to the TMP object itself — it stays even when `hitText.text` changes in code.

---

## Kontroller Nasıl Değiştirilir / How to Change the Controls

**Türkçe:** Kontroller kodda değil, `ProjectSettings/InputManager.asset` içinde saklı.
**English:** Controls are stored in `ProjectSettings/InputManager.asset`, not in code.

1. Unity'de / In Unity: **Edit → Project Settings → Input**.
2. Değiştirmek istediğin ekseni bul: `Forward` (W/S), `Strafe` (A/D), `Mouse X` (bakma), `Run` (Shift), `Interact` (E) / Find the axis you want to change, e.g. `Forward` (W/S), `Strafe` (A/D), `Mouse X` (look), `Run` (Shift), `Interact` (E).
3. **Positive Button** / **Negative Button** alanlarını kendi tuşlarınla değiştir / Change the **Positive Button** / **Negative Button** fields to your keys.
4. Pencereyi kapat — değişiklikler otomatik kaydedilir / Close the window — changes save automatically.

**Örnekler / Examples:**
- `E` (Etkileşim) → `F` yapmak: `Interact` ekseninde **Positive Button** → `f` / Make `E` (Interact) into `F`: in the `Interact` axis, set **Positive Button** to `f`.
- Shift (Koşma) → Ctrl yapmak: `Run` ekseninde **Positive Button** → `left ctrl` / Make Shift (Run) into Ctrl: in the `Run` axis, set **Positive Button** to `left ctrl`.

---

## Defterler Nerede / Where the Notebooks Are

**Türkçe:** Toplaman gereken **7 defter** var (bazı modlarda tekrar doğarlar). Okulun her yerine dağılmışlar / There are **7 notebooks** to collect (they also respawn in some modes).

- Her ana odada bir tane: sınıflar, kütüphane, kafeterya, koridorlar / One per major room: classrooms, library, cafeteria, hallways.
- Harita bir döngü, bir kez tüm koridorları yürü — parladıklarını görürsün / The map is a loop, so just walk every hallway once — you'll see them glowing.
- 7 defteri toplayınca çıkış kapıları açılır. Dikkat: Baldi 2. defterden itibaren kızar / After collecting all 7, the exit doors open. Watch out — Baldi gets angry from notebook 2 on.

> **İpucu / Tip:** Defterler Hierarchy'de `Notebook`, `Notebooks (1)` ... `(18)` diye adlandırılıyor. Kendi düzenin için istediğin yere taşıyabilirsin / The notebooks are named `Notebook`, `Notebooks (1)` ... `(18)` in the Hierarchy. You can move them anywhere you want for your own layout.

---

## Zorluk Ön-Ayarları / Difficulty Presets

Zorluğu değiştirmek için Inspector'da bu değerleri ayarla / Set these values in the Inspector to change the challenge:

**Kolay Mod / Easy Mode**
| Ayar / Setting | Değer / Value |
|---|---|
| Player → `Player Speed Multiplier` | 2 |
| Baldi → `Speed` / `Base Speed` | 40 |
| Baldi → `baldiWait` | 2 |
| Baldi → `Slap Move Frames` | 20 |

**Normal Mod (varsayılan) / Normal Mode (default)**
| Ayar / Setting | Değer / Value |
|---|---|
| Player → `Player Speed Multiplier` | 1.5 |
| Baldi → `Speed` | 75 |
| Baldi → `baldiWait` | 0.001 |
| Baldi → `Slap Move Frames` | 10 |

**Zor Mod / Hard Mode**
| Ayar / Setting | Değer / Value |
|---|---|
| Player → `Player Speed Multiplier` | 1 |
| Baldi → `Speed` / `Base Speed` | 150 |
| Baldi → `baldiWait` | 0.001 |
| Baldi → `Slap Move Frames` | 1 |

**Ekstra Zor / Extra Hard:** `NotebookScript.cs` içinde `gc.notebooks >= 2` → `gc.notebooks >= 1` yap / Also change `NotebookScript.cs` from `gc.notebooks >= 2` to `gc.notebooks >= 1`.

---

## NPC Rehberi / NPC Guide

| NPC | Davranışı / Behavior | Nasıl Kaçınırım / How to avoid |
|---|---|---|
| **Baldi** | Seslere doğru yürür, cetvelle vurur. Zamanla hızlanır / Walks toward noises, slaps with ruler. Gets faster over time. | Ses çıkarma, görünme, Anti-Hearing Tape kullan / Don't make noise, stay out of sight, use Anti-Hearing Tape. |
| **Principal of the Thing** | Kuralları çiğneyince (koridorda koşma, yeme, içme, bıçaklama yok vb.) gözaltına alır / Sends you to detention for breaking rules. | Yanında yürü, kurallara uy / Walk instead of run near it, follow the rules. |
| **Playtime** | Yakalarsa ip atlama oyunu oynatır / Forces a jump rope game if she catches you. | Onun bölgesinden geçme / Don't walk past her area. |
| **Gotta Sweep** | Seni yerde süpürür ve enerji harcatır / Sweeps you along the floor and drains stamina. | Yolundan uzak dur / Stay away from its path. |
| **1st Prize** | Kovalamaya başlar, sarılıp sürükler / Chases and hugs you, dragging you. | Köşelerin arkasına saklan — iyi dönemez / Hide behind corners — it can't turn well. |
| **Arts and Crafters** | Kapıları kapatır, eşya ister / Blocks doors and asks for items. | İsteyince eşya ver / Give it an item when asked. |
| **Bully** | Yanından geçince eşya alır / Takes an item when you walk past. | Ona gereksiz bir şey ver / Give it something you don't need. |

## NPC Ayar Rehberi / NPC Settings Guide

**Türkçe:** Her NPC'nin ayarları sahnede ilgili obje seçilip Inspector'da düzenlenir (script bölümü). Sahnedeki değerler kod varsayılanlarını ezer. Aşağıdaki değerler script'lerin (`.cs`) varsayılan davranışlarından derlendi.
**English:** Each NPC's settings are edited in the Inspector by selecting the object in the scene (its script section). Scene values override code defaults. The values below were compiled from the scripts' (`.cs`) default behavior.

### Principal of the Thing — `PrincipalScript.cs`

| Ayar / Setting | Ne İşe Yarar / What it does |
|---|---|
| `coolDown` | Yakaladıktan sonra tekrar oynayabilmesi için geçen süre / Delay before it can act again after catching you. |
| `timeSeenRuleBreak` | Kuralları 0.5 saniye görünce seni yakalar (düşür = daha katı) / Catches you after seeing a rule break for 0.5s (lower = stricter). |
| `playerDetentionPoint` / `principalDetentionPoint` | Senin ve müdürün gözaltı odasına ışınlanma noktaları / Where you and the principal teleport for detention. |
| `bully` / `bullySeen` | Bully'yi kovalar (kabadayılık cezası) / Chases the bully when it sees bullying. |
| `audNoRunning`, `audNoDrinking`, `audNoEating`, `audNoStabbing`, `audNoBullying`, `audNoFaculty`, `audNoLockers`, `audNoEscaping` | Kural ihlali uyarı sesleri / Rule-break warning sounds. |
| `aud_Whistle`, `aud_Delay` | Düdük ve tepki sesleri / Whistle and reaction sounds. |

### Playtime — `PlaytimeScript.cs`

| Ayar / Setting | Ne İşe Yarar / What it does |
|---|---|
| `playCool` | Oyun süresi (varsayılan 15 sn). Sonrası hayal kırıklığı / Jump-rope game length (default 15s), then she's disappointed. |
| `coolDown` | Oyun bittikten sonra bekleme süresi (1 sn) / Delay after a game ends (1s). |
| `animator` | İp atlama animasyonları / Jump-rope animations. |
| `aud_Instrcutions`, `aud_Oops`, `aud_LetsPlay`, `aud_Congrats`, `aud_ReadyGo`, `aud_Sad` | Oyun sırasındaki sesler / Sounds during the game. |

### Gotta Sweep — `SweepScript.cs`

| Ayar / Setting | Ne İşe Yarar / What it does |
|---|---|
| `coolDown` | Fırlayış sonrası bekleme (1 sn) / Cooldown after a sweep dash (1s). |
| `waitTime` | Tekrar görünme süresi (120–180 sn rastgele) / Time before it reappears (random 120–180s). |
| `wanders` | Aktif olmadan önce dolaşma sayısı / Wander count before it becomes active. |
| `aud_Sweep`, `aud_Intro` | Süpürme ve giriş sesleri / Sweep and intro sounds. |

### 1st Prize — `FirstPrizeScript.cs`

| Ayar / Setting | Ne İşe Yarar / What it does |
|---|---|
| `normSpeed` / `runSpeed` | Normal gezinme ve kovalama hızı / Normal and chase speeds. |
| `turnSpeed` | Dönüş hızı (düşük = köşelerde seni kaybeder) / Turn speed (lower = it loses you at corners). |
| `acceleration` | Kovalarken hızlanma oranı / How fast it accelerates while chasing. |
| `autoBrakeCool` | Otomatik fren arası / Auto-brake interval. |
| `crazyTime` | Seni kucakladıktan sonra hızlanma süresi / Speed-up duration after hugging you. |
| `audBang` | Sesi / Its sound. |

### Arts and Crafters — `CraftersScript.cs`

| Ayar / Setting | Ne İşe Yarar / What it does |
|---|---|
| `anger` / `gettingAngry` | Kapı kapatma/eşya isteme sinir seviyesi / Anger level for closing doors and asking for items. |
| `baldiTeleportPoint` / `playerTeleportPoint` | Eşya vermezsen Baldi ve senin ışınlanma noktaları / Where Baldi and you teleport if you refuse. |
| `sprite` | Görünürlük sprite'ı / Its visibility sprite. |
| `aud_Intro`, `aud_Loop` | Giriş ve döngü sesleri / Intro and loop sounds. |

### Bully — `BullyScript.cs`

| Ayar / Setting | Ne İşe Yarar / What it does |
|---|---|
| `waitTime` | Tekrar belirme süresi (60–120 sn) / Time before reappearing (60–120s). |
| `activeTime` | Aktif kaldığı süre / How long it stays active. |
| `guilt` | Bully'i müdüre yakalatma süresi (10 sn) / How long the bully stays "guilty" for the principal (10s). |
| `aud_Denied` | Eşyayı çalarkenki ses / Sound when it steals an item. |

---

## Eşya Rehberi / Item Guide

**Türkçe:** 3 eşya taşıyabilirsin. Seçmek için 1/2/3 tuşları, kullanmak için etkileşim tuşu.
**English:** You can carry 3 items. Press the number keys (1/2/3) to select, use with the interact key.

| Eşya / Item | Ne İşe Yarar / What it does |
|---|---|
| Energy flavored Zesty Bar | Enerji (stamina) doldurur / Restores stamina. |
| Yellow Door Lock | Arkanda kapıyı kilitler / Locks a door behind you. |
| Principal's Keys | Kapıları açar / Opens doors. |
| BSODA | Düşmanları yavaşlatır/sersemletir (Baldi dahil) / Slows or stuns enemies (including Baldi). |
| Quarter | Ödül eşyası / Reward item. |
| Baldi Anti Hearing and Disorienting Tape | Bir süreliğine Baldi'nin seni duymasını engeller / Stops Baldi from hearing you for a while. |
| Alarm Clock | Gürültüyle dikkat dağıtır / Creates a noise distraction. |
| WD-NoSquee (Door Type) | Kapıları sessizleştirir / Silences/quiets doors. |
| Safety Scissors | Bir şeyleri keser / belirli bulmacalarda kullanılır / Cuts away things / used for certain puzzles. |
| Big Ol' Boots | Gotta Sweep ve 1st Prize'dan korur / Protects from Gotta Sweep and 1st Prize. |
| Teleportation Teleporter | Seni güvenli bir yere ışınlar / Teleports you somewhere safe. |

---

## Ekran Görüntüleri / Screenshots

Buraya kendi ekran görüntülerini ekle — görselleri `Assets` klasörüne atıp editöründen README'ye yerleştir ya da bir siteye yükleyip linkleri aşağıya yapıştır / (Add your own screenshots here — drag images into the `Assets` folder, then insert them into this README in your editor, or upload them to a site and paste the links below.)

---

## Unity Temel Kılavuzu / Unity Basics (Quick Guide)

**Türkçe / English:** Unity'ye yeni misin? İşte düzenleme yapmak için bilmen gerekenler / New to Unity? Here's everything you need to make edits:

- **Hierarchy** (sol üst / top-left): sahnedeki objelerin listesi. Seçmek için tıkla / the list of objects in the scene. Click one to select it.
- **Scene view** (orta / center): 3D editör. Etrafa bakmak için sağ-tık basılı tut, yakınlaşmak için tekerleği çevir / the 3D editor. Hold right-click to look around, use the mouse wheel to zoom.
- **Game view** (orta, Play'e basınca / center, when pressed Play): oyuncunun gördüğü ekran / what the player actually sees.
- **Inspector** (sağ / right): seçili objenin bileşenleri ve değerleri. Çoğu şey burada düzenlenir / shows the selected object's components and values. This is where you edit most things.
- **Play / Pause / Stop** (üst orta / top-center): test etmeye başla/bırak. Play açıkken yapılan değişiklikler **kaydedilmez** — dururken yap / start and stop testing. Changes you make while Play is on are **not saved** — make them while stopped.
- **Project** (alt / bottom): dosyaların (script, ses, doku). `.cs` dosyaya çift tıkla, kod editöründe açılır / your files. Double-click a `.cs` script to open it in a code editor.
- Scene view'da obje taşımak için: seç → **Move tool** (W tuşu) → okları sürükle / To move an object: select it, then use the **Move tool** (W key) and drag the arrows.
- Obje kopyalamak için: Hierarchy'de sağ tık → **Duplicate** (Ctrl+D) / To duplicate an object: right-click → **Duplicate** (Ctrl+D).
- Boş obje eklemek için: sağ tık → **Create Empty** / To add an empty object: right-click → **Create Empty**.
- **Her zaman School sahnesinden test et** — başka sahneden değil / **Always test from the School scene** — press Play there, not from other scenes.

---

## PNG Nasıl Eklenir / How to Add a PNG

**Türkçe / English:**
1. PNG'yi `Assets` klasörüne sürükle / Drag the PNG into the `Assets` folder.
2. PNG'yi seç → Inspector → **Texture Type → Sprite (2D and UI)** → **Apply** / Select the PNG → Inspector → **Texture Type → Sprite (2D and UI)** → **Apply**.
3. **GameController → Hit Image Sprite** alanına sürükle / Drag it into **GameController → Hit Image Sprite**.

---

## Önemli Notlar / Important Notes

**Türkçe**
- **Inspector değişikliklerini kaydetmeyi unutma:** Değer değiştirdikten sonra **Ctrl+S** yap, yoksa oyun eski değerle başlar.
- Sahnede Inspector'da görünen değerler, kod varsayılanlarını ezer.
- Chase müziği `Resources/Music/` klasöründe; dosyanın adı `chase1` olmalı (kendi parçanı koyabilirsin).
- Hit text objesi sahnede zaten var; istersen sürekli görünebilir.

**English**
- **Remember to save Inspector changes:** Press **Ctrl+S** after changing values, otherwise the game starts with old values.
- Scene values (shown in Inspector) override code defaults.
- Chase music lives in `Resources/Music/`; the file must be named `chase1` (you can drop in your own track).
- The hit text object already exists in the scene; it can be always visible if you want.

---

## Oyun Kuralları / Game Rules (Standard BBiC)

**Türkçe**
- 7 defteri topla, çıkış kapılarından dışarı çık.
- 2. defterden itibaren Baldi sinirlenmeye başlar.
- 1. defterde çeyreklik (quarter) ödülü verilir.
- 7. defterde "All Notebooks" sesi çalar.

**English**
- Collect all 7 notebooks and go through the exit doors.
- Baldi starts getting angry from the 2nd notebook on.
- You get a quarter reward on the 1st notebook.
- The "All Notebooks" sound plays on the 7th notebook.

---

## Değişiklik Geçmişi / Changelog

**Türkçe**
- **Hit text sistemi** — defter alınca matematik yerine yazı + isteğe bağlı PNG + ses + sallanma + fade.
- **Baldi yeniden düzenlendi** — hızlı cetvel vuruşu, uzaklığa göre vuruş sesi, zamanla hızlanma.
- **Chase müziği** — Baldi kızınca müzik başlar.
- **Oyuncu hız çarpanı** — yeni Inspector ayarı.
- **Ödüller taşındı** — quarter (1. defter) ve AllNotebooks sesi (7. defter) matematik ekranı olmadan da çalışıyor.

**English**
- **Hit text system** — notebook grabs show text + optional PNG + sound + shake + fade instead of the math minigame.
- **Baldi rework** — fast ruler slapping, distance-based slap sound, time-based speed-up.
- **Chase music** — music starts when Baldi gets angry.
- **Player speed multiplier** — new Inspector setting.
- **Rewards moved** — quarter (1st notebook) and AllNotebooks sound (7th notebook) still work without the math minigame.

---

İyi eğlenceler! / Have fun!
