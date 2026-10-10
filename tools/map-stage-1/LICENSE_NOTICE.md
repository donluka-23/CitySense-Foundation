# Mapping test dependency and data notices

This directory contains CitySense test code and an npm lockfile; it does not vendor
provider map data, fonts, style code or restricted research archives.

- MapLibre GL JS 6.13.0 is BSD-3-Clause, with incorporated upstream notices. Preserve
  the installed package's complete `LICENSE.txt` if redistributing it.
- Mapbox GL JS 3.32.0 has a proprietary Mapbox product license and incorporated open
  source notices. Its complete installed `LICENSE.txt` and current Mapbox terms govern
  use; installing it does not authorize an account or a deployment.
- OpenFreeMap Liberty is derived from OSM Liberty/Bright: style code BSD-3-Clause,
  design CC BY 4.0; OpenMapTiles schema/design notices apply. OSM data is ODbL 1.0.
  Noto fonts use SIL OFL 1.1; additional icon/source notices are in the provider ledger.
- MapTiler styles/data are governed by the user's Cloud plan and current terms.

Attribution is requested through the engines' source attribution controls and kept
expanded. Mapbox's standard logo and MapTiler's official logo are retained. Actual on-screen attribution still requires
visual verification, especially on a narrow viewport.

Official references: [MapLibre license](https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt),
[Mapbox terms](https://www.mapbox.com/legal/tos),
[OpenFreeMap notices](https://github.com/hyperknot/openfreemap/blob/main/LICENSE.md),
[MapTiler Cloud terms](https://www.maptiler.com/terms/cloud/),
[OSM copyright and license](https://www.openstreetmap.org/copyright).
