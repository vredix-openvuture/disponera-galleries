# Adding a gallery

1. Create `src/<id>/` with the pictures. `<id>` is lowercase letters, digits and dashes.
2. Prepare each picture: JPEG, 2560 px on the long edge, quality 85, metadata stripped.
   ```bash
   magick in.jpg -colorspace sRGB -resize '2560x2560>' -strip -quality 85 -interlace JPEG out.jpg
   ```
3. Write `src/<id>/manifest.json` (see [format.md](format.md)) and `src/<id>/CREDITS.md`.
4. Run `scripts/build.py`. It writes `packs/<id>-1.zip`, `covers/<id>.jpg` and updates `index.json`.
5. Commit and push. GitHub Pages serves the new files a minute later, and the gallery shows up in Settings > Galleries the next time someone opens it.

## Changing a published gallery

A pack is never overwritten: a phone or a pinned build may still fetch the old one by its hash. Raise `version` in the manifest, rebuild, and keep the old zip in `packs/`. The app offers **Update** when the catalogue has a newer version than the installed one.

## Licensing

Only public domain or CC0 pictures. For paintings, the artist must have died more than 70 years ago. A faithful photograph of such a painting carries no new copyright in the EU (Art. 14 DSM directive). On Wikimedia Commons, check that the Licensing section says "PD-Art", "Public domain" or "CC0". Leave out anything "CC BY-SA".
