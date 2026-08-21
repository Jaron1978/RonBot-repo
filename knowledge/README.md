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

## RON-05 Implementation & Troubleshooting Notes

### Knowledge ingestion result

The RonBot website knowledge ingestion pipeline was successfully implemented and validated against the live portfolio website.

Final validated dataset:

- 12 website pages indexed
- 39 knowledge chunks generated
- Approximately 56 KB of structured JSONL data
- Restricted to `ron-jackson.co.uk`
- External URLs excluded
- HTML content only
- Source URL retained for every knowledge chunk

### Text encoding and chunking

During testing, incorrectly decoded UTF-8 characters were discovered in the generated dataset. The crawler was updated to detect the response encoding before extracting page content.

The chunking implementation was also improved after testing revealed that overlapping chunks could begin part-way through a word. Chunk overlap is now aligned to a word boundary, producing cleaner knowledge passages for downstream retrieval.

### Python environment troubleshooting

Development uncovered a broken local Python 3.14 installation which initially caused Python commands to exit successfully without producing output.

Investigation identified an empty Homebrew Python executable and a virtual environment referencing the damaged installation.

The environment was recovered by:

1. Updating Homebrew.
2. Reinstalling Python 3.14.
3. Recreating the project virtual environment.
4. Reinstalling dependencies using `python3 -m pip`.
5. Verifying Beautiful Soup and Requests imports.
6. Re-running Python syntax and indentation checks.
7. Regenerating and validating the RonBot knowledge dataset.

This troubleshooting also identified conflicting system/Homebrew Python and pip paths, reinforcing the use of a project-specific virtual environment.

### Validation

The ingestion pipeline was validated using:

```bash
python3 -m tabnanny ingest_site.py
python3 -m py_compile ingest_site.py
python3 test_scope.py
python3 ingest_site.py --start-url https://ron-jackson.co.uk --output ronbot_knowledge.jsonl
