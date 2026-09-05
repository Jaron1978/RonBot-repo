# RON-02 — RonBot Architecture Definition

**Status:** Complete

## Objective

Define the frontend, API, AI and website-knowledge components required for RonBot and select AWS services that keep the solution simple, scalable and cost-conscious.

RonBot must answer questions using only information made available from `ron-jackson.co.uk`. If sufficient information cannot be retrieved from the website knowledge base, RonBot must not invent an answer and should direct the visitor to the Contact Ron page.

## Current deployed architecture

RonBot now runs as a website-grounded AI assistant using a serverless AWS backend and Amazon Bedrock.

```text
Visitor
  |
  v
ron-jackson.co.uk / CloudFront
  |
  v
RonBot frontend (HTML / CSS / JavaScript)
  |
  | HTTPS
  v
Amazon API Gateway HTTP API
  |
  | POST /ask
  v
AWS Lambda (Python)
  |
  +----> Website knowledge (JSONL)
  |          |
  |          v
  |     Retrieval & scoring
  |          |
  |          v
  |     Retrieved website evidence
  |          |
  +----------+
             |
             v
       Amazon Bedrock
             |
             v
      Amazon Nova Micro
             |
             v
     Grounded AI response
             |
             v
      RonBot frontend
```

The portfolio website remains RonBot's canonical source of truth. Website content is processed into structured knowledge and retrieved by the Python backend before relevant evidence is supplied to the AI model.

Amazon Bedrock and Nova Micro generate natural-language responses from that retrieved evidence rather than acting as unrestricted sources of information.

## Frontend

RonBot is integrated into the existing static portfolio using HTML, CSS and JavaScript.

The frontend displays the Robot Ron character, accepts questions, sends them to the production API, displays responses, provides thinking and error states and offers a Contact Ron route when an answer is unavailable.

No AWS credentials or AI secrets are exposed to the browser.

## API

**Amazon API Gateway HTTP API** exposes the RonBot backend over HTTPS using:

`POST /ask`

The API provides the boundary between the public website and the AWS Lambda backend.

CORS is configured for the approved local-development and production portfolio origins.

## Backend

**AWS Lambda**, using Python, provides the RonBot application backend.

The Lambda backend:

- validates incoming requests;
- retrieves relevant evidence from the structured website knowledge;
- applies deterministic retrieval, scoring and grounding safeguards;
- invokes Amazon Nova Micro through Amazon Bedrock when AI-generated responses are appropriate;
- preserves deterministic answer branches where required;
- returns the Contact Ron fallback when sufficient website evidence cannot be retrieved;
- provides structured operational logging through Amazon CloudWatch.

The Lambda execution role uses least-privilege permissions, including model invocation access specifically required for the production Bedrock model.

## AI

**Amazon Bedrock** provides managed access to the production foundation model.

RonBot currently uses:

**Amazon Nova Micro — `amazon.nova-micro-v1:0`**

in AWS Region:

**Europe (London) — `eu-west-2`**

The backend uses the Amazon Bedrock Converse API to generate responses from retrieved website evidence.

The model is explicitly instructed to:

- use only facts supported by the supplied website evidence;
- avoid outside knowledge about Ron;
- avoid unsupported assumptions, speculation and extrapolation;
- avoid combining facts from different roles or contexts unless the evidence explicitly links them;
- leave unsupported details out of its response.

This preserves the website-only knowledge boundary while allowing more natural AI-generated answers.

## Website knowledge and retrieval

The portfolio website remains the authoritative knowledge source.

Approved website content is processed by the Python ingestion pipeline into structured and traceable JSONL knowledge stored in:

`knowledge/website.jsonl`

The Python retrieval layer selects relevant evidence using tokenisation, stop-word handling, query expansion, relevance scoring and targeted weighting for important technical terms.

The current implementation therefore performs retrieval before AI response generation:

`Question -> Retrieval & Scoring -> Website Evidence -> Bedrock -> Nova Micro -> Grounded Response`

