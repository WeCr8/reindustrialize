"""Fail the build when a selectable founder or active player scene lacks runtime art coverage."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "data/player-scene-manifest.json").read_text(encoding="utf-8"))
avatars = json.loads((ROOT / "data/avatars.json").read_text(encoding="utf-8"))["avatars"]
atlas = json.loads((ROOT / "packages/assets/sprites/atlas.json").read_text(encoding="utf-8"))
launch = {a["id"] for a in avatars if a.get("selectableAtLaunch")}
mapped = set(manifest["founders"])
assert launch == mapped, f"Founder scene map mismatch: missing={launch-mapped}, stale={mapped-launch}"
for founder, profile in manifest["founders"].items():
    assert profile["family"] in {"male", "female"}, f"Invalid family for {founder}"
    assert founder in atlas, f"Missing atlas entry for {founder}"
    assert (ROOT / "packages/assets/sprites" / atlas[founder]["file"]).is_file(), f"Missing sprite for {founder}"
for scene_id, scene in manifest["scenes"].items():
    if not scene.get("active"): continue
    assert scene.get("identityOverlay") is True, f"Active scene {scene_id} lacks exact founder overlay"
    for family in {x["family"] for x in manifest["founders"].values()}:
        asset = scene.get("assets", {}).get(family)
        assert asset, f"Scene {scene_id} lacks {family} asset"
        assert (ROOT / "packages/assets" / asset).is_file(), f"Missing scene asset: {asset}"
print(f"PASS: {len(launch)} founders x {sum(s.get('active', False) for s in manifest['scenes'].values())} active scenes covered")
