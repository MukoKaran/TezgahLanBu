# Tezgah Lan Bu! — source validation and opening the project

Target editor: **Unity 6000.6.2f1**. This is a Unity source project, not an APK or Windows executable.

## Static verification

Run either command from the project root (Python 3, standard library only):

```sh
python3 -m unittest discover -s Tools/Validation -v
python3 -m unittest discover -v
```

Both commands execute 35 tests. A discovery guard rejects an empty test suite.
Coverage includes exact editor/product/Android identity; retained built-in modules;
full 176-entry mobile package presence; unique project GUID ownership; rig script,
local fileID and asset references; direct School/TestRoom rig instances; action
bindings; analog clamping and no-rig fallback; independent item-use hit area;
pause-menu rendering/resume wiring; a targeted Control Freak removed-API scan;
duplicate class declarations; all 45 installer-defined raw hardware axes with
exact indices and settings; active CF2 hardware-read dependencies; TestRoom's
shared input bridge and EventSystem graph; action-key rebinding isolation; and
delivery exclusions.

These are source/serialization checks, **not Unity runtime tests or compilation**.
The conditional scanner only covers the boolean directives present in this source,
using Unity 6 Android player and editor symbol profiles. It is not a C# compiler.

## Findings and remaining checks

- The Control Freak API scan found old `Screen.lockCursor` and editor callback APIs
  only in inactive pre-Unity-5/pre-2018 branches. The active Unity 6 branches use
  their modern replacements. No speculative package source changes were made.
- Deprecated-but-still-available APIs, including `FindObjectOfType`,
  `FindObjectsOfType` and scripting-define-symbol group accessors, remain unchanged.
  Warnings and actual compilation must be checked in the editor.
- School retains 28 legacy UnityEngine.UI DLL script references with GUID
  `f70555f144d8491a825f0804e09c671c`. These are external Unity UI components, not
  missing user scripts. Their migration to UGUI package scripts must be verified
  during the first editor import. TextMeshProUGUI references are package-owned too.
- TestRoom now uses the same EventSystem/StandaloneInputModule components as
  School, copied with unique scene fileIDs and valid local references. These two
  legacy UI component references also require first-import UGUI migration checks.
  Its PlayerMovement now consumes the shared keyboard/touch bridge, with a
  sensitivity default for opening the sandbox directly without saved settings.
- The 45 Control Freak raw hardware axes are committed in InputManager.asset
  using the package installer's definitions (including zero-based serialized
  indices). Cloud/headless imports no longer need its interactive setup prompt.
  Existing game axes are preserved. Run, Look Behind and Pause touch axes no
  longer duplicate hard-coded physical keys or synthesize keys for other actions;
  the game's configurable keyboard mappings remain responsible for physical input.
- **One genuine missing mesh is inherited from the provided template.** School's
  `Seat` GameObject (fileID `2268`) has MeshFilter `15368` referencing missing mesh
  GUID `4d7c1677b1627914cbcfa55acd72889a`. The original source commit has the same
  reference. No matching asset or second Seat prefab exists, so the reference was
  preserved rather than replaced with guessed geometry. The regression check
  allows only this exact scene/document/GUID exception; new missing refs fail.
  Inspect that seat in Unity and supply its original mesh to restore it faithfully.
- Unity 6000.6.2f1 editor import, script compilation, Android build and device play
  testing **were not run** because no Unity editor is installed in this environment.

Open the root folder in the target editor, allow package resolution/API migration,
then check Console errors and missing scripts. In School, test walking at partial
joystick deflection, turning, interaction, item use, slots 1/2/3, run, look behind,
pause/resume and switching between keyboard/mouse and touch. Build and test on an
Android phone in landscape; verify menu and notebook interactions on the device.

## Delivery contents

The ZIP has one `TezgahLanBu/` root and includes only tracked source, project
settings, package manifest, validation tools and documentation. It excludes Git
internals, worktrees, agent scratch reports, Library/Temp/Logs/obj/bin, IDE files,
Python caches and nested ZIPs. Archive integrity and entry names are checked
independently after creation.
