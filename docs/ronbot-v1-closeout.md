# RonBot v1 — Release and Project Close-out

**Project:** RonBot — Website-Grounded Assistant  
**Close-out date:** 5 October 2026  
**Status:** Complete and live

## Purpose

This record closes RonBot v1 after production release, external user testing
and final verification. It is a concise technical record of what was released,
what real-world feedback exposed and how the project was signed off.

## Release outcome

RonBot is a portfolio assistant available across Ron Jackson's website. It
answers only from approved website content and directs visitors to the Contact
page when the website does not contain enough evidence for a reliable answer.

The production implementation includes:

- a site-wide browser widget;
- Amazon API Gateway, AWS Lambda and Amazon Bedrock;
- a versioned, website-only knowledge dataset;
- input validation, rate controls and safe error handling;
- grounding, prompt-injection and privacy guardrails;
- budget and cost-anomaly monitoring; and
- automated regression tests alongside public API and live-site checks.

## External testing and feedback

RonBot was shared with a small group of external testers. The feedback phase
was intentionally focused on serious usability, accuracy and safety issues.
No tester conversation history or personal data is retained in this document.

| Feedback theme | Resolution |
| --- | --- |
| Lambda failed to load its deployed knowledge file | Rebuilt the deployment package with the required `knowledge/website.jsonl` path preserved, then re-tested the public API. |
| Some broad employment-history questions were incomplete | Expanded approved work-history coverage and added targeted employer responses based only on published portfolio evidence. |
| “Longest job” questions needed a clearer answer | Added a tested, evidence-based response identifying Systems Engineer I at Nexxen (January 2022 to February 2025) as the longest individual listed role. |

Every identified issue was fixed, covered by a regression test and deployed
before close-out.

## Final verification

| Area | Result |
| --- | --- |
| Backend regression suite | Pass — 35 tests passed. |
| Public API | Pass — supported role and longest-role questions returned grounded answers. |
| Safety behaviour | Pass — unknown, private and instruction-like requests use the defined safe responses. |
| Live website | Pass — widget opens, accepts questions and displays answers across the portfolio. |
| Operational controls | Pass — API rate protection, Lambda monitoring, budget and anomaly-monitoring controls remain in place. |

## Completion decision

RON-23, RON-24 and RON-25 are complete. RonBot v1 has a working live release,
documented architecture and safeguards, production validation, external user
feedback and a reproducible regression suite.

Future enhancements belong to a separately scoped RonBot v2 rather than this
completed v1 delivery.
