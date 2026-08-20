# RON-02 — RonBot Architecture Definition

**Status:** Complete

## Objective

Define the frontend, API, AI and website-knowledge components required for RonBot and select AWS services that keep the solution simple, scalable and cost-conscious.

RonBot must answer questions using only information made available from `ron-jackson.co.uk`. If sufficient information cannot be retrieved from the website knowledge base, RonBot must not invent an answer and should direct the visitor to the Contact Ron page.

## Proposed architecture

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
  v
AWS Lambda (Python)
  |
  +----> Amazon Bedrock foundation model
  |
  +----> Amazon Bedrock Knowledge Base
              |
              v
        Website knowledge
              |
              v
         Amazon S3
              |
              v
         S3 Vectors
```

## Frontend

RonBot will be integrated into the existing static portfolio using HTML, CSS and JavaScript. The frontend will display the Robot Ron character, accept questions, send them to the API, display responses, provide loading/error states and offer a Contact Ron route when an answer is unavailable. No AWS credentials or AI secrets will be exposed to the browser.

## API

**Amazon API Gateway HTTP API** will expose the RonBot backend over HTTPS, initially through an endpoint such as `POST /ronbot/chat`.

The API layer will provide a clean boundary between the public website and backend, with CORS restrictions, request controls and throttling as appropriate. An HTTP API is preferred because RonBot does not currently require the broader feature set of an API Gateway REST API.

## Backend

**AWS Lambda**, using Python, will act as the application backend. It will validate requests, retrieve relevant website knowledge, invoke the Bedrock model with RonBot's instructions and retrieved context, and return the response to the browser.

The Lambda should also implement the Contact Ron fallback when sufficient grounded information cannot be retrieved.

## AI

**Amazon Bedrock** will provide the foundation model. The initial low-cost candidate is **Amazon Nova Micro**, subject to validation during implementation.

The model will not be treated as an unrestricted source of knowledge. It will be instructed to answer from supplied website context and not invent missing information.

## Website knowledge and RAG

The approved portfolio content will be stored in a dedicated S3 knowledge source, for example:

```text
ronbot-knowledge/
├── home.txt
├── about.txt
├── work-experience.txt
├── education.txt
├── certifications.txt
├── projects.txt
├── cloud-resume.txt
└── contact.txt
```

**Amazon Bedrock Knowledge Bases** will retrieve relevant content for each question. **Amazon S3 Vectors** is the planned vector store because RonBot has a small, bounded knowledge corpus and the project prioritises low ongoing cost.

This creates a Retrieval-Augmented Generation (RAG) flow: retrieve relevant website information first, then use the model to formulate a natural response from that context.

## Knowledge updates

The website remains the authoritative source. For the first version, significant website changes will be manually reflected in the S3 knowledge documents and followed by a knowledge-base synchronisation. Automation can be considered later as part of the deployment pipeline.

## Cost-control principles

The design avoids permanently running application infrastructure. The existing static website/CloudFront setup is reused, while API Gateway, Lambda and Bedrock are usage-based services. The knowledge corpus is small, so S3 storage requirements should remain minimal.

No EC2 instances, always-on containers or Kubernetes clusters are required for RonBot v1.

## Initial security principles

- Do not expose AWS credentials in the browser.
- Use least-privilege IAM permissions for Lambda and related services.
- Restrict browser access using CORS.
- Apply request-size and rate controls.
- Treat retrieved website content as the authoritative knowledge source.
- Resist attempts to override RonBot's website-only behaviour.
- Do not expose system prompts, credentials, secrets or sensitive internal configuration.

## Architecture decision

**RonBot v1:**

`Portfolio Website -> API Gateway HTTP API -> Lambda -> Bedrock + Bedrock Knowledge Base -> S3 / S3 Vectors`

This gives RonBot a serverless, AWS-native, low-cost architecture suitable for a portfolio RAG application with a deliberately constrained knowledge domain.
