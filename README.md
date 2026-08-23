# RonBot

RonBot is an AI assistant for [ron-jackson.co.uk](https://ron-jackson.co.uk), designed to help visitors explore Ron Jackson's professional experience, skills, education, certifications and technical projects through natural conversation.

RonBot is deliberately **website-grounded**: it should answer from the portfolio knowledge base rather than behave as a general-purpose chatbot. If the website does not contain enough information to answer accurately, RonBot directs the visitor to the Contact Ron page.

## Project goals

- Build a distinctive Robot Ron frontend experience rather than a generic chat widget.
- Use a low-cost, serverless AWS architecture.
- Ground answers in approved portfolio content using retrieval-augmented generation (RAG).
- Adapt response depth for recruiters, general visitors and technical users.
- Avoid unsupported claims and hallucinated information about Ron.
- Make the project useful both as a portfolio feature and as an AWS/AI engineering project.

## Planned architecture

`Portfolio Website -> API Gateway HTTP API -> AWS Lambda -> Amazon Bedrock + Bedrock Knowledge Base -> Amazon S3 / S3 Vectors`

See [docs/architecture.md](docs/architecture.md) for the RON-02 architecture decision.

## RonBot behaviour

RonBot is friendly, professional, concise and technically capable. Accuracy takes priority over personality. Its core rule is:

> **If it's on Ron's website, I can talk about it. If it isn't, I don't make it up.**

See [docs/personality.md](docs/personality.md) for the RON-03 personality and response specification.

## RON-04 — Production RonBot character

RON-04 established the production visual identity for RonBot. Rather than using a generic chatbot icon, the project uses a distinctive **Robot Ron** character designed to make the assistant recognisable as part of the portfolio experience.

The production character incorporates visual references to the technologies and learning behind the portfolio, including an AWS hoodie, Redpanda T-shirt, Azure beanie, Google-branded khaki trousers and study material carried under his arm.

The production artwork is stored at:

`frontend/assets/ronbot-production.png`

See [docs/ronbot-character.md](docs/ronbot-character.md) for the character specification.

## RON-05 — Local RonBot chat interface

RON-05 moved RonBot from design and planning into a working local prototype.

The local implementation introduced:

- `frontend/ronbot-widget.html` — the local chat interface.
- `frontend/ronbot.css` — RonBot-specific presentation and layout.
- `frontend/ronbot.js` — frontend interaction logic.
- `backend/retrieve.py` — retrieval logic for finding relevant website knowledge.
- `backend/answer.py` — response-generation logic using retrieved website content.
- `frontend/assets/ronbot-production.png` — the production Robot Ron artwork used by the interface.

This stage provided a local environment in which the frontend, retrieval behaviour and answer flow could be developed and tested before AWS deployment.

## RON-06 — Animation & interaction

RON-06 added the interaction and animation layer to the local RonBot prototype.

The implementation includes:

- Hover feedback on the Robot Ron launcher.
- Animated opening and closing of the chat panel.
- Click-to-open and click-to-close launcher behaviour.
- A dedicated close button and ARIA open/closed state.
- User message bubbles and automatic conversation scrolling.
- A purposeful thinking state in which Robot Ron animates only while a response is being prepared.
- An animated **RonBot is thinking...** indicator.
- Improved message spacing and a more compact chat-panel layout.
- `prefers-reduced-motion` handling for visitors who disable motion.

An early continuous idle animation was intentionally removed after testing because it was distracting during conversation. Motion is now used as feedback rather than decoration.

The response currently shown by the prototype is still a temporary local test response. Connecting the frontend to the production retrieval/API path is handled by later project tasks.

## RON-07 — Website knowledge ingestion

RON-07 implemented the process used to turn the public portfolio website into a local RonBot knowledge source.

The ingestion tooling crawls `ron-jackson.co.uk` and extracts website content into a structured JSONL knowledge base. The resulting data gives RonBot a controlled source from which relevant information can be retrieved rather than allowing it to answer from unrestricted external knowledge.

The ingestion work included:

- Building `ingest_site.py`.
- Crawling the portfolio's same-site HTML pages.
- Extracting useful page text into structured knowledge chunks.
- Preserving source information so retrieved content remains traceable to the website.
- Generating `ronbot_knowledge.jsonl` for local retrieval.
- Verifying that website details were present in the generated knowledge data.

A successful ingestion run visited **39 pages** and produced approximately **56,000 tokens** of website-grounded content.

The ingestion boundary deliberately keeps RonBot focused on the portfolio website rather than crawling external destinations such as GitHub, LinkedIn or other linked services.

## RON-08 — Knowledge preparation and local retrieval

RON-08 prepared the ingested website knowledge for use by the local RonBot retrieval and answer pipeline.

This stage validated that the generated knowledge base could be searched locally and that relevant website content could be supplied to the answer layer. The objective is to ensure that RonBot's responses remain grounded in retrieved portfolio content and that insufficient website evidence results in a safe fallback rather than an invented answer.

RON-07 and RON-08 also produced useful development lessons while establishing the local Python environment. Troubleshooting included:

- Correcting indentation and tab/space issues in the ingestion script.
- Handling website character encoding using `response.apparent_encoding`.
- Diagnosing a broken `.venv` whose Python symlinks pointed to an unavailable Python installation.
- Repairing the Homebrew Python environment.
- Recreating the virtual environment.
- Installing project dependencies with `python3 -m pip`.
- Standardising local Mac commands on `python3` rather than `python`.

These issues and fixes form part of the engineering record for the project rather than being treated simply as setup problems: they document how the local ingestion and retrieval environment was made repeatable and functional.

## Current progress

| Task | Description | Status |
| --- | --- | --- |
| RON-02 | Define frontend, API, AI and website knowledge architecture | Complete |
| RON-03 | Define RonBot personality and response style | Complete |
| RON-04 | Create production RonBot character | Complete |
| RON-05 | Build local RonBot chat interface | Complete |
| RON-06 | Animation and interaction | Complete |
| RON-07 | Build website knowledge ingestion | Complete |
| RON-08 | Prepare and validate local knowledge retrieval | Complete |

**Project progress: 8 / 24 tasks complete**

**Next task:** RON-09 — Unknown-answer Contact fallback

## Repository structure

```text
RonBot-repo/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── personality.md
│   └── ronbot-character.md
├── assets/
│   └── ronbot/
│       └── README.md
├── frontend/
│   ├── assets/
│   │   └── ronbot-production.png
│   ├── ronbot-widget.html
│   ├── ronbot.css
│   └── ronbot.js
├── backend/
│   ├── answer.py
│   └── retrieve.py
└── infrastructure/
```

The repository now contains the local RonBot frontend, interaction layer and retrieval/answer prototype. The infrastructure directory remains available for the later AWS deployment stages.
