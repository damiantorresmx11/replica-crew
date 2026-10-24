# Target: website

Content and presentation sites: landing pages, portfolios, blogs, docs,
restaurant or event sites. Usually no accounts, little backend.

- **Recon:** the public pages themselves, at human speed. Record sections,
  layout per breakpoint, navigation, forms, animations and the content
  types (not the content). `stitch-extract-design-md` writes a DESIGN.md of
  the structure.
- **Stack:** Astro or Next.js static export, Tailwind, a headless CMS or
  Markdown if the user edits content. Forms through the host or Resend.
- **Skip phases:** `replica-backend` unless there are forms, search or a CMS.
  `replica-entrepreneur` is optional (useful for agencies pitching a client).
- **Content:** every text, image and video is the user's own, licensed, or a
  clearly marked placeholder.
- **Test:** Playwright on every page at 390 and 1440 px, axe, Lighthouse.
- **Diff:** `imgdiff.py` layout mode per page.
- **Ship:** static host (Vercel, Netlify, Cloudflare Pages) or the user's VPS.
- **Modes:** for the user's **own** site (redesign, migration to a new
  stack) use `faithful` mode with `clone-website`, `clone-team` or
  `web-clone`; `restyle` then applies the new identity.
