# Pack format

## index.json

```json
{ "format": 1,
  "galleries": [
    { "id": "paintings", "name": "Paintings", "version": 1, "count": 11,
      "bytes": 9772609, "sha256": "…", "url": "packs/paintings-1.zip",
      "cover": "covers/paintings.jpg" } ] }
```

`url` and `cover` are relative to the site root. `sha256` and `bytes` are those of the zip.

## The zip

Every entry is **stored**, not deflated. Disponera's phone app reads the zip with a small reader of its own and refuses a deflated entry. `scripts/build.py` always writes stored entries.

Contents: `manifest.json`, `CREDITS.md`, the pictures. No folders.

## manifest.json

```json
{ "id": "paintings", "name": "Paintings", "version": 1,
  "default": "monet-water-lilies.jpg",
  "pictures": [ { "file": "monet-water-lilies.jpg", "title": "Water Lilies",
                  "artist": "Claude Monet", "year": "1915", "source": "https://…" } ] }
```

`default` is optional. Disponera uses it as the out-of-the-box wallpaper, but only for the preinstalled gallery.
