# HiPSter: Generate HiPS and catalog

HiPSter is using the HEALPix framework to generate a Hierarchical Progressive Survey (HiPS) for the corresponding spherical latent space positions.
The HiPS representation can be visuaized with [Aladin-Lite](https://github.com/cds-astro/aladin-lite).

```{figure} assets/HEALPix.png
---
name: fig:healpix
width: 500px
align: center
---
Source: {cite}`Fernique_2015`
```

## Installation

HiPSter can be installed via `pip`:

```bash
pip install astro-hipster
```

## Usage

The following command generates a HiPS representation and a catalog showing the real images located
on the latent space using the trained model.

```bash
hipster --checkpoint <checkpoint-file>.ckpt
```

Call `hipster --help` for more information.

Example of a HiPSter config file:
```yaml
root_path: HiPSter
html:
  url: http://localhost:8083
  title: HiPSter representation of Gaia XP DR3
  aladin_lite_version: latest
tasks:
  <list of tasks>
```

For visualization, a Python HTTP server can be started by executing `python3 -m http.server 8082` within the HiPSter output file.
