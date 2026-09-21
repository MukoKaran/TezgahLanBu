from collections import defaultdict
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
GUID_PATTERN = re.compile(r"^guid: ([0-9a-f]{32})$", re.MULTILINE)
RIG_SCRIPT_GUID_PATTERN = re.compile(
    r"m_Script: \{fileID: 11500000, guid: ([0-9a-f]{32}), type: 3\}"
)
UGUI_BUILTIN_SCRIPT_GUIDS = {
    "0cd44c1031e13a943bb63640046fad76",  # CanvasScaler
    "1344c3c82d62a2a41a3576d8abb8e3ea",  # Text
    "4e29b1a8efbd4b44bb3f3716e73f07ff",  # Button
    "dc42784cf147c0c48a680349fa168899",  # GraphicRaycaster
    "fe87c0e1cc204ed48ad3b37840f39efc",  # Image
}
PACKAGE_EXTERNAL_GUIDS = UGUI_BUILTIN_SCRIPT_GUIDS | {
    "f4688fdb7df04437aeb418b961361dc5",  # TextMeshProUGUI, supplied by UGUI 2.0
    "f70555f144d8491a825f0804e09c671c",  # Legacy UnityEngine.UI DLL; editor migrates it
}
UNITY_BUILTIN_GUIDS = {"0000000000000000e000000000000000", "0000000000000000f000000000000000"}


def scalar(text, key, indent=0):
    values = re.findall(rf"^{' ' * indent}{re.escape(key)}: (.*)$", text, re.MULTILINE)
    if len(values) != 1:
        raise ValueError(f"Expected one {key}, got {values}")
    return values[0]


def without_csharp_comments(text):
    # Preserve strings so comment-like URL fragments do not consume live code.
    return re.sub(r'@"(?:[^"]|"")*"|"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/',
                  lambda m: " " if m[0].startswith(("//", "/*")) else m[0], text, flags=re.DOTALL)


def unity6_source(text, editor=True):
    """Small conditional scanner, not a C# compiler; only boolean directives."""
    defined = {"UNITY_6000_0_OR_NEWER", "UNITY_6000_6", "UNITY_2017_1_OR_NEWER", "UNITY_2017_3_OR_NEWER", "UNITY_ANDROID"}
    if editor:
        defined.add("UNITY_EDITOR")

    def condition(expression):
        # Convert only recognized identifiers/operators, never evaluate C# input.
        tokens = re.findall(r"[A-Za-z_]\w*|&&|\|\||[!()]", expression)
        if "".join(tokens) != re.sub(r"\s", "", expression):
            raise ValueError(f"Unsupported directive: {expression}")
        boolean = " ".join({"&&": "and", "||": "or", "!": "not", "(": "(", ")": ")"}.get(
            t, str(t == "true" or t in defined)) for t in tokens)
        return bool(eval(boolean, {"__builtins__": {}}, {}))

    output, stack, active = [], [], True
    for line in without_csharp_comments(text).splitlines():
        directive = re.match(r"\s*#(\w+)\s*(.*)", line)
        if not directive:
            if active:
                output.append(line)
            continue
        name, value = directive.groups()
        if name == "if":
            chosen = condition(value)
            stack.append([active, chosen])
            active = active and chosen
        elif name in ("elif", "else"):
            parent, taken = stack[-1]
            chosen = not taken and (name == "else" or condition(value))
            stack[-1][1] |= chosen
            active = parent and chosen
        elif name == "endif":
            active = stack.pop()[0]
        elif name == "define" and active:
            defined.add(value.strip())
        elif name == "undef" and active:
            defined.discard(value.strip())
    if stack:
        raise ValueError("Unbalanced C# directives")
    return "\n".join(output)


def qualified_classes(text):
    """Track namespace/nested-class scopes, ignoring braces in C# strings."""
    text = re.sub(r'@"(?:[^"]|"")*"|"(?:\\.|[^"\\])*"', '""', without_csharp_comments(text))
    scopes, pending, result = [], None, []
    for match in re.finditer(r"\b(namespace|class|struct)\s+([\w.]+)|[{}]", text):
        if match.group(1):
            kind, name = match.group(1, 2)
            pending = name
            if kind == "class":
                result.append(".".join([s for s in scopes if s] + [name]))
        elif match[0] == "{":
            scopes.append(pending)
            pending = None
        else:
            if scopes:
                scopes.pop()
    return result


def project_root():
    return ROOT


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def asset_guid(relative):
    match = GUID_PATTERN.search(read(relative))
    if match is None:
        raise ValueError(f"No Unity GUID in {relative}")
    return match.group(1)


