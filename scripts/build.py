#!/usr/bin/env python3
"""Build every gallery under src/ into packs/, covers/ and index.json.

A pack is a zip whose entries are all STORED: JPEGs do not shrink under
deflate, and a stored zip can be read by the phone without an inflate library.
Entries are written in a fixed order with a fixed timestamp, so the same
source always yields the same bytes and the same SHA-256.

A published version is immutable: if packs/<id>-<version>.zip exists and the
fresh build differs, this stops. Bump "version" in the manifest instead.

Usage: scripts/build.py
"""

import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
COVER_EDGE = 480
PICTURE_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def fail(msg: str) -> None:
    print(f"build: {msg}", file=sys.stderr)
    sys.exit(1)


def load_manifest(src: Path) -> dict:
    manifest = json.loads((src / "manifest.json").read_text())
    for key in ("id", "name", "version", "pictures"):
        if key not in manifest:
            fail(f"{src.name}/manifest.json lacks '{key}'")
    if manifest["id"] != src.name:
        fail(f"{src.name}/manifest.json has id '{manifest['id']}'; it must match the folder")
    listed = {p["file"] for p in manifest["pictures"]}
    present = {f.name for f in src.iterdir() if f.suffix.lower() in PICTURE_EXT}
    if listed != present:
        fail(f"{src.name}: manifest and folder disagree: {sorted(listed ^ present)}")
    if manifest.get("default") and manifest["default"] not in listed:
        fail(f"{src.name}: default '{manifest['default']}' is not one of its pictures")
    return manifest


def pack_bytes(src: Path, manifest: dict) -> bytes:
    """The zip in memory: manifest.json, CREDITS.md (if any), then the pictures."""
    from io import BytesIO
    names = ["manifest.json"] + (["CREDITS.md"] if (src / "CREDITS.md").exists() else [])
    names += sorted(p["file"] for p in manifest["pictures"])
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        for name in names:
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            zf.writestr(info, (src / name).read_bytes())
    return buf.getvalue()


def write_cover(src: Path, manifest: dict, dest: Path) -> None:
    pick = manifest.get("default") or manifest["pictures"][0]["file"]
    dest.parent.mkdir(exist_ok=True)
    if shutil.which("magick"):
        subprocess.run(["magick", str(src / pick), "-resize", f"{COVER_EDGE}x{COVER_EDGE}>",
                        "-strip", "-quality", "82", str(dest)], check=True)
    else:
        shutil.copyfile(src / pick, dest)


def main() -> None:
    galleries = []
    (ROOT / "packs").mkdir(exist_ok=True)
    for src in sorted(p for p in (ROOT / "src").iterdir() if p.is_dir()):
        manifest = load_manifest(src)
        gid, version = manifest["id"], int(manifest["version"])
        data = pack_bytes(src, manifest)
        pack = ROOT / "packs" / f"{gid}-{version}.zip"
        if pack.exists():
            if pack.read_bytes() != data:
                fail(f"{pack.name} is published and the source changed: bump the version")
            state = "unchanged"
        else:
            pack.write_bytes(data)
            state = "built"
        cover = ROOT / "covers" / f"{gid}.jpg"
        write_cover(src, manifest, cover)
        galleries.append({
            "id": gid, "name": manifest["name"], "version": version,
            "count": len(manifest["pictures"]), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "url": f"packs/{pack.name}", "cover": f"covers/{cover.name}",
        })
        print(f"{pack.name}: {state}, {len(data) / 1e6:.1f} MB, sha256 {galleries[-1]['sha256'][:12]}")
    (ROOT / "index.json").write_text(json.dumps({"format": 1, "galleries": galleries}, indent=2) + "\n")


if __name__ == "__main__":
    main()
