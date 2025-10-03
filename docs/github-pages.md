
# Publish Docs on GitHub Pages (Step‑by‑Step)

This repo already includes a CI workflow at `.github/workflows/docs.yml` that:
1) Builds the MkDocs site into `./site`, and  
2) Publishes it to the **`gh-pages`** branch using `GITHUB_TOKEN`.

Follow these steps to enable Pages:

## 1) Ensure Actions can push to `gh-pages`
- Go to **Repository → Settings → Actions → General**  
  - **Workflow permissions**: select **“Read and write permissions.”**  
  - Save.
- If your org enforces branch protections, allow GitHub Actions to push to `gh-pages` (or create an exception).

## 2) Enable Pages
- Go to **Repository → Settings → Pages**  
  - **Source**: **Deploy from a branch**  
  - **Branch**: select **`gh-pages`**, **/ (root)**  
  - Save.  
  GitHub will show your docs URL, e.g. `https://<user>.github.io/<repo>/`.

> The first publish happens after the next push to `main` that touches `docs/**` or `mkdocs.yml`.

## 3) Run the workflow
- Commit and push any change under `docs/`:
  ```bash
  echo "" >> docs/index.md
  git add docs/index.md && git commit -m "trigger docs publish" && git push
  ```
- Watch **Actions → Build & Publish Docs**; on success, Pages serves your site.

## 4) (Optional) Custom domain
- Create `CNAME` in repo root (or in `docs/` then configure MkDocs to include it) with your domain:
  ```
  docs.example.com
  ```
- Point your DNS to GitHub Pages per the official docs.
- In **Settings → Pages**, set the custom domain; GitHub will provision TLS automatically.

## 5) (Optional) Private repositories
- GitHub Pages for private repos requires an appropriate plan. If restricted, consider:
  - Publishing the site from a public mirror repo,
  - Or self-hosting the static `site/` via any web server / S3 + CloudFront.

## Troubleshooting
- **404 / old content**: Clear browser cache, ensure Pages is set to `gh-pages`, confirm the workflow pushed `site/` contents.
- **Action cannot push**: Check Workflow permissions, branch protection, or use a PAT with `contents:write` (then set it as a secret and pass it to the gh-pages action).