def all_guids():
    return {
        asset_guid(meta.relative_to(ROOT))
        for meta in (ROOT / "Assets").rglob("*.meta")
    }


def guid_owners():
    owners = defaultdict(list)
    for meta in (ROOT / "Assets").rglob("*.meta"):
        owners[asset_guid(meta.relative_to(ROOT))].append(
            str(meta.relative_to(ROOT))
        )
    return dict(owners)


def script_guid_owners():
    owners = defaultdict(list)
    for meta in (ROOT / "Assets").rglob("*.cs.meta"):
        owners[asset_guid(meta.relative_to(ROOT))].append(
            str(meta.relative_to(ROOT))
        )
    return dict(owners)


class ProjectLayoutTests(unittest.TestCase):
    def test_default_discovery_cannot_silently_run_zero_tests(self):
        suite = unittest.TestLoader().discover(str(ROOT), pattern="test_project.py")
        self.assertGreaterEqual(suite.countTestCases(), 24)

    def test_unity_project_layout_exists(self):
        for name in ("Assets", "Packages", "ProjectSettings"):
            self.assertTrue((ROOT / name).is_dir(), name)

    def test_generated_directories_are_excluded(self):
        for name in ("Library", "Temp", "Logs", "obj"):
            self.assertFalse((ROOT / name).exists(), name)

    def test_unused_textmesh_pro_examples_are_excluded(self):
        examples = ROOT / "Assets/TextMesh Pro/Examples & Extras"
        self.assertFalse(examples.exists(), examples.relative_to(ROOT))
        self.assertFalse(Path(f"{examples}.meta").exists(), f"{examples.relative_to(ROOT)}.meta")

    def test_project_version_is_readable(self):
        self.assertTrue(read("ProjectSettings/ProjectVersion.txt").strip())


class ProjectMetadataTests(unittest.TestCase):
    def test_editor_version_and_product_identity(self):
        self.assertEqual("6000.6.2f1", scalar(read("ProjectSettings/ProjectVersion.txt"), "m_EditorVersion"))
        settings = read("ProjectSettings/ProjectSettings.asset")
        self.assertEqual("Tezgah Lan Bu!", scalar(settings, "productName", 2))
        identifiers = re.search(r"^  applicationIdentifier:\n((?:    .*\n)+)", settings, re.MULTILINE).group(1)
        self.assertEqual("com.mukokaran.tezgahlanbu", scalar(identifiers, "Android", 4))
        self.assertEqual("4", scalar(settings, "defaultScreenOrientation", 2))

    def test_manifest_is_valid_json(self):
        manifest = json.loads(read("Packages/manifest.json"))
        self.assertEqual("2.0.0", manifest["dependencies"]["com.unity.ugui"])
        for removed in (
            "com.unity.analytics",
            "com.unity.package-manager-ui",
            "com.unity.textmeshpro",
            "com.unity.modules.vr",
        ):
            self.assertNotIn(removed, manifest["dependencies"])
        modules = "ai animation assetbundle audio cloth director imageconversion imgui jsonserialize particlesystem physics physics2d screencapture terrain terrainphysics tilemap ui uielements umbra unityanalytics unitywebrequest unitywebrequestassetbundle unitywebrequestaudio unitywebrequesttexture unitywebrequestwww vehicles video wind xr".split()
        for module in modules:
            self.assertEqual("1.0.0", manifest["dependencies"].get(f"com.unity.modules.{module}"), module)


class MobilePackageTests(unittest.TestCase):
    def test_every_mobile_package_path_was_imported(self):
        expected = read("Tools/Validation/mobile_package_paths.txt").splitlines()
        self.assertEqual(176, len(expected))
        missing = [path for path in expected if not (ROOT / path).exists()]
        self.assertEqual([], missing)

        missing_meta = [
            path
            for path in expected
            if not (ROOT / path).is_dir() and not (ROOT / f"{path}.meta").is_file()
        ]
        self.assertEqual([], missing_meta)

    def test_cf2_rig_keeps_its_guid_and_resolves_script_guids(self):
        rig_meta = "Assets/Mobile Controll Folder/CF2-Rig.prefab.meta"
        self.assertEqual("05520b6b54183844f81fbd1abb07aa56", asset_guid(rig_meta))

        script_guids = RIG_SCRIPT_GUID_PATTERN.findall(
            read("Assets/Mobile Controll Folder/CF2-Rig.prefab")
        )
        self.assertTrue(script_guids)
        custom_script_guids = set(script_guids) - UGUI_BUILTIN_SCRIPT_GUIDS
        script_owners = script_guid_owners()
        unresolved = {
            guid: script_owners.get(guid, [])
            for guid in sorted(custom_script_guids)
            if len(script_owners.get(guid, [])) != 1
        }
        self.assertEqual({}, unresolved)

    def test_mobile_package_guids_are_unique(self):
        expected = read("Tools/Validation/mobile_package_paths.txt").splitlines()
        guids = [asset_guid(f"{path}.meta") for path in expected]
        self.assertEqual(len(guids), len(set(guids)))

    def test_project_wide_guid_ownership_is_unique(self):
        duplicates = {
            guid: sorted(owners)
            for guid, owners in guid_owners().items()
            if len(owners) > 1
        }
        self.maxDiff = None
        self.assertEqual({}, duplicates)


