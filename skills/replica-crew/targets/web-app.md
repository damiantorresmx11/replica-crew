# Target: web-app

The original Replica pipeline was written for this target; every phase skill
applies as written.

- **Recon:** help center, pricing, changelog, public API docs, walkthrough
  videos (`video-to-ui`), the user's own account.
- **Stack:** `replica-architect` default (Next.js, Postgres, Stripe, Resend).
- **Build helpers:** `shadcn-ui`, `stitch-react-components`.
- **Test:** Playwright + axe. **Diff:** `parity.py`, `imgdiff.py`.
- **Ship:** Vercel or the user's own host; `replica-deploy`.
