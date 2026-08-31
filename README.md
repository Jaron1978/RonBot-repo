# 🤖 RonBot — Portfolio AI Assistant

**RonBot** is a website-grounded AI assistant designed to help visitors explore my professional experience, skills, education, certifications and technical projects through natural conversation.

<p align="center">
  <img src="frontend/assets/ronbot-production.png" alt="RonBot — Portfolio AI Assistant" width="300">
</p>

<p align="center">
  <a href="https://www.ron-jackson.co.uk">🌐 Portfolio</a> •
  <a href="docs/architecture.md">🏗️ Architecture</a> •
  <a href="docs/personality.md">💬 Personality</a> •
  <a href="docs/ronbot-character.md">🤖 Character Design</a>
</p>

---

## 🚀 Project Snapshot

🌐 **39 portfolio pages ingested**  
📚 **~56,000 tokens of website-grounded content**  
🧪 **11 / 11 regression tests passed**  
🛡️ **Website-only knowledge boundary**  
🐍 **Python retrieval & answer pipeline**  
☁️ **AWS production architecture planned**

## ✨ Current Capabilities

**🔎 Retrieval:** Searches structured knowledge extracted from the portfolio website  
**💬 Grounded Answers:** Responds using retrieved website evidence rather than unrestricted knowledge  
**🧩 Multi-Chunk Evidence:** Combines relevant information when an answer spans multiple knowledge chunks  
**🛡️ Safe Fallback:** Unsupported questions are not guessed and direct visitors to the Contact page  
**🤖 Interaction:** Animated Robot Ron frontend with purposeful thinking states  
**♿ Accessibility:** Supports `prefers-reduced-motion`

## 🛡️ Grounding Principle

RonBot is deliberately restricted to approved portfolio content.

> **If it's on Ron's website, I can talk about it. If it isn't, I don't make it up.**

**Website evidence available** → Grounded answer  
**Insufficient evidence** → Contact Ron fallback

This boundary is a core design requirement, not simply a conversational preference.

### 💻 Current Local Architecture

![RonBot Current Local Architecture](ronbot-current-local-architecture.png)

The current implementation provides a complete local path from portfolio content to grounded answers.

**Knowledge:** Website → Ingestion → JSONL knowledge base  
**Retrieval:** Question → Local retrieval → Relevant website evidence  
**Answer:** Retrieved evidence → Grounded response  
**Fallback:** Insufficient evidence → Contact Ron

✅ **Implemented and tested locally**

### ☁️ Planned AWS Architecture

![RonBot Planned AWS Architecture](ronbot-planned-aws-architecture.png)

> **PLANNED / FUTURE ARCHITECTURE — NOT YET DEPLOYED**

The production design moves the grounded RonBot experience onto a low-cost, serverless AWS architecture.

**Frontend:** Portfolio Website → API Gateway  
**Compute:** API Gateway → AWS Lambda  
**AI:** Lambda → Amazon Bedrock  
**Knowledge:** Bedrock Knowledge Base → Amazon S3 / S3 Vectors  
**Guardrail:** Portfolio-grounded answers remain the core requirement

🔵 **Current status:** Architecture designed; AWS implementation planned.

[View the detailed architecture decision →](docs/architecture.md)

## 🛠️ Technology Stack

**🐍 Backend:** Python · Local retrieval · Grounded answer pipeline  
**🌐 Frontend:** HTML · CSS · JavaScript  
**🧠 AI & Retrieval:** RAG concepts · Knowledge ingestion · Query expansion · Multi-chunk retrieval  
**📚 Knowledge:** Website content · Structured JSONL  
**☁️ Planned AWS:** API Gateway · Lambda · Amazon Bedrock · Bedrock Knowledge Base · S3 / S3 Vectors  
**🔧 Development:** Git · GitHub · Python virtual environments

## 🔨 Development Highlights

RonBot is being built incrementally, with each stage adding and validating a specific part of the system.

**🤖 RON-04 — Character Design**  
Created the production Robot Ron identity used throughout the portfolio experience.

**💬 RON-05 — Local Chat Interface**  
Built the working HTML, CSS and JavaScript conversational interface.

**✨ RON-06 — Animation & Interaction**  
Added purposeful interaction states, thinking feedback and reduced-motion accessibility.

**🌐 RON-07 — Website Knowledge Ingestion**  
Built the website crawler and ingestion pipeline, processing **12 portfolio pages** into **45 structured knowledge chunks**.

**🔎 RON-08 — Local Retrieval**  
Prepared and validated the local knowledge retrieval pipeline used to find relevant website evidence.

**🛡️ RON-09 — Grounded Answers & Fallback**  
Improved query matching, multi-chunk evidence handling and safe unknown-answer behaviour.

**🧠 RON-10 — Recruiter & Technical Answer Depth**
Added adaptive answer depth so general visitors receive concise portfolio answers while technical questions can surface deeper website-grounded implementation detail.

### 🧪 Regression Result

**11 / 11 representative questions passed**

Testing includes both supported questions and deliberately unsupported questions to verify that RonBot does not invent information.

## 💡 Engineering Lessons

Building RonBot's local ingestion and retrieval environment involved troubleshooting several real development issues:

- **Python environment** — diagnosed a broken `.venv` with invalid Python symlinks
- **Homebrew** — repaired the local Python installation and recreated the virtual environment
- **Dependencies** — standardised installation using `python3 -m pip`
- **Character encoding** — resolved website ingestion issues using detected response encoding
- **Python syntax** — identified and corrected indentation and mixed whitespace errors
- **Repeatability** — established a clean, reproducible local development environment