class InputBridgeTests(unittest.TestCase):
    """Static integration contracts; Unity runtime tests still require the editor."""

    def setUp(self):
        self.manager = read("Assets/Scripts/Core/UI/Settings/ControlMapper/InputManager.cs")
        self.player = read("Assets/Scripts/PlayerFunctions/PlayerScript.cs")
        self.controller = read("Assets/Scripts/Core/GameControllerScript.cs")

    def test_mobile_actions_have_distinct_named_buttons(self):
        self.assertIn("using ControlFreak2;", self.manager)
        for action, button in (
            ("Interact", "Fire1"), ("UseItem", "Use Item"), ("Run", "Run"),
            ("LookBehind", "Look Behind"), ("PauseOrCancel", "Pause"),
        ):
            with self.subTest(action=action):
                self.assertRegex(
                    self.manager,
                    rf'case InputAction\.{action}:\s*return CF2Input\.GetButton\("{button}"\);',
                )

    def test_action_state_merges_before_existing_edge_detection(self):
        # A held touch must contribute to current state, not bypass down/up edges.
        self.assertIn("currentKeyStates[i] = keyDown || GetMobileAction(action);", self.manager)
        self.assertIn("currentKeyStates[(int)action] && !previousKeyStates[(int)action]", self.manager)
        self.assertIn("!currentKeyStates[(int)action] && previousKeyStates[(int)action]", self.manager)
        self.assertNotRegex(self.manager, r"CF2Input\.GetButton(?:Down|Up)\(")
        update = self.manager.split("private void Update()", 1)[1].split("private void UpdateSimulatedKeys()", 1)[0]
        self.assertNotIn("continue;", update, "Unmapped touch actions must still update/reset their state")

    def test_key_fallback_preserves_slots_without_digitizing_joystick(self):
        self.assertIn("CF2Input.GetKey(key)", self.manager)
        self.assertIn("physicalOnly ? Input.GetKey(key) : CF2Input.GetKey(key)", self.manager)
        self.assertRegex(self.manager, r"bool physicalOnly = action >= InputAction\.MoveLeft && action <= InputAction\.MoveBackward;")
        for key in ("primaryKey", "secondaryKey"):
            self.assertIn(f"GetKeyState(binding.{key}, physicalOnly)", self.manager)

    def test_mobile_buttons_do_not_read_undefined_legacy_axes_without_rig(self):
        self.assertRegex(self.manager, r"private bool GetMobileAction\(InputAction action\)\s*\{\s*if \(CF2Input\.activeRig == null\)\s*\{\s*return false;")

    def test_combined_move_axis_clamps_keyboard_and_touch(self):
        self.assertIn("public Vector2 GetMoveAxis()", self.manager)
        self.assertIn('CF2Input.GetAxis("Strafe")', self.manager)
        self.assertIn('CF2Input.GetAxis("Forward")', self.manager)
        for action, adjustment in (
            ("MoveLeft", "x -= 1f"), ("MoveRight", "x += 1f"),
            ("MoveBackward", "y -= 1f"), ("MoveForward", "y += 1f"),
        ):
            self.assertRegex(self.manager, rf"if \(GetActionKey\(InputAction\.{action}\)\)\s*{re.escape(adjustment)};")
        self.assertIn("return Vector2.ClampMagnitude(new Vector2(x, y), 1f);", self.manager)

    def test_no_rig_does_not_read_cf2_wasd_before_mapped_keys(self):
        # Without the Task 5 rig, CF2 falls back to Unity's hard-coded WASD/arrows.
        # GetMoveAxis must use only the game's configurable action mappings in that case.
        move_axis = self.manager.split("public Vector2 GetMoveAxis()", 1)[1].split("public float GetLookAxisX()", 1)[0]
        self.assertRegex(
            move_axis,
            r"float x = 0f;\s*float y = 0f;\s*if \(CF2Input\.activeRig != null\)\s*\{\s*x = CF2Input\.GetAxis\(\"Strafe\"\);\s*y = CF2Input\.GetAxis\(\"Forward\"\);",
        )
        # Require the complete guard body, then reject any CF2 axis read outside
        # it (the earlier prefix-only assertion missed a second unguarded read).
        guard = re.search(r'if \(CF2Input\.activeRig != null\)\s*\{([^{}]*)\}', move_axis)
        self.assertIsNotNone(guard)
        self.assertEqual(['Strafe', 'Forward'], re.findall(r'CF2Input\.GetAxis\("([^"]+)"\)', guard[1]))
        outside_guard = move_axis[:guard.start()] + move_axis[guard.end():]
        self.assertNotRegex(outside_guard, r'CF2Input\.(?:GetAxis|GetAxisRaw|GetKey)\(')
        self.assertNotIn("else", outside_guard)

    def test_player_consumes_clamped_analog_magnitude_and_look(self):
        self.assertIn("Singleton<InputManager>.Instance.GetMoveAxis()", self.player)
        self.assertIn("Singleton<InputManager>.Instance.GetLookAxisX()", self.player)
        self.assertIn('public float GetLookAxisX() => CF2Input.GetAxis("Mouse X");', self.manager)
        self.assertIn("Vector3.ClampMagnitude(transform.forward * moveAxis.y + transform.right * moveAxis.x, 1f)", self.player)
        self.assertIn("moveDirection = movement * playerSpeed;", self.player)
        self.assertNotIn(".normalized", self.player, "Normalizing promotes partial joystick motion to full speed")
        self.assertNotRegex(self.player, r"\bInput\.GetAxis\(")

    def test_scroll_wheel_uses_cf2_desktop_fallback(self):
        self.assertIn("using ControlFreak2;", self.controller)
        self.assertEqual(2, self.controller.count('CF2Input.GetAxis("Mouse ScrollWheel")'))
        self.assertNotRegex(self.controller, r'\bInput\.GetAxis\("Mouse ScrollWheel"\)')


