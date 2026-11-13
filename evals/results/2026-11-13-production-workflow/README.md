# Cold-session production workflow checks

These are measured editorial workflow attempts in fresh GPT-6 Luna sessions. They are retained as evaluation evidence and are excluded from production task reading paths. They are not current operating instructions.

## Scope and method

Each attempt received an ordinary user request and a separate source checkout without the coordinator's diagnosis or an expected route. The source-file SHA-256 manifest records the exact candidate. The harness captured actual shell commands, stdout, stderr, exit codes and times. Separate local SQLite databases and artifact stores kept these attempts out of production state. No paid media generation, production approvals, upload or publication was authorized.

The copies share the host filesystem; this was logical state isolation, not an operating-system security sandbox. The wrapper fixes the working directory and, for the History cases, the database/workspace environment. It does not capture direct web/collaboration tool calls or progress messages. The source notes, final model answer and coordinator observations must not be confused with a complete raw conversation transcript. The exact user request is preserved where captured; the full initial orchestration prompt for the early attempts is not reconstructed.

`source-manifest.json` records source hashes, not a complete source archive. `accepted-artifacts/` contains exact bytes registered in the store, checked against their digest. `working-artifacts/` preserves adjacent draft files even if subsequently edited. A later edit is never substituted for the registered artifact. `result.json` and the selected state summaries are coordinator-produced assessments from the captured commands, files and read-only SQLite queries.

## Observed outcomes

| Attempt | Outcome | Concrete observation |
|---|---|---|
| `luna-provided` | Failed | Preserved supplied source and created a run, then treated unobserved web search as an unavailable capability without discovery. |
| `luna-history-entry` | Failed | Read entry documentation but wrote an ad hoc script without a run; repeated opening sentences were presented as a loop. |
| `luna-history-start` | Failed | Used `start`, read context and completed research, then stopped before independent review despite an exposed collaboration capability. |
| `luna-history-review` | Failed editorial acceptance | Created the run and an actual reviewer session; store reached `awaiting_script_approval`, but coordinator inspection rejected the narrative seam and review evidence. |
| `luna-history-verbatim` | Failed completion | Created a run and read research context, then saved an unregistered draft and stopped with every task pending and no recorded blocker. |

The fourth attempt received infrastructure assistance: a coordinator-owned read-only task occupied the last collaboration slot. After the writer observed a real thread-limit error, that task was stopped and the writer was told that capacity was available. No correct script, seam or verdict was supplied. Even a successful continuation would therefore be a capacity-assisted result.

The fifth attempt used the strict reviewer-result contract but never reached it. It also read an obsolete redirect that still described an optional narrator loop. Its fifteen-minute budget was not exhausted: captured commands span about two minutes. This is evidence for removing competing legacy instructions and checking actual completion in the host's stop lifecycle, rather than relying on another author reminder. It is not evidence that the stricter review schema itself was exercised by a model.

## Why the fourth result is a failure

The final script ends by asking the viewer to remember what failed before the Boston molasses wave. Replay then starts a new dated introduction to that wave. This reconnects the topic but does not make the opening a natural continuation of the final utterance. The submitted loop evidence nevertheless labeled it continuous narration, declared two ending utterances while quoting one, and described two full readings by the author.

The separate `script-review-evidence.json` decoded to a JSON string rather than a structured review object. The then-current general review validator checked a reviewer identity and script hash without validating that file. The final independent-reader message actually observed by the coordinator discussed attribution of the auditor's legal conclusion, not a recorded review of the exact final two-cycle text. Reaching a state-machine gate did not establish this editorial requirement.

These observations motivate the single reader-produced `ytv-script-review-v1` result and exact reading-input contract. They do not prove that a later reviewer cannot make a semantic mistake. Machine checks bind bytes, required observations and declared failures; the quality of the actual reading remains an evaluated judgment.

## Separate infrastructure attempt

`cli-infrastructure-attempt/` preserves the initial CLI launch failure before a model run began. The in-process app-server client failed with a read-only-filesystem error. It is an infrastructure failure, not a model attempt or a passing evaluation.

## Repeating the check

Prepare a new source checkout and an empty database/workspace. Give a fresh session only an ordinary user request and the checkout path. Keep the evaluator's expected route private. Preserve actual command/tool evidence, exact output hashes, reviewer input and unmodified response, state and approvals. Inspect the story and literal end-to-start seam yourself after the model stops. Record failures and assistance as observed rather than rewriting them after a fix.

No test in this directory claims five finished live videos, measured cost savings, a reliability percentage or a guarantee about future model behavior.
