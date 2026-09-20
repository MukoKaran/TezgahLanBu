# Tezgah Lan Bu! Mobile Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the supplied Number Slop template to a clean Unity 6000.6.2f1 project named `Tezgah Lan Bu!` and integrate every asset from the supplied Control Freak 2 mobile-control package.

**Architecture:** Preserve the existing legacy Input Manager and desktop controls, then route touch state from Control Freak 2 through the project's existing `InputManager`. Import the Unity package with original paths and GUIDs, place the rig prefab directly in playable scenes, and validate the project with deterministic Python tests because the Unity editor is unavailable in this environment.

**Tech Stack:** Unity 6000.6.2f1, C#, legacy Unity Input Manager, Control Freak 2, YAML scene/prefab assets, Python 3 `unittest` validation.

**Spec:** `docs/superpowers/specs/2026-09-19-tezgah-lan-bu-mobile-design.md`

## Global Constraints

- Target editor is exactly Unity `6000.6.2f1`.
- Product name is exactly `Tezgah Lan Bu!`.
- Android application identifier is `com.mukokaran.tezgahlanbu` when the source has no explicit identifier.
- Preserve desktop keyboard/mouse behavior while enabling Android touch controls.
- Import all 176 Unity-package entries, including Control Freak 2 samples, debug tools, and editor files, because the user selected full-package import.
- Keep direct scene/prefab references; do not load or swap the mobile-control visuals with `Resources.Load` at runtime.
- Exclude generated `Library`, `Temp`, `.git`, IDE caches, and generated project files from the delivery ZIP.

## Review Focus

- The mobile rig exists but its panel is inactive: gameplay must activate it only in mobile mode without hiding desktop input.
- Touch joystick and keyboard are pressed together: the resulting movement must clamp to magnitude 1 rather than increase speed diagonally.
- Pause is held across frames: `PauseOrCancel` must fire once on the down edge and not rapidly toggle.
- Interaction and item use are distinct: tapping interaction must never consume the selected item.
- Scene and prefab GUID references survive archive creation: every referenced mobile script, sprite, and prefab GUID must resolve.

---

### Task 1: Establish the Unity project and validation harness

**Files:**
- Import: `Assets/**`, `Packages/**`, `ProjectSettings/**` from `baldis_basics_number_slop_template.zip`
- Create: `.gitignore`
- Create: `Tools/Validation/test_project.py`
- Preserve: `docs/superpowers/specs/2026-09-19-tezgah-lan-bu-mobile-design.md`

**Interfaces:**
- Consumes: uploaded ZIP at `/workspace/scratch/d4bbd1e2fbab/upload/baldis_basics_number_slop_template.zip`.
- Produces: `project_root() -> pathlib.Path` and reusable validation helpers `read(path) -> str`, `asset_guid(path) -> str`, and `all_guids() -> set[str]`.

- [ ] **Step 1: Write baseline tests that describe a distributable Unity project**

Create `Tools/Validation/test_project.py` with `unittest.TestCase` tests asserting that `Assets`, `Packages`, and `ProjectSettings` exist; generated `Library` and `Temp` do not exist; and `ProjectSettings/ProjectVersion.txt` is readable. Add helpers using only `pathlib`, `re`, and `unittest`.

```python
ROOT = Path(__file__).resolve().parents[2]

def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")

class ProjectLayoutTests(unittest.TestCase):
    def test_unity_project_layout_exists(self):
        for name in ("Assets", "Packages", "ProjectSettings"):
            self.assertTrue((ROOT / name).is_dir(), name)

    def test_generated_directories_are_excluded(self):
        for name in ("Library", "Temp", "Logs", "obj"):
            self.assertFalse((ROOT / name).exists(), name)
```

- [ ] **Step 2: Run the tests and verify they fail before source import**

Run: `python3 -m unittest Tools.Validation.test_project -v`

Expected: FAIL because `Assets`, `Packages`, and `ProjectSettings` are absent.

- [ ] **Step 3: Import only authoritative project sources**

Extract the uploaded ZIP to a temporary directory, copy `Assets`, `Packages`, `ProjectSettings`, `.vsconfig`, and other source-level root files into the repository, and intentionally omit `Library`, generated `.csproj` files, `.vscode`, and editor caches. Add a `.gitignore` covering `Library/`, `Temp/`, `Logs/`, `obj/`, `.vs/`, `.vscode/`, `*.csproj`, and `*.sln`.

- [ ] **Step 4: Run layout tests**

Run: `python3 -m unittest Tools.Validation.test_project.ProjectLayoutTests -v`

