# RON-02 — RonBot Architecture Definition

**Status:** Complete

## Objective

Define the frontend, API, AI and website-knowledge components required for RonBot and select AWS services that keep the solution simple, scalable and cost-conscious.

RonBot must answer questions using only information made available from `ron-jackson.co.uk`. If sufficient information cannot be retrieved from the website knowledge base, RonBot must not invent an answer and should direct the visitor to the Contact Ron page.

## Current deployed architecture

RON-11 and RON-12 established the first deployed AWS architecture for RonBot.

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

  +--> Retrieval & relevance scoring

  |

  +--> Grounded answer logic

  |

  v

Website knowledge base

  |

  v

Grounded response
```

## Frontend

RonBot will be integrated into the existing static portfolio using HTML, CSS and JavaScript. The frontend will display the Robot Ron character, accept questions, send them to the API, display responses, provide loading/error states and offer a Contact Ron route when an answer is unavailable. No AWS credentials or AI secrets will be exposed to the browser.

## API

**Amazon API Gateway HTTP API** exposes the deployed RonBot backend over HTTPS using `POST /ask`.

The API layer provides a clean boundary between the public website and backend, with CORS configured for the approved frontend origins. Additional request controls and throttling can be introduced as the production architecture evolves.

## Backend

**AWS Lambda**, using Python, is the deployed application backend. It validates requests, runs the existing website-grounded retrieval and answer logic, applies safe fallback behaviour and returns responses through API Gateway.

The Lambda implementation includes structured application logging, AWS request IDs, request-duration measurements, safe `400` and `500` error handling and configurable `LOG_LEVEL` support.

Amazon Bedrock integration is the next development stage. RON-13 will evolve the backend so the model can formulate natural-language responses from approved website evidence without weakening RonBot's existing grounding boundary.

## Planned AI integration

**Amazon Bedrock** will provide the foundation model. The initial low-cost candidate is **Amazon Nova Micro**, subject to validation during implementation.

The model will not be treated as an unrestricted source of knowledge. It will be instructed to answer from supplied website context and not invent missing information.

## Planned managed knowledge and RAG

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

The portfolio website remains RonBot's authoritative source.

The current ingestion pipeline crawls approved portfolio content and generates the structured `knowledge/website.jsonl` dataset used by the retrieval layer.

As RonBot evolves toward managed AWS knowledge services, the update process may move to S3-backed knowledge documents and managed synchronisation. Any future implementation must preserve the website as the canonical source rather than creating a competing source of truth.

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

## Original RON-02 architecture decision

The target architecture selected during RON-02 was:

**RonBot v1 target:**

`Portfolio Website -> API Gateway HTTP API -> Lambda -> Bedrock + Bedrock Knowledge Base -> S3 / S3 Vectors`

This gives RonBot a serverless, AWS-native, low-cost architecture suitable for a portfolio RAG application with a deliberately constrained knowledge domain.
