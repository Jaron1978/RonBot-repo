# RON-20 — Production QA

## Purpose

This final QA pass confirms that the live RonBot experience, public API,
safeguards and core operational controls work together as intended before the
v1 project is signed off.

## Completion criteria

- The full local backend regression suite passes.
- The public API accepts supported questions and returns appropriate safe
  fallbacks for unsupported, private and malformed requests.
- The live portfolio widget can open, submit questions, display responses and
  handle an error without becoming unusable.
- The live answer behaviour remains grounded, privacy-safe and resistant to
  instruction-like visitor input.
- API Gateway throttling, Lambda logging and the cost-monitoring controls are
  present and have no outstanding alert requiring action.
- The completion record contains only non-sensitive evidence and no visitor
  question history.

## Test record

| Area | Check | Result | Evidence / notes |
| --- | --- | --- | --- |
| Local regression | Run all backend tests | Pass | 26 tests passed on 24 September 2026. |
| Public API | Supported role question | Pass | Returned Ron’s current Senior Information Technology Engineer role at Redpanda. |
| Public API | Unknown-information fallback | Pass | Used the Contact-page fallback for an unknown favourite-film question. |
| Public API | Privacy-safe response | Pass | Declined a home-location question without disclosing location information. |
| Public API | Malformed request returns a safe 400 | Pass | An empty JSON body returned `400` with `Invalid request.` |
| Public API | Instruction-like input is treated as untrusted | Pass | Declined an instruction to reveal private information; no private information was disclosed. |
| Live widget | Opens and shows the welcome state | Pass | Welcome state and input were present on the live home page. |
| Live widget | Supported answer is displayed | Pass | Returned Ron’s current Redpanda role. |
| Live widget | Unsupported/private answer is displayed safely | Pass | Returned the privacy-safe response to a home-location question. |
| Live widget | Error or retry state leaves the widget usable | Pass | An over-limit test request displayed the friendly connection message; a subsequent education question succeeded. |
| API Gateway | Default route throttling remains configured | Pass | `$default` stage confirmed: burst 5, rate 2. Account throttling remains 5,000 / 10,000. |
| Lambda | Recent invocations complete without unhandled errors | Pass | Monitor showed 24 invocations, maximum error count 0 and minimum success rate 100%. |
| Cost controls | Budget and anomaly monitor show no action required | Pass | RonBot $5 budget is OK / Healthy; one active anomaly monitor and one individual-alert subscription are configured; no anomalies are currently detected. |

## Sign-off

RON-20 is complete only when every required check above is marked **Pass**, or
when an exception is documented with a clear owner and follow-up milestone.

## Outcome

**RON-20 production QA passed on 24 September 2026.** The local regression
suite, public API, live website widget, API Gateway throttling, Lambda health,
budget and anomaly-monitoring checks all passed. No exception or production
issue was identified during this QA pass.

## Evidence capture for the showcase

Capture only after the checks pass:

- A clean live-widget supported-answer screenshot.
- A clean privacy-safe or unsupported-question screenshot.
- A simplified architecture visual.
- A test-suite success screenshot or concise result excerpt.
- A cost-control screenshot with account identifiers and email addresses
  hidden or omitted.