Expected: PASS.

- [ ] **Step 5: Commit the source baseline**

```bash
git add .gitignore Assets Packages ProjectSettings Tools docs
git commit -m "chore: import Number Slop Unity source"
```

### Task 2: Migrate project metadata to Unity 6000.6.2f1

**Files:**
- Modify: `ProjectSettings/ProjectVersion.txt`
- Modify: `ProjectSettings/ProjectSettings.asset`
- Modify: `Packages/manifest.json`
- Modify: `Tools/Validation/test_project.py`

**Interfaces:**
- Consumes: project layout from Task 1.
- Produces: Unity 6000.6.2f1 metadata with `Tezgah Lan Bu!`, landscape Android settings, and a valid package manifest.

- [ ] **Step 1: Add failing metadata tests**

Add assertions for exact editor version, product name, bundle identifier, landscape orientation, and JSON parsing:

```python
def test_editor_version_and_product_identity(self):
    self.assertIn("m_EditorVersion: 6000.6.2f1", read("ProjectSettings/ProjectVersion.txt"))
    settings = read("ProjectSettings/ProjectSettings.asset")
    self.assertIn("productName: Tezgah Lan Bu!", settings)
    self.assertRegex(settings, r"applicationIdentifier:\s*\n\s*Android: com\.mukokaran\.tezgahlanbu")

def test_manifest_is_valid_json(self):
    manifest = json.loads(read("Packages/manifest.json"))
    self.assertEqual("2.0.0", manifest["dependencies"]["com.unity.ugui"])
```

- [ ] **Step 2: Run metadata tests and confirm failure**

Run: `python3 -m unittest Tools.Validation.test_project.ProjectMetadataTests -v`

Expected: FAIL showing Unity `2018.3.9f1` and product `Baldi's Basics Classic`.

- [ ] **Step 3: Apply the minimal Unity 6 metadata migration**

Set `m_EditorVersion: 6000.6.2f1`; change `productName`; replace the empty application identifier map with the Android identifier; keep landscape orientation; remove the obsolete analytics, package-manager-ui, and standalone TextMesh Pro dependencies; add `com.unity.ugui` version `2.0.0`, which supplies Unity UI and TextMesh Pro in Unity 6; retain the existing built-in modules. Do not bulk reserialize scenes.

- [ ] **Step 4: Run metadata and complete baseline tests**

Run: `python3 -m unittest Tools.Validation.test_project -v`

Expected: PASS.

- [ ] **Step 5: Commit metadata migration**

```bash
git add ProjectSettings/ProjectVersion.txt ProjectSettings/ProjectSettings.asset Packages/manifest.json Tools/Validation/test_project.py
git commit -m "chore: migrate project metadata to Unity 6000.6"
```

### Task 3: Import the complete mobile-control Unity package

**Files:**
- Create/modify: the 176 paths encoded in `MobileControllFolder.unitypackage`
- Create: `Tools/Validation/mobile_package_paths.txt`
- Modify: `Tools/Validation/test_project.py`

**Interfaces:**
- Consumes: extracted `MobileControllFolder.unitypackage` and its `pathname`, `asset`, `asset.meta` records.
- Produces: all mobile package assets at their declared paths with original GUIDs, including prefab GUID `05520b6b54183844f81fbd1abb07aa56`.

- [ ] **Step 1: Generate the expected-path manifest and failing completeness test**

Write the 176 package pathnames, sorted and newline-delimited, to `Tools/Validation/mobile_package_paths.txt`. Add a test that every path exists and every non-folder asset has a `.meta` file.

```python
def test_every_mobile_package_path_was_imported(self):
    expected = read("Tools/Validation/mobile_package_paths.txt").splitlines()
    self.assertEqual(176, len(expected))
    missing = [p for p in expected if not (ROOT / p).exists()]
    self.assertEqual([], missing)
```

- [ ] **Step 2: Run package completeness test and confirm failure**

Run: `python3 -m unittest Tools.Validation.test_project.MobilePackageTests.test_every_mobile_package_path_was_imported -v`

Expected: FAIL with mobile package paths missing.

- [ ] **Step 3: Materialize all package records**

For every Unity-package record, copy `asset` to its exact `pathname` and `asset.meta` to `<pathname>.meta`; create directories as needed and keep bytes unchanged. If a package path already exists, compare GUIDs and preserve the package dependency graph while avoiding silent overwrite of unrelated project content.

- [ ] **Step 4: Validate completeness and GUID preservation**

