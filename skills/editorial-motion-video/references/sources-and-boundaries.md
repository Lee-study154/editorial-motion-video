# Components, sources and integration boundaries

| Source | Role | Included / verified | Boundary |
|---|---|---|---|
| [TalkCraft](https://github.com/Vincentwei1021/video-talkcraft) | Explainer production method, semantic shots and reference cards | Approved film adaptations and original reference cards: media-pop-in, tilt-3d-page, source-converge, magnifier-detail, still-layout-relay, word-slot-cycle; hashes/provenance included in example | Full native workbench and every upstream audit gate are NOT integrated; no claim of complete upstream skill execution |
| [OneTake](https://github.com/feitangyuan/onetake) | Case selection, causal motion, camera and continuity | Approved film ending-v3 source: OneTakeMotion, ScaleCamera, NestedPage, ScriptGrid, OutroScenesV3; adapted easing/camera helpers and clearing-inspired design. Source lineage otk-7f3e1c; case reference snapshot commit 415758128aa45cc54340df40d8109363447f582e | Upstream is a distinct HTML/JS renderer. This approved film uses a Remotion adaptation, not an installed native OneTake pipeline. Full case composition/score may not be public |
| [Fred visual library](https://www.fred-fu.com/visual-library) | Visual selection/reference | Visual reference role documented | Member-only source was not obtained or bundled; no full-library connector exists |
| [ShotCraft](https://github.com/Vincentwei1021/video-shotcraft) | Optional camera/shot selection for new films | Source link only | Not installed or bundled; inspect relevant skill and actual source before using |
| [Blue illustrations](https://github.com/Lee-study154/blue-editorial-illustrations) | User's illustration assets, character and cover | Approved art layers in old-film example; configurable share in starter | Optional separate skill; no image-generation account/configuration or secrets bundled |
| Remotion 4.0.536 + React 19.3.1 | Actual renderer of approved film and starter | Pinned project manifests, reusable runtime wrapper | Dependencies and browser are not in archive; install/reuse them on target computer |
| Thomas / en-GB-ThomasNeural | Approved English voice | Final approved mixed audio retained | No TTS service is invoked automatically; do not claim offline synthesis or perpetual service availability |

## OneTake effects as options

Use the current upstream README's **Films made with it** as the authoritative list when choosing for a new film. The known local snapshot includes motion-web, one-dot, knockon, clearing, pith, ebb and Pocket Weather Club references; it is not a promise that this list is exhaustive or every full case project is downloadable.

A case may contain several reusable motions. Present the effect and reason for its use, compare a preview, then build/adapt the necessary implementation. Preserve successful implementations for later template extraction; the template database/editor is deliberately not implemented yet.

## Provenance and permissions

The example is a personal project-source bundle, not a relicensing of upstream components or third-party screenshots. Keep source comments, original reference files and provenance hashes when extracting components. TalkCraft and OneTake licenses were verified for this release: both use PolyForm Noncommercial 1.0.0, which permits distribution subject to its terms and required notices. Full license copies and Required Notice lines are included in `../NOTICE.md` and `../licenses/`. No unrestricted or MIT license is claimed for this combined project. Fred member-only source is not bundled. Original artwork and other material retain their creators' rights.

The original BGM was synthesized for this project; the approved mix contains narration, music and SFX. Screenshots and user illustration remain source material with their original rights. No .env, credentials, account settings, node_modules, render cache, old video exports or model weights are included.