## 📊 Project Progress

**RonBot v1 — Website-Grounded Assistant**

✅ RON-02 — Architecture  
✅ RON-03 — Personality & response design  
✅ RON-04 — Production character  
✅ RON-05 — Local chat interface  
✅ RON-06 — Animation & interaction  
✅ RON-07 — Website knowledge ingestion  
✅ RON-08 — Local knowledge retrieval  
✅ RON-09 — Grounded answers & safe fallback  
✅ RON-10 — Recruiter & technical answer depth  
✅ RON-11 — RonBot API and frontend integration

**Current milestone:** AWS-hosted RonBot API and browser integration established while preserving website-only grounding.

➡️ **Next:** Production website integration and continued RonBot v1 development.

## RON-10 — Recruiter and technical answer depth

RON-10 introduced adaptive answer depth so RonBot can provide concise responses for general visitors while allowing technically focused visitors to ask for deeper implementation detail.

Implemented improvements include:

- Added concise, recruiter-friendly responses for general RonBot questions.
- Added technical-depth detection for questions about architecture, implementation, retrieval, grounding, ingestion and the knowledge source.
- Improved retrieval so RonBot implementation questions favour the dedicated Project 02 content rather than unrelated Work Experience content.
- Resolved ambiguity around phrases such as "How does RonBot work?", where "work" could previously be interpreted as employment history.
- Preserved website-only grounding and the Contact-page fallback for unsupported questions.
- Standardised `knowledge/website.jsonl` as the canonical generated website knowledge file used by the retrieval pipeline.

Example behaviour:

- **"What is RonBot?"** → concise portfolio-focused explanation.
- **"How does RonBot work?"** → deeper explanation of website ingestion, structured knowledge, Python retrieval, grounded answering and fallback behaviour.

RON-10 was acceptance-tested against general, technical-depth and unsupported questions, with the existing grounding and fallback behaviour preserved.

## RON-11 — RonBot API and frontend integration

RON-11 moved RonBot from a local-only prototype to a working AWS-hosted API connected to the browser chat interface.

The work was completed in two stages:

- **RON-11A — API Build:** Created the Lambda handler, packaged the existing retrieval and grounded-answer logic for AWS Lambda, deployed the function in `eu-west-2`, and exposed it through an Amazon API Gateway HTTP API using `POST /ask`.
- **RON-11B — Integration & Testing:** Connected `frontend/ronbot.js` to the live API, configured CORS for local development and the production portfolio domains, verified guardrails and unsupported-question fallbacks through the browser, tested frontend failure handling, cleaned the deployment package, and reviewed the Lambda configuration and cost exposure.

Current request path:

`Browser → API Gateway HTTP API → AWS Lambda → RonBot retrieval and answer logic → website knowledge → browser`

RON-11 was acceptance-tested through both direct Lambda invocation and the browser interface. The browser now receives real responses from the AWS-hosted RonBot backend rather than simulated frontend responses.

The API remains deliberately lightweight at this stage. RonBot continues to use the existing deterministic website-grounded retrieval and answer logic; Amazon Bedrock and the planned managed knowledge architecture remain future development work.

## 🗺️ Roadmap

### 🤖 RonBot v1 — Website-Grounded Assistant

Build and deploy a production-ready conversational assistant grounded exclusively in approved portfolio content.

**Current →** Website ingestion · grounded retrieval and answers · AWS Lambda API · API Gateway · browser integration  
**Next →** Production website integration · Bedrock integration · managed knowledge architecture · production hardening

### 🧠 RonBot v2 — Portfolio AI Agent

Evolve RonBot from question-and-answer into an intelligent interface for exploring the portfolio.

**Planned capabilities:**

- Recruiter · Hiring Manager · Engineer visitor experiences
- AI CV exploration
- Contextual project deep-dives
- Interactive architecture explanations
- Semantic portfolio search
- Controlled portfolio navigation and actions

> AI remains optional — visitors will always be able to explore the traditional portfolio directly.

## 📚 Documentation & Repository

Explore the technical documentation and implementation behind RonBot:

**🏗️ Architecture:** [`docs/architecture.md`](docs/architecture.md)  
**💬 Personality & behaviour:** [`docs/personality.md`](docs/personality.md)  
**🤖 Character design:** [`docs/ronbot-character.md`](docs/ronbot-character.md)  
**🌐 Frontend:** [`frontend/`](frontend/)  
**🐍 Backend:** [`backend/`](backend/)

The repository now contains the working frontend, website ingestion and retrieval pipeline, grounded-answer implementation, AWS Lambda handler, and browser integration with the deployed API Gateway HTTP API.
## 💡 Project Philosophy

RonBot isn't about adding a chatbot to a website simply because AI is available.

The goal is to build a genuinely useful portfolio experience while developing practical skills in **retrieval, grounding, RAG, semantic search, serverless architecture and responsible AI behaviour**.

> **Build it incrementally. Ground it in evidence. Test it before adding complexity.**

---

<p align="center">
  <a href="https://www.ron-jackson.co.uk">🌐 Portfolio</a> •
  <a href="https://github.com/Jaron1978">👤 GitHub Profile</a> •
  <a href="https://github.com/Jaron1978/website-project">☁️ Website Project</a>
</p>