Add and run assertions that the CF2 rig meta contains `guid: 05520b6b54183844f81fbd1abb07aa56`, all script GUIDs referenced by the rig resolve, and there are no duplicate GUIDs.

Run: `python3 -m unittest Tools.Validation.test_project.MobilePackageTests -v`

Expected: PASS.

- [ ] **Step 5: Commit the complete package import**

```bash
git add Assets/Plugins Assets/'Mobile Controll Folder' Assets/'CF2 Controller Folder' Assets/'Cf2 Script' Assets/Ch4Texture Assets/CircleSolid01.png* Assets/Scene/Scenes Assets/Texture2D Tools/Validation
git commit -m "feat: import complete Control Freak 2 mobile package"
```

### Task 4: Bridge Control Freak 2 into the existing game input system

**Files:**
- Modify: `Assets/Scripts/Core/UI/Settings/ControlMapper/InputManager.cs`
- Modify: `Assets/Scripts/PlayerFunctions/PlayerScript.cs`
- Modify: `Assets/Scripts/Core/GameControllerScript.cs`
- Modify: `Tools/Validation/test_project.py`

**Interfaces:**
- Consumes: `ControlFreak2.CF2Input.GetAxis(string)`, `GetButton(string)`, and `GetKey(KeyCode)`.
- Produces: `InputManager.GetMoveAxis() -> Vector2`, `InputManager.GetLookAxisX() -> float`, and merged action state through existing `GetActionKey`, `GetActionKeyDown`, and `GetActionKeyUp` methods.

- [ ] **Step 1: Add failing source-contract tests**

Assert that `InputManager.cs` imports `ControlFreak2`, defines `GetMoveAxis` and `GetLookAxisX`, maps `Fire1`, `Run`, `Look Behind`, and `Pause`, and uses `CF2Input.GetKey`. Assert `PlayerScript` calls both new axis methods and clamps movement magnitude.

- [ ] **Step 2: Run source-contract tests and confirm failure**

Run: `python3 -m unittest Tools.Validation.test_project.InputBridgeTests -v`

Expected: FAIL because the project still reads only desktop keys and `UnityEngine.Input.GetAxis`.

- [ ] **Step 3: Implement merged action states in `InputManager`**

Add `using ControlFreak2;`. Replace the physical key fallback with `CF2Input.GetKey(key)`. In the per-action state calculation, OR keyboard state with named mobile buttons:

```csharp
private bool GetMobileAction(InputAction action)
{
    switch (action)
    {
        case InputAction.Interact: return CF2Input.GetButton("Fire1");
        case InputAction.UseItem: return CF2Input.GetButton("Use Item");
        case InputAction.Run: return CF2Input.GetButton("Run");
        case InputAction.LookBehind: return CF2Input.GetButton("Look Behind");
        case InputAction.PauseOrCancel: return CF2Input.GetButton("Pause");
        default: return false;
    }
}

public Vector2 GetMoveAxis()
{
    float x = CF2Input.GetAxis("Strafe");
    float y = CF2Input.GetAxis("Forward");
    if (GetActionKey(InputAction.MoveLeft)) x -= 1f;
    if (GetActionKey(InputAction.MoveRight)) x += 1f;
    if (GetActionKey(InputAction.MoveBackward)) y -= 1f;
    if (GetActionKey(InputAction.MoveForward)) y += 1f;
    return Vector2.ClampMagnitude(new Vector2(x, y), 1f);
}

public float GetLookAxisX() => CF2Input.GetAxis("Mouse X");
```

Compute `currentKeyStates[i]` from keyboard and `GetMobileAction` before edge detection, so held Pause produces one down edge.

- [ ] **Step 4: Consume analog axes in player and game controller**

In `PlayerScript.MouseMove`, use `GetLookAxisX()`. In `PlayerMove`, build forward/right motion from `GetMoveAxis()` and clamp once. Replace direct scroll-wheel calls in `GameControllerScript` with `CF2Input.GetAxis("Mouse ScrollWheel")` so desktop fallback remains intact.

- [ ] **Step 5: Run bridge tests**

Run: `python3 -m unittest Tools.Validation.test_project.InputBridgeTests -v`

Expected: PASS, including simultaneous keyboard/touch clamping, distinct interaction/use-item names, and edge-state source checks.

- [ ] **Step 6: Commit the input bridge**

```bash
git add Assets/Scripts/Core Assets/Scripts/PlayerFunctions Tools/Validation/test_project.py
git commit -m "feat: bridge touch controls into game input"
```

### Task 5: Complete the mobile rig and bind it directly to playable scenes