def unity_documents(text):
    """Index Unity serialized records without requiring a third-party YAML loader."""
    return {
        file_id: body
        for file_id, body in re.findall(
            r"^--- !u!\d+ &(\d+)(?: stripped)?\n(.*?)(?=^--- !u!|\Z)",
            text, re.MULTILINE | re.DOTALL,
        )
    }


class MobileSceneTests(unittest.TestCase):
    """Serialized scene/prefab contracts, not an editor or device play test."""

    def setUp(self):
        self.rig = read("Assets/Mobile Controll Folder/CF2-Rig.prefab")
        self.docs = unity_documents(self.rig)
        self.objects = {
            re.search(r"^  m_Name: (.*)$", body, re.MULTILINE).group(1): (file_id, body)
            for file_id, body in self.docs.items()
            if body.startswith("GameObject:") and "  m_Name:" in body
        }

    def components(self, name):
        self.assertIn(name, self.objects, f"Missing usable control {name}")
        _, body = self.objects[name]
        return [self.docs[i] for i in re.findall(r"component: \{fileID: (\d+)\}", body)]

    def test_mobile_panel_and_controls_are_active_with_mobile_only_visibility(self):
        self.assertIn("  m_IsActive: 1\n", self.objects["CF2-Panel"][1])
        for name in ("Joystick", "TrackPad", "Run", "Interaction", "Pause", "Mirror", "Item0", "Item1", "Item2", "Use Item"):
            with self.subTest(control=name):
                components = self.components(name)
                self.assertIn("  m_IsActive: 1\n", self.objects[name][1])
                controls = [c for c in components if "  disablingConditions:\n" in c]
                self.assertEqual(1, len(controls))
                self.assertIn("    mobileModeRelation: 0\n", controls[0])

    def test_item_use_and_interaction_are_separate_registered_buttons(self):
        for name, axis in (("Use Item", "Use Item"), ("Interaction", "Fire1")):
            with self.subTest(control=name):
                control = next(c for c in self.components(name) if "  pressBinding:\n" in c)
                binding = control.split("  pressBinding:\n", 1)[1].split("  toggleOnlyBinding:", 1)[0]
                self.assertIn("    enabled: 1\n", binding)
                self.assertEqual([axis], re.findall(r"axisName: (.+)", binding))
                self.assertRegex(self.rig, rf"    - name: {axis}\n      axisType: 2\n")

    def test_movement_axes_do_not_read_or_synthesize_physical_keys(self):
        for name in ("Strafe", "Forward"):
            with self.subTest(axis=name):
                axis = re.search(rf"    - name: {name}\n(.*?)(?=    - name:|\Z)", self.rig, re.DOTALL).group(1)
                fields = ("affectSourceKeys", "affectedKeyPositive", "affectedKeyNegative") + tuple(
                    f"keyboard{side}{suffix}"
                    for side in ("Positive", "Negative") for suffix in ("", "Alt0", "Alt1", "Alt2")
                )
                for field in fields:
                    self.assertRegex(axis, rf"(?m)^      {field}: 0$", field)
        joystick = next(c for c in self.components("Joystick") if "  joyStateBinding:" in c)
        for direction, axis in (("horz", "Strafe"), ("vert", "Forward")):
            self.assertRegex(joystick, rf"{direction}AxisBinding:\n      enabled: 1\n      targetList:\n      - separateAxes: 0\n        singleAxis: {axis}\n")

    def test_playable_scenes_have_one_direct_rig_instance(self):
        guid = "05520b6b54183844f81fbd1abb07aa56"
        for scene in ("School", "TestRoom"):
            with self.subTest(scene=scene):
                contents = read(f"Assets/Scene/{scene}.unity")
                instances = [body for body in unity_documents(contents).values()
                             if body.startswith("PrefabInstance:") and guid in body]
                self.assertEqual(1, len(instances))
                self.assertEqual(1, contents.count(guid))
                self.assertIn(f"m_SourcePrefab: {{fileID: 100100000, guid: {guid}, type: 3}}", instances[0])
                self.assertIn("m_TransformParent: {fileID: 0}", instances[0])
                self.assertIn("m_Modifications: []", instances[0])
        root = self.components("CF2-Rig")[0]
        self.assertIn("m_LocalPosition: {x: 0, y: 0, z: 0}", root)
        self.assertIn("m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}", root)
        self.assertIn("m_LocalScale: {x: 1, y: 1, z: 1}", root)

    def test_prefab_local_references_and_asset_guids_resolve(self):
        ids = re.findall(r"^--- !u!\d+ &(\d+)", self.rig, re.MULTILINE)
        self.assertEqual(len(ids), len(set(ids)), "Duplicate prefab fileID")
        local_refs = set(re.findall(r"\{fileID: (\d+)\}", self.rig)) - {"0"}
        self.assertEqual(set(), local_refs - set(ids), "Broken local fileID")
        external = set(re.findall(r"guid: ([0-9a-f]{32})", self.rig))
        self.assertEqual(set(), external - all_guids() - UGUI_BUILTIN_SCRIPT_GUIDS)

    def test_item_use_is_connected_to_panel_and_has_separate_hit_area(self):
        use_transform = self.components("Use Item")[0]
        panel_transform = self.components("CF2-Panel")[0]
        use_id = re.findall(r"component: \{fileID: (\d+)\}", self.objects["Use Item"][1])[0]
        self.assertIn(f"  - {{fileID: {use_id}}}\n", panel_transform)
        self.assertIn("m_AnchorMin: {x: 1, y: 0}", use_transform)
        self.assertIn("m_AnchorMax: {x: 1, y: 0}", use_transform)
        # At the supplied 640x480 reference size, reject overlapping action hitboxes.
        def rect(body):
            def pair(field):
                return tuple(map(float, re.search(rf"{field}: \{{x: ([-.\d]+), y: ([-.\d]+)\}}", body).groups()))
            x, y = pair("m_AnchoredPosition")
            ax, ay = pair("m_AnchorMin")
            w, h = pair("m_SizeDelta")
            return x + ax * 640, y + ay * 480, w, h
        x, y, w, h = rect(use_transform)
        self.assertTrue(0 <= x-w/2 < x+w/2 <= 640)
        self.assertTrue(0 <= y-h/2 < y+h/2 <= 480)
        for name in ("Interaction", "Pause", "Run", "Mirror", "Item0", "Item1", "Item2"):
            ox, oy, ow, oh = rect(self.components(name)[0])
            self.assertTrue(abs(x-ox) >= (w+ow)/2 or abs(y-oy) >= (h+oh)/2, name)

    def test_pause_modal_renders_above_mobile_rig_and_keeps_a_resume_path(self):
        # CF2-Rig uses sorting order 100.  The playable School scene's modal must
        # win UI raycasts while paused; TestRoom is intentionally a stripped
        # sandbox and has no GameController/PauseMenu contract to layer.
        school = read("Assets/Scene/School.unity")
        docs = unity_documents(school)
        pause_object_id, pause_object = next(
            (file_id, body) for file_id, body in docs.items()
            if body.startswith("GameObject:") and "  m_Name: PauseMenu\n" in body
        )
        pause_components = [
            docs[file_id]
            for file_id in re.findall(r"component: \{fileID: (\d+)\}", pause_object)
        ]
        pause_canvas = next(component for component in pause_components if component.startswith("Canvas:"))
        self.assertRegex(pause_canvas, r"(?m)^  m_SortingOrder: (?:10[1-9]|[1-9]\d{2,})$")
        self.assertIn("  m_ReceivesEvents: 1", pause_canvas)

        game_controller = next(
            file_id for file_id, body in docs.items()
            if body.startswith("MonoBehaviour:")
            and asset_guid("Assets/Scripts/Core/GameControllerScript.cs.meta") in body
        )
        resume_button_id, resume_button = next(
            (file_id, body) for file_id, body in docs.items()
            if body.startswith("MonoBehaviour:")
            and "m_MethodName: UnpauseGame" in body
        )
        self.assertIn(f"m_Target: {{fileID: {game_controller}}}", resume_button)

        resume_object_id = re.search(r"  m_GameObject: \{fileID: (\d+)\}", resume_button).group(1)
        resume_object = docs[resume_object_id]
        resume_transform_id = next(
            file_id
            for file_id in re.findall(r"component: \{fileID: (\d+)\}", resume_object)
            if docs[file_id].startswith("RectTransform:")
        )
        ancestor_objects = set()
        while resume_transform_id != "0":
            transform = docs[resume_transform_id]
            ancestor_objects.add(re.search(r"  m_GameObject: \{fileID: (\d+)\}", transform).group(1))
            resume_transform_id = re.search(r"  m_Father: \{fileID: (\d+)\}", transform).group(1)
        self.assertIn(pause_object_id, ancestor_objects)

        test_room = read("Assets/Scene/TestRoom.unity")
        self.assertNotIn("m_Name: PauseMenu", test_room)
        self.assertNotIn("m_MethodName: UnpauseGame", test_room)
        self.assertNotIn(asset_guid("Assets/Scripts/Core/GameControllerScript.cs.meta"), test_room)


