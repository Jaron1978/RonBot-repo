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

## Current progress

| Task | Description | Status |
| --- | --- | --- |
| RON-01 | Requirements & knowledge boundary | Complete |
| RON-02 | Define frontend, API, AI and website knowledge architecture | Complete |
| RON-03 | Define RonBot personality and response style | Complete |
| RON-04 | Create production RonBot character | Complete |
| RON-05 | Build local RonBot chat interface | Complete |
| RON-07 | Build and validate website knowledge source | Complete |
| RON-08 | Enforce website-only grounding | Complete |

**Project progress: 7 / 24 tasks complete**

**Next task:** RON-06 — Animation & Interaction

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

The frontend and backend directories now contain the local RON-05 implementation. The infrastructure directory is reserved for the later AWS deployment stages.

## Links & project information

- **Portfolio website:** [www.ron-jackson.co.uk](https://www.ron-jackson.co.uk/)
- **RonBot project page:** [Project 02 — RonBot](https://www.ron-jackson.co.uk/project-02.html)
- **GitHub repository:** [Jaron1978/RonBot-repo](https://github.com/Jaron1978/RonBot-repo)

### Current implementation status

RonBot is currently in local development. The browser-based chat interface, production RonBot character, Python retrieval components and website knowledge ingestion pipeline are in place.

The knowledge source is deliberately restricted to content published on Ron's portfolio website. External domains such as GitHub, LinkedIn and Credly are excluded from RonBot's knowledge source.

If RonBot cannot find sufficient information in the website knowledge base to answer a question accurately, it should not guess. Instead, the visitor is directed to the portfolio Contact page.

Production AWS deployment and live website integration will be completed in later project tasks.

