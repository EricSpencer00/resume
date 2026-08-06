# resume

LaTeX source for Eric Spencer's CV and role-tuned resumes. GitHub Actions builds
the PDFs on every push to `main` and publishes them into the site repo, where
they are served from:

| URL | File |
| --- | --- |
| `ericspencer.us/cv` | `cv.tex` — the full CV. Everything: all roles, all publications, all projects. No length limit. |
| `ericspencer.us/resume/project44` | `variants/project44.tex` — one page, tuned for a Forward Deployed Engineer role. |

## Adding a tuned resume

1. Copy an existing variant: `cp variants/project44.tex variants/acme.tex`
2. Edit it. Keep it to one page — CI fails the build otherwise.
3. Push to `main`. It appears at `ericspencer.us/resume/acme` once the site's
   landing page for it is added (see `SETUP.md`).

## Layout

- `preamble.tex` — shared styling, macros, and the contact heading. Edit once, every variant updates.
- `cv.tex` — full CV.
- `variants/*.tex` — one file per tuned resume.

## Building locally

```bash
pdflatex cv.tex
```

Variants use `\input{preamble}`, so compile them from the repo root:

```bash
pdflatex -jobname resume-project44 variants/project44.tex
```