If retrieval cannot find sufficient evidence, RonBot uses the Contact Ron fallback rather than asking the model to answer from unrestricted knowledge.

## Grounding safeguards

Grounding is enforced at multiple layers rather than relying solely on the AI prompt.

Current safeguards include:

- website-only knowledge ingestion;
- minimum retrieval relevance requirements;
- deterministic handling for selected questions and guardrails;
- retrieved evidence supplied to the model;
- strict Bedrock grounding instructions;
- explicit protection against unsupported cross-role fact mixing;
- Contact Ron fallback when sufficient evidence is unavailable.

The website remains the canonical source of truth throughout the response path.

## Knowledge updates

Website knowledge is currently generated through the RonBot ingestion pipeline.

When approved portfolio content changes, the knowledge dataset can be regenerated so that `knowledge/website.jsonl` reflects the current website.

This keeps the public portfolio as the authoritative source rather than maintaining a separate manually authored knowledge store.

## Observability

The AWS Lambda backend includes production observability introduced during RON-12.

Current operational controls include:

- structured application logging;
- AWS Lambda request IDs;
- request-duration measurements;
- configurable `LOG_LEVEL`;
- safe `400` and `500` error handling;
- Amazon CloudWatch visibility.

Visitor questions and RonBot answers are not deliberately written to application logs.

## IAM and Bedrock access

The RonBot Lambda execution role follows least-privilege principles.

Bedrock model access is restricted to the permission required to invoke the selected Nova Micro foundation model:

`bedrock:InvokeModel`

for:

`arn:aws:bedrock:eu-west-2::foundation-model/amazon.nova-micro-v1:0`

Broad Amazon Bedrock administrator access is not required by the RonBot Lambda.

## Cost-control principles

The design avoids permanently running application infrastructure.

The existing static website and CloudFront architecture is reused while Amazon API Gateway, AWS Lambda and Amazon Bedrock provide usage-based backend and AI services.

The knowledge corpus remains small and locally structured, avoiding unnecessary managed retrieval infrastructure at the current stage.

No EC2 instances, always-on containers or Kubernetes clusters are required for RonBot v1.

## Security principles

- Do not expose AWS credentials in the browser.
- Use least-privilege IAM permissions for Lambda and related services.
- Restrict browser access using CORS.
- Apply request-size and rate controls as the security layer evolves.
- Treat retrieved website content as the authoritative knowledge source.
- Resist attempts to override RonBot's website-only behaviour.
- Do not expose system prompts, credentials, secrets or sensitive internal configuration.
- Do not deliberately log visitor questions or RonBot answers.

Additional production security controls are planned under RON-15.

## Planned managed knowledge architecture

The original RON-02 architecture considered **Amazon Bedrock Knowledge Bases**, **Amazon S3** and **S3 Vectors** as a future managed retrieval architecture.

These services are **not part of the current production RonBot request path**.

A future architecture may evolve toward:

```text
Portfolio Website
       |
       v
Website Knowledge
       |
       v
Amazon S3
       |
       v
Bedrock Knowledge Base / Managed Retrieval
       |
       v
Amazon Bedrock
       |
       v
Grounded Response
```

Managed retrieval will only be introduced where it provides a clear engineering benefit over the current lightweight Python retrieval implementation.

## Architecture evolution

### Original RON-02 direction

`Portfolio Website -> API Gateway -> Lambda -> Bedrock + Managed Knowledge -> Grounded Response`

### Current production architecture

`Portfolio Website -> API Gateway -> Lambda -> Python Retrieval -> Website Evidence -> Amazon Bedrock -> Nova Micro -> Grounded Response`

This incremental approach allowed retrieval, grounding, API integration, observability and AI model behaviour to be developed and validated independently before being combined.

## Next architectural milestone

**RON-14 — Conversation Context**

The next stage will allow RonBot to support natural follow-up questions while ensuring conversation history cannot override the website-only grounding boundary.

Conversation context will remain subordinate to retrieved website evidence and RonBot's grounding rules.
