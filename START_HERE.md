# Your website: how to publish it

This folder is the al-folio theme with your content already filled in: bio, news, publications (blue venue badges with HTML/PDF buttons), a CV page, and a PDF CV generated from the same data. The theme's example content and its maintenance workflows have been removed.

## 1. Before you publish

Your GitHub username (root-goksenin), LinkedIn and site address (https://root-goksenin.github.io) are already filled in.

Check:
- `_bibliography/papers.bib` and `_data/cv.yml`: AudioSphere uses the submission title. Update it if the camera-ready title differs, and add `html`/`pdf`/`code` links once it's public.
- `_pages/about.md` and `_data/cv.yml`: confirm your advisors' names.
- `_news/2026-09-neurips.md`: set the real acceptance date.

## 2. Push it to GitHub

1. On GitHub, create a new **public** repository named exactly `root-goksenin.github.io` (empty: no README).
2. In this folder:
   ```bash
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/root-goksenin/root-goksenin.github.io.git
   git push -u origin main
   ```
3. In the repo: **Settings → Actions → General → Workflow permissions** → choose **Read and write permissions**.
4. Open the **Actions** tab, enable Actions if asked, then open **Deploy site → Run workflow** (main branch). Wait a few minutes until it's green. It creates a `gh-pages` branch. Don't edit that branch.
5. **Settings → Pages** → Source: "Deploy from a branch" → branch `gh-pages`, folder `/ (root)`.
6. Your site is live at `https://root-goksenin.github.io`.

## 3. Day-to-day updates

Every push to `main` redeploys the site; it's live a few minutes later (watch **Actions → Deploy site**). You can edit a file on github.com (pencil icon → **Commit changes**), or work in your local folder:

```bash
git pull            # first: the Render a CV action commits new CV PDFs to the repository
# ...edit files...
git add -A
git commit -m "Describe the change"
git push
```

To update from a new `goksenin-website.zip`:

```bash
git pull
unzip -o ~/Downloads/goksenin-website.zip -d /tmp/site-update
cp -R /tmp/site-update/goksenin-website/. .   # the "/." also copies hidden files such as .github
git add -A
git commit -m "Update site"
git push
```

Two things to avoid:
- Copying files in Finder: it hides the `.github` folder and other files whose names start with a dot. Without `.github/workflows`, pushes stop deploying the site.
- **Re-run jobs** on an old Deploy site run: a re-run rebuilds the commit that run started from. To deploy by hand, use **Actions → Deploy site → Run workflow**, which builds the latest commit.

| To… | Edit |
|---|---|
| Add a paper | `_bibliography/papers.bib`. Set `pubgroup = {reviewed}`, `{underreview}` or `{preprint}` to choose its section (when a paper is accepted, change it to `reviewed`). Add `selected = {true}` to show it on the homepage, and `preview = {file.png}` with the image in `assets/img/publication_preview/`. Add it to the matching section of `_data/cv.yml` too |
| Add a news item | a new file in `_news/` (copy an existing one, change the date and text) |
| Change the bio | `_pages/about.md` |
| Update the CV | `_data/cv.yml`. On push, the **Render a CV** action rebuilds `assets/rendercv/rendercv_output/Goksenin_Yuksel_CV.pdf` (linked from the site) plus two team-specific versions, `Goksenin_Yuksel_CV_spatial_audio.pdf` and `Goksenin_Yuksel_CV_speech.pdf`. Their order of interests, PhD results and papers under review is set in `bin/make_cv_variants.py` |
| Change the photo | replace `assets/img/prof_pic.jpg` |
| Add to the reading list | `_data/reading_list.yml`. Paste an arXiv link with `status: to-read`; change it to `read` when you are done. Title and authors are filled in from arXiv when the site is built. For a paper that isn't on arXiv, give its link, title, authors and year instead (the comments at the top of the file show how). On your phone, use the GitHub app or the pencil icon on github.com |
| Citation counts | filled in automatically from Google Scholar three times a week (**Update Google Scholar citations** action) |
