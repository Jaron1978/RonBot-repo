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
| RON-02 | Define frontend, API, AI and website knowledge architecture | Complete |
| RON-03 | Define RonBot personality and response style | Complete |
| RON-04 | Create production RonBot character | In progress |

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
├── backend/
└── infrastructure/
```

The frontend, backend and infrastructure directories are placeholders for later implementation tasks.
