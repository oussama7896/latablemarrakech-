# La Table Marrakech — Static Site

This repository contains a single-page static website for La Table Marrakech.

Local preview

```
node serve.mjs
open http://localhost:3000
```

Deploy to GitHub + Vercel

1. Create a new GitHub repository and push this local repo:

```
git init
git branch -M main
git add .
git commit -m "Initial site + analytics"
git remote add origin git@github.com:<your-org-or-username>/<repo>.git
git push -u origin main
```

2. On Vercel: Import the GitHub repo and deploy (Vercel will deploy on each push).

Optional: enable GitHub Actions automatic Vercel deploy (requires secrets): `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.