class FinalIntegrationTests(unittest.TestCase):
    """Contracts at the CF2/raw-input and scene/input-module boundaries."""

    def test_all_installer_axes_exist_once_with_exact_hardware_configuration(self):
        # Removal, duplication, or an off-by-one axis index breaks raw CF2 reads.
        axes = defaultdict(list)
        for block in read("ProjectSettings/InputManager.asset").split("  - serializedVersion: 3\n")[1:]:
            fields = dict(re.findall(r"^    (\w+): *(.*?) *$", block, re.MULTILINE))
            axes[fields["m_Name"]].append(fields)
        required = {"cfEmpty": (0, -1, 0, 0), "cfMouseX": (1, 0, 0, 0),
                    "cfMouseY": (1, 1, 0, 0), "cfScroll0": (1, 2, 0, 0),
                    "cfScroll1": (1, 3, 0, 0)}
        required.update({f"cfJ{joy}{axis}": (2, axis, joy + 1, 0.2)
                         for joy in range(4) for axis in range(10)})
        self.assertEqual(45, len(required))
        for name, (kind, index, joy, dead) in required.items():
            with self.subTest(axis=name):
                self.assertEqual(1, len(axes[name]), f"Missing/duplicate raw axis {name}")
                fields = axes[name][0]
                for key, value in {"type": kind, "axis": index, "joyNum": joy,
                                   "dead": dead, "sensitivity": 1, "gravity": 0,
                                   "snap": 0, "invert": 0}.items():
                    self.assertEqual(value, float(fields[key]), (name, key))
                for key in ("positiveButton", "negativeButton", "altPositiveButton", "altNegativeButton"):
                    self.assertEqual("", fields[key], (name, key))

    def test_active_cf2_hardware_reads_resolve_to_installed_axes(self):
        # Enumerate runtime raw reads; unknown/new dynamic dependencies require review.
        base = ROOT / "Assets/Plugins/Control-Freak-2/Scripts"
        dependencies = set()
        names = re.findall(r"^    m_Name: (.*)$", read("ProjectSettings/InputManager.asset"), re.MULTILINE)
        for path in base.rglob("*.cs"):
            if any(part.startswith("Editor") for part in path.relative_to(base).parts):
                continue
            if path.name == "CF2Input.cs":
                continue  # Public no-rig fallback; named callers tested separately.
            code = unity6_source(path.read_text(encoding="utf-8-sig"), editor=False)
            for arg in re.findall(r"(?<!\w)(?:UnityEngine\.)?Input\.Get(?:Axis(?:Raw)?|Button(?:Down|Up)?)\(([^)]+)\)", code):
                dependencies.add((path.name, arg))
        expected = {("InputRig.cs", "InputRig.CF_MOUSE_DELTA_X_AXIS"),
                    ("InputRig.cs", "InputRig.CF_MOUSE_DELTA_Y_AXIS"),
                    ("GamepadManager.cs", "this.axisName")}
        self.assertEqual(expected, dependencies)
        rig = read("Assets/Plugins/Control-Freak-2/Scripts/System/InputRig.cs")
        for constant in ("CF_MOUSE_DELTA_X_AXIS", "CF_MOUSE_DELTA_Y_AXIS"):
            name = re.search(rf'{constant}\s*=\s*"([^"]+)"', rig)[1]
            self.assertEqual(1, names.count(name), name)
        gamepads = read("Assets/Plugins/Control-Freak-2/Scripts/Gamepads/GamepadManager.cs")
        self.assertRegex(gamepads, r'MAX_JOYSTICKS\s*=\s*4;')
        self.assertRegex(gamepads, r'MAX_INTERNAL_AXES\s*=\s*10;')
        self.assertIn('return ("cfJ" + joyId + "" + axisId);', gamepads)
        for joy in range(4):
            for axis in range(10):
                self.assertEqual(1, names.count(f"cfJ{joy}{axis}"))

    def test_testroom_player_consumes_shared_mobile_and_rebindable_input(self):
        movement = without_csharp_comments(read("Assets/Scripts/PlayerFunctions/PlayerMovement.cs"))
        for call in ("GetMoveAxis()", "GetLookAxisX()", "GetActionKey(InputAction.Run)"):
            self.assertIn(f"Singleton<InputManager>.Instance.{call}", movement)
        self.assertNotRegex(movement, r"\bInput\.Get(?:Axis|Button|Key)")
        self.assertIn("transform.right * moveAxis.x", movement)
        self.assertIn("transform.forward * moveAxis.y", movement)
        self.assertRegex(movement, r'PlayerPrefs.GetFloat\("MouseSensitivity",\s*[^0][^)]*\)')
        scene = read("Assets/Scene/TestRoom.unity")
        self.assertIn(asset_guid("Assets/Scripts/PlayerFunctions/PlayerMovement.cs.meta"), scene)

    def test_testroom_event_system_graph_and_navigation_axes_resolve(self):
        scene = read("Assets/Scene/TestRoom.unity")
        docs = unity_documents(scene)
        anchors = re.findall(r"^--- !u!\d+ &(\d+)", scene, re.MULTILINE)
        self.assertEqual(len(anchors), len(set(anchors)), "Duplicate scene fileIDs")
        systems = [(i, body) for i, body in docs.items()
                   if body.startswith("GameObject:") and "  m_Name: EventSystem\n" in body]
        self.assertEqual(1, len(systems))
        object_id, body = systems[0]
        self.assertIn("  m_IsActive: 1\n", body)
        components = [docs[i] for i in re.findall(r"component: \{fileID: (\d+)\}", body)]
        self.assertEqual(3, len(components))
        for component in components:
            self.assertIn(f"m_GameObject: {{fileID: {object_id}}}", component)
            for target in re.findall(r"\{fileID: (\d+)\}", component):
                self.assertTrue(target == "0" or target in docs, target)
        transform = next(c for c in components if c.startswith("Transform:"))
        self.assertIn("  m_Father: {fileID: 0}", transform)
        module = next(c for c in components if "m_HorizontalAxis:" in c)
        event = next(c for c in components if "m_sendNavigationEvents:" in c)
        school = read("Assets/Scene/School.unity")
        for component in (module, event):
            self.assertIn("  m_Enabled: 1", component)
            script = re.search(r"m_Script: (.*)", component)[1]
            self.assertIn(f"m_Script: {script}", school)
        installed = re.findall(r"^    m_Name: (.*)$", read("ProjectSettings/InputManager.asset"), re.MULTILINE)
        for name in re.findall(r"m_(?:HorizontalAxis|VerticalAxis|SubmitButton|CancelButton): (.*)", module):
            self.assertIn(name, installed)

    def test_touch_action_axes_do_not_bypass_user_keyboard_rebindings(self):
        rig = read("Assets/Mobile Controll Folder/CF2-Rig.prefab")
        for name in ("Strafe", "Forward", "Run", "Look Behind", "Pause"):
            block = re.search(rf"    - name: {re.escape(name)}\n(.*?)(?=    - name:|  keyboardBlockedCodes:)",
                              rig, re.DOTALL)[1]
            self.assertEqual("0", scalar(block, "affectSourceKeys", 6), name)
            values = re.findall(r"^      (?:keyboard\w+|affectedKey\w+): (\d+)$", block, re.MULTILINE)
            self.assertTrue(values)
            self.assertTrue(all(v == "0" for v in values), (name, values))


