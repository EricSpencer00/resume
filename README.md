# resume

LaTeX source for Eric Spencer's CV and role-tuned resumes. GitHub Actions builds
the PDFs on every push to `main` and publishes them into the site repo, where
they are served from:

| URL | File |
| --- | --- |
| `ericspencer.us/cv` | `cv.tex` — the full CV. Everything: all roles, all publications, all projects. No length limit. |
| `ericspencer.us/resume/80626` | `variants/80626.tex` — one page, tuned. |

## Adding a tuned resume

Variants are named by the date they were written, never by the company or role
they target — the URL gets sent to strangers, so it should say nothing about who
it was sent to. Format is `M` + `DD` + `YY`: August 6, 2026 is `80626`. A second
one the same day appends a counter: `806261`.

1. Copy an existing variant: `cp variants/80626.tex variants/80726.tex`
2. Edit it. Keep it to one page — CI fails the build otherwise.
3. Add the matching row to `content/resumes.txt` in the site repo.
4. Push to `main`.

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
pdflatex -jobname resume-80626 variants/80626.tex
```
