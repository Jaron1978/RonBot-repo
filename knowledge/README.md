# RON-07 / RON-08 — Website Knowledge Source & Website-Only Grounding

This package creates RonBot's knowledge dataset from the public content of `ron-jackson.co.uk` only.

## Knowledge boundary

RonBot may index and answer from content published on:

- `https://www.ron-jackson.co.uk`
- `https://ron-jackson.co.uk`

External destinations are **never crawled or indexed**, even when the website links to them. This includes GitHub, LinkedIn, Credly, Formspree, AWS documentation, or any other external site.

A link being visible on Ron's website is not permission to ingest the destination. RonBot may know the visible link text or URL if it appears in indexed page content, but it does not fetch the external page.

## What gets indexed

- Public HTML pages discovered by following same-site links.
- Visible content inside each page's `<main>` element.
- Page titles and source URLs for traceability.

## What is excluded

- External links and external redirects.
- CSS, JavaScript, images, fonts, archives, video/audio, PDFs and other non-HTML assets.
- Scripts, styles, SVG markup, navigation/footer boilerplate and interactive form fields.

## Output

The crawler writes JSON Lines (`.jsonl`) records containing:

- stable chunk ID
- source page URL
- page title
- chunk number
- text
- scope marker: `ron-jackson.co.uk-only`

This makes every knowledge chunk traceable back to the website page that supplied it.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ingest_site.py
```

Default output:

```text
knowledge/website.jsonl
```

## Guardrail principle

**If Ron publishes it on the website, RonBot can know it. If it is not on the website, RonBot must not invent it or search elsewhere.**

The later answer-generation layer should reject unsupported answers and direct the visitor to the site's Contact page.