class FinalRegressionTests(unittest.TestCase):
    def test_no_new_unresolved_playable_scene_references(self):
        # External Unity/UI/TMP refs are not project-local assets. The single
        # Seat mesh reference is already missing in the supplied 2018 template:
        # pin its exact document and location, never exempt the GUID globally.
        known = all_guids() | PACKAGE_EXTERNAL_GUIDS | UNITY_BUILTIN_GUIDS
        baseline_missing = {("School", "15368", "4d7c1677b1627914cbcfa55acd72889a")}
        unresolved = set()
        for scene in ("School", "TestRoom"):
            for file_id, body in unity_documents(read(f"Assets/Scene/{scene}.unity")).items():
                for guid in re.findall(r"guid: ([0-9a-f]{32})", body):
                    if guid not in known:
                        unresolved.add((scene, file_id, guid))
        self.assertEqual(set(), unresolved - baseline_missing)

    def test_cf2_has_no_active_removed_api_calls_in_unity6(self):
        removed = re.compile(r"\b(?:GUITexture|GUIText|MovieTexture)\b|\b(?:UnityEngine\.)?Screen\.lockCursor\b|\bApplication\.(?:LoadLevel|loadedLevel|isWebPlayer)\b|\bEditorApplication\.(?:hierarchyWindowChanged|playmodeStateChanged)\b|\bPrefabUtility\.(?:CreatePrefab|ReplacePrefab|GetPrefabType)\b")
        hits = []
        for path in (ROOT / "Assets/Plugins/Control-Freak-2").rglob("*.cs"):
            for editor in (False, True):
                active = unity6_source(path.read_text(encoding="utf-8-sig"), editor)
                for match in removed.finditer(active):
                    hits.append((str(path.relative_to(ROOT)), editor, match[0]))
        self.assertEqual([], hits)

    def test_control_freak_classes_are_not_defined_twice(self):
        for editor in (False, True):
            definitions = defaultdict(list)
            for path in (ROOT / "Assets").rglob("*.cs"):
                for name in qualified_classes(unity6_source(path.read_text(encoding="utf-8-sig"), editor)):
                    definitions[name].append(str(path.relative_to(ROOT)))
            duplicates = {name: files for name, files in definitions.items()
                          if len(files) > 1 and any("/Control-Freak-2/" in file for file in files)}
            self.assertEqual({}, duplicates)

    def test_source_delivery_contains_no_generated_or_nested_archives(self):
        # git archive uses precisely these tracked entries; the output archive
        # is independently inspected after creation as well.
        if not (ROOT / ".git").exists():
            files = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        else:
            files = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT, text=True).split("\0")
        forbidden = {".git", ".worktrees", ".superpowers", "Library", "Temp", "Logs", "obj", "bin", ".vs", ".vscode", ".idea", "__pycache__", ".pytest_cache"}
        bad = [p for p in files if p and (forbidden.intersection(Path(p).parts) or Path(p).suffix.lower() in {".zip", ".csproj", ".sln", ".pyc", ".pyo", ".user"})]
        self.assertEqual([], bad)

    def test_scanner_handles_nested_classes_and_inactive_legacy_branches(self):
        source = '''namespace ControlFreak2 { class Outer { class Nested {} }
// class Fake {} braces { }
#if UNITY_PRE_5
class Legacy { GUITexture texture; }
#else
class Current { string url = "https://example.com/{class Fake}"; }
#endif
}'''
        self.assertEqual(["ControlFreak2.Outer", "ControlFreak2.Outer.Nested", "ControlFreak2.Current"], qualified_classes(unity6_source(source)))
        self.assertNotIn("GUITexture", unity6_source(source))
