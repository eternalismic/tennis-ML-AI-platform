
# How to apply this overlay

1) From your repo root, unzip this file:
   ```bash
   unzip woow-mega-docs-extra.zip -d .
   ```
2) Append the contents of `mkdocs.yml.append` to your existing `mkdocs.yml` nav (under `nav:`).
   You can insert them after the existing entries, for example:
   ```yaml
   nav:
     - Home: index.md
     - Architecture: architecture.md
     # ...
   # Append the lines below:
   (contents of mkdocs.yml.append)
   ```
3) Commit and push:
   ```bash
   git add docs mkdocs.yml docs/README-APPLY.md
   git commit -m "docs: GH Pages guide, calibration demo, extra diagrams, OpenShift UWM page"
   git push
   ```
4) Enable GitHub Pages as described in `docs/github-pages.md`.
