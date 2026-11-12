# Consultation: lock wait failure modes

URL: https://chatgpt.com/c/6aedf0dd-11d0-83ed-998a-86302cef8363. Task ID: waiting-design-20261106. Model menu: GPT-6 selected; reasoning: Extra High, 4 of 5. Exact prompt saved in prompt.txt; SHA-256 15848af9a169162be47c7fd2826b17a167fa236da67605c6de0c68d82dc00446. The field and conversation were empty before input. PREPARED, INSERTED and SEND_ATTEMPT_RECORDED were obtained; exact posted text and empty field were visible, then CONFIRMED released the lock before waiting. The finished response below was transcribed from the visible page with formatting normalized.

An indefinite, cancellable wait is acceptable for an advisory lock. An indefinite lock hold is not. The protocol must handle abandoned waiters, unused grants, and stale owners without modifying browser drafts.

## Failure modes

| Scenario | Failure | Minimal safeguard |
|---|---|---|
| Client disconnects while waiting | Orphaned queue entry, head-of-line blocking | Remove waiter on cancellation or disconnect; expire abandoned entries |
| Client cancels as lock is granted | Grant/cancellation race; abandoned ownership | Atomically resolve the race; release any grant assigned to a cancelled client |
| Client receives lock but never acts | Other clients wait indefinitely | Short acquisition/activation deadline; expire unused grant |
| Lock holder crashes | Lock remains held | Bounded lease with renewal |
| Holder pauses beyond lease expiry | Old and new holders may both attempt edits | Monotonic fencing token and ownership check before each mutation |
| Release arrives after ownership changes | Old holder releases another client's lock | Release only when owner ID and generation match |
| Lock expires during a browser operation | Concurrent manipulation of composer | Revalidate ownership and composer state before each consequential UI action |

## Minimal safe protocol

1. WAITING: Register a unique request ID. Waiting may continue indefinitely, but must support cancellation and disconnect cleanup. Queue expiry or periodic liveness checks prevent orphaned waiters.
2. GRANTED: Assign an owner token, fencing generation, and short activation deadline. An unused grant expires automatically.
3. ACTIVE: Require bounded leases and renewal tied to client liveness. Reject operations from expired owners or outdated generations.
4. RELEASED / CANCELLED / EXPIRED: Revoke ownership conditionally and wake the next eligible waiter. Cleanup must be idempotent.
5. RECOVERY: Inspect current composer state before taking further action. Never assume that obtaining the lock means the composer is empty or unchanged.

## Critical browser invariant

Lock ownership grants permission to attempt an operation, not permission to overwrite browser state.

If the composer contains an unknown draft, or its ownership/content cannot be established:

- Do not clear, replace, submit, or otherwise modify it.
- Do not automatically retry an uncertain submission.
- Preserve the existing UI state and report a recoverable conflict.
- Require explicit reconciliation before continuing.

A lease or fencing token protects against stale cooperative clients only if every client checks it at the mutation boundary. It cannot make browser UI operations atomic or prevent uncontrolled actors from editing the composer.

## Recommendation

Use cancellable indefinite acquisition + bounded ownership lease + fencing generation + conservative composer-state validation. Keep lock recovery separate from draft recovery. Expiring a stale lock should restore scheduling progress, never trigger browser cleanup.

Safety: Unknown drafts remain untouched.

Liveness: Disconnected clients and inactive owners cannot block the queue indefinitely, assuming failure detection and cleanup continue operating.

Limitation: Actual browser mutations remain subject to UI races unless access is fully serialized and validated.

Decision: The existing fcntl lock is OS-released on process death, unlike the generic failure table. Do not expire an activated browser owner based on a timer: the UI does not provide enforceable fencing. Add cancellable waiting with an activation handshake and a deadline only before browser work starts, while preserving inspection of unresolved state and exact drafts.