**Files:**
- Modify: `Assets/Mobile Controll Folder/CF2-Rig.prefab`
- Modify: `Assets/Scene/School.unity`
- Modify: `Assets/Scene/TestRoom.unity`
- Modify: `Tools/Validation/test_project.py`

**Interfaces:**
- Consumes: mobile input names from Task 4 and prefab GUID `05520b6b54183844f81fbd1abb07aa56`.
- Produces: active mobile canvas and direct scene prefab instances with a distinct `Use Item` binding.

- [ ] **Step 1: Add failing prefab/scene tests**

Assert the rig prefab contains object names `Joystick`, `TrackPad`, `Run`, `Interaction`, `Pause`, `Mirror`, `Item0`, `Item1`, `Item2`, and `Use Item`; contains `axisName: Use Item`; and has `CF2-Panel` active. Assert both scene files reference the rig GUID exactly once.

- [ ] **Step 2: Run prefab/scene tests and confirm failure**

Run: `python3 -m unittest Tools.Validation.test_project.MobileSceneTests -v`

Expected: FAIL because the panel is inactive, `Use Item` is absent, and the scenes do not reference the rig.

- [ ] **Step 3: Add the dedicated item-use control**

Duplicate the supplied interaction-button structure inside `CF2-Rig.prefab`, rename it `Use Item`, place it above the lower-right item area without overlapping `Pause` or `Interaction`, and change its digital binding from `Fire1` to `Use Item`. Preserve direct sprite GUID references and use a unique set of YAML file IDs.

- [ ] **Step 4: Enable the panel and add direct prefab instances**

Set the `CF2-Panel` GameObject `m_IsActive` to `1`; its Control Freak disabling conditions remain responsible for platform visibility. Add one `PrefabInstance` referencing GUID `05520b6b54183844f81fbd1abb07aa56` to each of `School.unity` and `TestRoom.unity`, with identity transform and no runtime loading code.

- [ ] **Step 5: Run prefab, scene, and GUID tests**

Run: `python3 -m unittest Tools.Validation.test_project.MobileSceneTests Tools.Validation.test_project.MobilePackageTests -v`

Expected: PASS.

- [ ] **Step 6: Commit scene integration**

```bash
git add Assets/'Mobile Controll Folder'/CF2-Rig.prefab Assets/Scene/School.unity Assets/Scene/TestRoom.unity Tools/Validation/test_project.py
git commit -m "feat: add mobile rig to playable scenes"
```

### Task 6: Compatibility scan, archive, and final verification

**Files:**
- Modify as required by evidence: `Assets/Plugins/Control-Freak-2/**/*.cs`
- Modify: `Tools/Validation/test_project.py`
- Create: `TezgahLanBu.zip` outside the project root

**Interfaces:**
- Consumes: completed project from Tasks 1–5.
- Produces: validated source archive ready to open or build with Unity 6000.6.2f1.

- [ ] **Step 1: Add final regression tests**

Add tests scanning for unresolved GUIDs in the rig and scene references, removed Unity APIs identified by the compatibility scan, duplicate Control Freak class definitions, wrong product-name remnants in Player Settings, and forbidden delivery directories.

- [ ] **Step 2: Run the full suite before compatibility repairs**

Run: `python3 -m unittest discover -s Tools/Validation -v`

Expected: either PASS or targeted failures identifying exact Unity 6 compatibility issues; no broad speculative edits.

- [ ] **Step 3: Apply only evidence-backed compatibility repairs**

For each failing removed-API assertion, patch the smallest affected Control Freak 2 editor/sample file without changing runtime input behavior. Keep copyright headers and original GUIDs. Re-run the exact failing test after each repair.

- [ ] **Step 4: Run full verification and archive checks**

Run: `python3 -m unittest discover -s Tools/Validation -v`

Expected: all tests PASS.

Create the ZIP from the project parent, excluding `.git`, generated Unity/IDE files, and any nested delivery ZIP. Then run `unzip -t TezgahLanBu.zip` and list the archive to verify the top-level folder is `TezgahLanBu/` and forbidden paths are absent.

- [ ] **Step 5: Commit the final validated source state**

```bash
git add Assets Packages ProjectSettings Tools docs .gitignore
git commit -m "test: validate Unity 6000.6 mobile project"
```

- [ ] **Step 6: Save the delivery archive and report test limitations**

Save `TezgahLanBu.zip` as the deliverable. Report that static validation passed and explicitly state that Unity import and Android build remain to be run in Unity 6000.6.2f1 or UBA because the editor is unavailable locally.
