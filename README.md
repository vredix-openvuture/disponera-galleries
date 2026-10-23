# disponera-galleries

Picture galleries for [Disponera](https://github.com/vredix-openvuture/disponera), downloaded from inside the app.

Each gallery is one zip that Disponera fetches from this repo's GitHub Pages site and installs on the desktop or the phone. The main app repo holds no pictures. It pins the one gallery it ships preinstalled in `galleries.lock`.

## Install

Nothing to install. In Disponera, open **Settings > Galleries** and press **Get** next to a gallery.

To rebuild the packs after changing a gallery:

```bash
scripts/build.py
```

It needs Python 3.11. ImageMagick (`magick`) is optional and makes the catalogue covers smaller.

## Galleries

| Id | Pictures | Notes |
|---|---|---|
| `paintings` | 11 | Public domain paintings from 1766 to 1915. Preinstalled in Disponera. Its default picture (Monet, *Water Lilies*) is the out-of-the-box wallpaper. |

## Links

- [Adding a gallery](docs/adding-a-gallery.md)
- [Pack format](docs/format.md)

Pictures: public domain or CC0, credited per gallery in `src/<id>/CREDITS.md`. Scripts: MIT.

---

<br>
<br>

<div align="center">

<a href="https://openvuture.com"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/icons/ov-site-dark.svg"><img src="assets/icons/ov-site-light.svg" alt="OpenVuture" height="45"></picture></a><a href="https://openvuture.shop"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/icons/ov-shop-dark.svg"><img src="assets/icons/ov-shop-light.svg" alt="OpenVuture Shop" height="45"></picture></a><a href="https://ko-fi.com/openvuture"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/icons/ov-kofi-dark.svg"><img src="assets/icons/ov-kofi-light.svg" alt="Support on Ko-fi" height="45"></picture></a>

<a href="https://openvuture.com"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/icons/ov-madeby-dark.svg"><img src="assets/icons/ov-madeby-light.svg" alt="made by OpenVuture" height="19"></picture></a>

</div>
