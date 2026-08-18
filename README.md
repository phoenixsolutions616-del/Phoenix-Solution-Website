# Phoenix Solutions Website

Static site, no build step required. Brand-compliant per the Phoenix Solutions Branding Guide
(Fire Orange #FF6A00, Charcoal #1A1A1A, Montserrat/Inter, sub-brand accents for EV/Solar/Smart).

## Deploy: GitHub + Cloudflare Pages (recommended)

### 1. Push to GitHub (one-time setup)
Create an empty repo on github.com (e.g. `phoenix-solutions-site`, private is fine), then from this folder:

```bash
git init
git add .
git commit -m "Phoenix Solutions website v1"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/phoenix-solutions-site.git
git push -u origin main
```

### 2. Connect Cloudflare Pages
1. Cloudflare Dashboard > Workers & Pages > Create > Pages > **Connect to Git**
2. Authorise GitHub and select the repo
3. Build settings:
   - Framework preset: **None**
   - Build command: *(leave empty)*
   - Build output directory: `/`
4. Save and Deploy. First deploy takes about a minute.
5. Add the custom domain (phoenix-solutionsuk.com) under the project's **Custom domains** tab
   and follow the DNS prompt.

`404.html`, `_headers`, `robots.txt` and `sitemap.xml` are picked up automatically.

### 3. Making changes afterwards
Edit, then:

```bash
git add .
git commit -m "describe the change"
git push
```

Cloudflare redeploys automatically on every push. Previous deployments are kept, so you can
roll back instantly from the Pages dashboard if needed. Pushing to any other branch creates a
private preview URL instead of touching the live site.

## Editing pages
- `bodies/` contains page content only; `build.py` wraps each body with the shared
  header/footer/CTA band. After editing a body, run `python3 build.py` to regenerate,
  then commit both the body and the rebuilt .html files.
- You can also edit the built .html files directly if you prefer; they are self-contained.
- Images live in `images/` (optimised JPEGs extracted from the client's asset PDFs).

## Quote form email (already wired)
The form POSTs to `/api/quote`, handled by the Pages Function in `functions/api/quote.js`,
which emails the submission (with photo attachments) to the office inbox via Resend.

One-time setup, about 10 minutes:

1. **Create a Resend account** at resend.com (free tier: 100 emails/day, ample for quotes).
2. **Verify the sending domain**: Resend dashboard > Domains > Add Domain >
   `phoenix-solutionsuk.com`. Resend shows a few DNS records (SPF + DKIM); since the domain
   is already on Cloudflare, add them in Cloudflare > DNS (Resend also offers a one-click
   Cloudflare integration). Wait for the domain to show **Verified**.
3. **Create an API key**: Resend > API Keys > Create (permission: Sending only). Copy it.
4. **Add it to the site**: Cloudflare > your Pages project > Settings > Variables and
   Secrets > Add > name `RESEND_API_KEY`, type **Secret**, paste the key. Save, then
   redeploy (Deployments > Retry, or just push any commit).

That's it. Submissions arrive at **info@phoenixsolutions.com** with the customer's address
as Reply-To, so replying goes straight to them.

Optional variables (same place, plain text):
- `TO_EMAIL` - override the destination inbox (default `info@phoenixsolutions.com`)
- `FROM_EMAIL` - override the sender (default `Phoenix Solutions Website <quotes@phoenix-solutionsuk.com>`;
  the domain part must match the domain verified in Resend)

Notes:
- Pages **Functions only run on Git-connected deployments** - another reason for the
  GitHub route. Drag-and-drop "Upload assets" deploys will serve the site but the form
  will show its error fallback (with phone/email) instead of sending.
- Spam protection: a hidden honeypot field silently discards bot submissions. If spam ever
  becomes a problem, Cloudflare Turnstile can be added to the form - ask your developer.
- Attachment limit: 6 files / 15 MB total per submission; anything above is skipped and
  noted in the email.
