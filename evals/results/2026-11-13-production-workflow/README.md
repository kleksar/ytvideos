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
| `luna-history-guarded` | Failed creative completion; guard path observed | A simulated host sent the real Stop-hook response, leading from a premature stop to completed research and two actual negative reviews. The writer then recorded a script blocker at the two-pass editorial limit. |

The fourth attempt received infrastructure assistance: a coordinator-owned read-only task occupied the last collaboration slot. After the writer observed a real thread-limit error, that task was stopped and the writer was told that capacity was available. No correct script, seam or verdict was supplied. Even a successful continuation would therefore be a capacity-assisted result.

The fifth attempt used the strict reviewer-result contract but never reached it. It also read an obsolete redirect that still described an optional narrator loop. Its fifteen-minute budget was not exhausted: captured commands span about two minutes. This is evidence for removing competing legacy instructions and checking actual completion in the host's stop lifecycle, rather than relying on another author reminder. It is not evidence that the stricter review schema itself was exercised by a model.

## Sixth attempt: bounded continuation and an unresolved script

The sixth attempt used an immutable 604-file source snapshot, identified by manifest digest `1b4cc39abced2dd7c70fd8c5952a750be3042f82ae4bc5d87352a5b91992869f`. Every file still matched that snapshot when evidence was collected. This is the source version tested; later repository changes are not retroactively attributed to the attempt.

The writer first created a run, read context and saved an unregistered Halifax script, then stopped without independent review. The coordinator invoked the actual hook entrypoint with an explicitly simulated `Stop` event. It returned `block`, continuation 1/3, and the next task action. The coordinator sent only that exact reason back to the writer. The writer then recorded capabilities, completed research, claimed the script task and invoked two real child reviewer sessions for successive versions.

Both reviewers returned `revise`. The second found that the narration overstated the connection between the warning and relief trains. It also rejected the proposed loop: after a qualified answer, replay asks the initial framing question again. The writer recorded a script blocker after the pinned two-pass editorial limit, with no accepted script artifact or approval. The final simulated `Stop` allowed stopping at that blocker. The creative goal failed; the observed improvement is that premature stopping triggered one bounded continuation and the failed story was not accepted as ready.

The review packet exposed another failure. It contained the exact script and two-cycle reading text, but the required output shape was documented elsewhere. The child responses were substantive negative reviews in the wrong JSON structure. During the attempt, the writer requested a schema correction from reviewer v2. The recorded command at `04:31:11 UTC` changed its loop fields and severities; the result still lacked `first_listener`. Neither response was submitted successfully to `complete`. `captured-review-responses/` preserves the exact v1 response, the original v2 response and its later correction from captured `cat` stdout. Original errors are not replaced by the correction. `captured-review-inputs/` extracts each exact script from its reading input and verifies its recorded SHA-256.

`host-config.json`, `host-events.jsonl`, the launch prompt and both saved stop outputs document the simulation. The hook process ran normally, but actual Codex hook trust was not activated. `last_assistant_message` was populated from the saved output artifact, not a verbatim final chat message; the guard ignores that field. Writer and child shell commands shared the recorder's synthetic `CODEX_THREAD_ID`, so this attempt does not prove live host subagent routing. The coordinator observed the child sessions, but raw collaboration calls and messages are outside the shell capture. No production media, approval, external PR, upload or publication occurred.

## Why the fourth result is a failure

The final script ends by asking the viewer to remember what failed before the Boston molasses wave. Replay then starts a new dated introduction to that wave. This reconnects the topic but does not make the opening a natural continuation of the final utterance. The submitted loop evidence nevertheless labeled it continuous narration, declared two ending utterances while quoting one, and described two full readings by the author.

The separate `script-review-evidence.json` decoded to a JSON string rather than a structured review object. The then-current general review validator checked a reviewer identity and script hash without validating that file. The final independent-reader message actually observed by the coordinator discussed attribution of the auditor's legal conclusion, not a recorded review of the exact final two-cycle text. Reaching a state-machine gate did not establish this editorial requirement.

These observations motivate the single reader-produced `ytv-script-review-v1` result and exact reading-input contract. They do not prove that a later reviewer cannot make a semantic mistake. Machine checks bind bytes, required observations and declared failures; the quality of the actual reading remains an evaluated judgment.

## Targeted fresh reviewer packet probe

`reviewer-packet-probe/` is a separate, narrower check after adding the full response schema to the canonical reading packet. A fresh Luna reviewer received only that packet, its descriptor and actual session/tool metadata. Its unmodified response passed the structural/binding CLI with `decision: revise`, `pass_consistent: false` and `script_accepted: false`. It identified the ending-to-opening restart without receiving the previous diagnosis. This is a successful response-contract probe with a negative editorial verdict, not a completed story workflow or proof of historical accuracy.

The three captured shell commands include a failed write command. According to the saved reviewer follow-up, the successful file creation used `apply_patch`, which the shell wrapper does not capture; the exact resulting file and subsequent actual parse/hash output are retained. No raw tool event was reconstructed. The host supplied only its actual returned session identity after assignment. Input, output, implementation hashes, validation stdout and capture limits are in the probe directory.

## Separate infrastructure attempt

`cli-infrastructure-attempt/` preserves the initial CLI launch failure before a model run began. The in-process app-server client failed with a read-only-filesystem error. It is an infrastructure failure, not a model attempt or a passing evaluation.

## Repeating the check

Prepare a new source checkout and an empty database/workspace. Give a fresh session only an ordinary user request and the checkout path. Keep the evaluator's expected route private. Preserve actual command/tool evidence, exact output hashes, reviewer input and unmodified response, state and approvals. Inspect the story and literal end-to-start seam yourself after the model stops. Record failures and assistance as observed rather than rewriting them after a fix.

No test in this directory claims five finished live videos, measured cost savings, a reliability percentage or a guarantee about future model behavior.
