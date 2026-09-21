#if UNITY_EDITOR
using TMPro;
using UnityEditor;
using UnityEngine;

namespace TezgahLanBu.EditorTools
{
    /// <summary>
    /// Unity Cloud Build ortaminda (ozellikle temiz/fresh checkout sonrasi tam
    /// asset reimport gerektigi durumlarda) TextMeshPro'nun "TMP Settings"
    /// kaynagina ilk erisimi, asset veritabani importu tam bitmeden gerceklesebiliyor.
    ///
    /// Bu durumda TMP, essentials'in eksik oldugunu sanip ilk kurulum penceresini
    /// (TMP_PackageResourceImporterWindow) -batchmode altinda acmaya calisiyor.
    /// Bu pencere icin bir GPU swap chain olusturulmaya calisiliyor, ki bu
    /// Unity Cloud Build'in ekransiz/headless build makinesinde basarisiz olup
    /// "d3d12: Unrecoverable GPU device error" ile build'i tamamen cokertiyor.
    ///
    /// Bu script, Editor yuklendigi anda (ve ozellikle -batchmode calistirmalarda)
    /// TMP Settings'i erkenden zorla yukleyip cache'leyerek bu yaris durumunun
    /// (race condition) tetiklenme ihtimalini azaltir. Essentials zaten
    /// Assets/TextMesh Pro/Resources altinda mevcut oldugu icin bu sadece
    /// erisim zamanlamasini erkene cekiyor, yeni bir davranis eklemiyor.
    /// </summary>
    [InitializeOnLoad]
    public static class TMPCloudBuildFix
    {
        static TMPCloudBuildFix()
        {
            // Sadece CI / -batchmode build ortaminda calis; normal Editor
            // kullanimini (interaktif calisirken) hicbir sekilde etkilemez.
            if (!Application.isBatchMode)
                return;

            var settings = Resources.Load<TMP_Settings>("TMP Settings");

            if (settings == null)
            {
                Debug.LogWarning(
                    "[TMPCloudBuildFix] 'TMP Settings' bulunamadi. " +
                    "TextMesh Pro essentials (Assets/TextMesh Pro/Resources) " +
                    "eksik veya yanlis konumda olabilir.");
            }
        }
    }
}
#endif
