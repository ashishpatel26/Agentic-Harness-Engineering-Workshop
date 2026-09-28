# Capstone instructor key

Assign one or two faults per pair. The script prints failures without making network calls or sending mail. The teaching goal is a diagnosis tied to a harness boundary, followed by a minimal repair.

| Fault | Diagnosis | Minimum repair |
| --- | --- | --- |
| 1 | Tool selection routes a calculation to document search | Route annual ROI to the calculator; verify its arguments |
| 2 | Invalid cost is converted to a plausible numeric answer | Reject zero or negative cost before calculation |
| 3 | Source ID and claim are unsupported | Cite `security.md` and state deletion guarantees are unverified; keep the report validator |
| 4 | Memory scope is shared across customers | Use the validated `customer_scope(customer_id)` helper |
| 5 | Conclusion ignores unresolved security evidence | Return `pilot` or `insufficient` until the gap is resolved |
| 6 | Retry count exceeds configured cap | Bound attempts to initial run plus `max_retry` |
| 7 | Action check ignores approval | Return false unless approval is recorded; retain the gate immediately before the action |
| 8 | Trace omits the tool event | Register `ToolUsageFinishedEvent` in the listener |

For a real incident, inspect a CrewAI trace and run state before changing code. These faults are deliberately small so every pair can finish a repair within the proposal's 45-minute capstone.
