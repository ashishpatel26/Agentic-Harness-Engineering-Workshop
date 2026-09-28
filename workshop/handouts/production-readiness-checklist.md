# Production-readiness checklist

For each item, mark **implemented**, **demonstrated only**, or **future work**. The workshop app is a teaching reference; checking a box requires evidence from a run or test.

- [ ] Tool permissions are explicit and limited to the task.
- [ ] Tool inputs and outputs have validated contracts.
- [ ] Retrieved text is treated as evidence, not instructions.
- [ ] Material claims link to retrievable source passages.
- [ ] Memory scopes isolate users/customers; retention and deletion are defined.
- [ ] Flow state is typed and retry limits are finite.
- [ ] Side effects require authorization at the action boundary.
- [ ] Replayed work cannot repeat a side effect.
- [ ] Model and embedding providers are explicit and approved for the data.
- [ ] Failures, tool calls, and model calls are observable without leaking sensitive content.
- [ ] Evaluation includes normal, missing-evidence, cross-customer, injection, and approval-denied cases.
- [ ] Latency and provider cost are measured against a real budget.
- [ ] Persistence, recovery, deployment ownership, and rollback are rehearsed.

**Next action:** Choose the first unchecked item that can change a user outcome or external action, name an owner, and create a test that demonstrates completion.
