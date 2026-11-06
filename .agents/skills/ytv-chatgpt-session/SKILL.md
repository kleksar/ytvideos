---
name: ytv-chatgpt-session
description: Use ChatGPT.com in Chrome for project consultations, selecting the requested model and reasoning mode through the visible UI and safely coordinating shared drafts.
---

# ChatGPT browser session

Use this skill for ChatGPT.com work in Google Chrome, including required project consultations, model selection, reasoning effort, and tab cleanup. This procedure is the single owner for browser session handling. Project-specific requirements for research, editorial scope, records, and required consultation stages remain with the relevant root or topic skill.

## Prepare the session

1. Read the project root instructions, bootstrap, and the applicable task-specific skill. Resolve the exact task and its allowed inputs before opening ChatGPT.
2. Before opening or focusing a ChatGPT tab, acquire the shared composer lock described below. If it is busy, do not open another ChatGPT tab or edit a composer; do independent work and resume when the lock is free.
3. Use a visible Chrome tab. Prefer reusing an agent-created tab already dedicated to the same task. Do not duplicate a live user session or create multiple tabs for the same task without a concrete need.
4. Inspect the visible conversation and composer under the lock before interacting.

## Coordinate the shared composer

In this setup, an unsent composer draft can appear across ChatGPT tabs in the same browser profile. Treat it as one shared mutable slot, based on the user's observed workflow; do not assume every account, profile, or interface version behaves identically. This is a coordination precaution, not a claim that the UI prevents concurrent work.

Use the local advisory lock before opening/focusing ChatGPT or touching a composer:

```sh
python3 .agents/skills/ytv-chatgpt-session/scripts/composer_lock.py --task-id paper-046-story-v1 --controlled
```

Controlled protocol for new cooperating clients: add `--controlled`, keep its stdin open and wait for `READY`. Before clicking Send, write `PENDING <sha256-of-exact-saved-prompt>` and wait for `PENDING_RECORDED`. After visually confirming both the exact posted message and an empty composer, write `VERIFIED`; the holder releases immediately, before waiting for a response. If send status is uncertain, write `UNCERTAIN` and do not retry. EOF/crash after `PENDING` leaves a durable inspection marker. On `NEEDS_INSPECTION`, inspect the original conversation and composer without changing any unknown draft, reconcile whether the message was sent, record the result, and only then write `INSPECTED`; this is a human/agent attestation, not automated verification. If the state cannot be resolved, close stdin and stop. Never infer success from a click or timeout. Do not delete or alter someone else's draft. New invocations using the legacy command refuse unresolved controlled markers, but processes already running older code and clients ignoring the protocol cannot be forced to comply; never interrupt them or claim global enforcement during migration.

Use a unique short task ID, such as the example above. Keep the command running while inspecting the composer, entering text, selecting a model/mode, sending, and verifying the send. The lock file contains only a short task ID, PID, and acquisition time, not the prompt. If another process holds it, the helper reports its task ID and exits without waiting. Prepare prompts, read completed responses, and save records outside the lock. Follow the controlled protocol to release immediately after the posted message and empty composer are confirmed. If the attempt cannot continue, record the observed send state and close stdin; unresolved PENDING remains for inspection. If the tool/session is interrupted, the OS releases the lock; the metadata file may remain, but that alone does not mean the lock is still held.

Before typing, save the exact prompt in the task's consultation record. Each session can restore its own draft from this record. If this request already appears as a posted user message, recover its response. Otherwise, check the composer:

- If it is empty, enter the saved prompt.
- If its full text matches this task's recorded prompt and it has not already been posted, resume without pasting again.
- If the composer contains any other unsent text, leave it untouched, record the obstruction and release the lock without sending.

After entering text, inspect the composer and compare it with the saved prompt before sending. If it differs, leave the text untouched, record the obstruction, and stop. Use the visible Send control only when the full prompt matches, then verify that the user message appears in the conversation and the composer is empty. If submission status is uncertain, record it and inspect the current conversation and composer before acting again. If the exact prompt is already a posted user message, do not resend it. Never retry just because a click or tool call returned an ambiguous result.

For recovery after interruption, reacquire the lock and inspect the current conversation and composer using the same checks. If abandoning an unsent attempt, preserve the prompt, URL, task ID, and observed send status in the task record. Leave any unknown or mixed draft untouched.

The lock coordinates agents sharing this local runtime. It does not coordinate another device, profile, or machine; for those, establish one active composer owner through the shared task coordination channel. Other tasks may prepare work or review completed responses in parallel, but only one task edits/sends through the shared composer at a time.

## Choose the model and reasoning mode

Model and reasoning effort are separate controls. Read each visible label independently immediately before sending a prompt, and record the exact labels in the task record when required.

- Choose the model the user requested, if it is available in the visible model menu. Do not infer model availability from a previous session, plan, or subscription label.
- Choose the reasoning mode the user requested, if it is available in the visible reasoning control. In this UI, reasoning effort is exposed through a labeled slider; use its visible label to confirm the result. The model menu also exposes a separate GPT-6 / GPT-5.6 Sol choice.
- When the user explicitly requests Pro or Extra High, select that mode in the UI. Do not claim that the mode cannot be changed merely because a different mode is currently selected. Do not equate Pro with a model name or treat Extra High as the skill's identity.
- For ytvideos' required personal consultation, use Extra High by default unless the user specifies another mode. A direct Pro request takes precedence. For other tasks, follow the user's requested mode; if none is specified and no project rule sets one, keep the current visible mode.
- Labels, available models, and control layout may change. Do not rely on remembered slider positions or instructions from a previous interface version. If the requested option is absent, disabled, or blocked, capture what the UI actually says and report that limitation without claiming a successful switch.
- The visible Russian label `Очень высокий` is the localized label for `Extra High`. Either confirms Extra High. Record the label as displayed.
- Before sending, confirm that the visible label corresponds to the requested mode, including its documented localization. If the mode is not visibly confirmed, do not send a prompt that depends on it.

Use one narrow request per consultation. Wait for the full answer, read it, and save the request, exact visible model/mode labels, URL, completed answer, and decisions in the task's record. Apply the relevant task skill's content and review requirements; this browser skill does not replace them.

## Save the completed response

Use supported browser UI observations to obtain the complete finished response as text, then write it directly to the task-owned project file with an available authorized file tool. Check that the captured text is complete and matches the visible response; record the source URL and verification. Long output may be truncated: do not claim a complete capture unless checked. Browser and file tools may be separate; no direct filesystem access from the browser runtime is assumed.

Do not open TextEdit or another user editor solely to transfer text. Do not use the shared clipboard when it would change or overwrite its contents; do not inspect, restore, or overwrite another session’s clipboard contents. Use a supported non-clipboard route where available. If complete text cannot be obtained and saved safely using supported tools, preserve the source and report the concrete blocker; do not bypass sandbox, browser or platform restrictions. A visible application remains appropriate when explicitly requested or required by the actual task or supported workflow, not as an automatic workaround.

## Verify inheritance between tabs

Do not assume a new tab inherits a model or reasoning choice. Check the visible label in each new chat before submitting. To verify inheritance as a test, use a separate agent-created tab with an empty composer, select a mode in the first test tab, then inspect the new tab before entering any content. Do not perform this test in a profile with active user sessions or unsent input. Record both observations and restore the original mode after a test if the preference is shared. If a clean isolated test is unavailable, say that inheritance is unverified.

## Close completed tabs

- Close only tabs created by the current task, and only after the answer is complete, the required record is saved, and the tab has no unsent input or unfinished work.
- In a multi-session review, close each completed task-owned tab as soon as its response is recorded and it is no longer needed, without waiting for the entire review cycle to finish. Start each required independent review in a new chat.
- Leave user-created or user-owned tabs open. If using a claimed user tab, release it without closing it.
- Close a task-owned tab only when its composer is empty. The shared composer procedure governs clearing drafts. Leave tabs with approval/login waits or unfinished work open.
- If work remains unfinished and the draft cannot be cleared safely, leave the tab open and identify the continuation point. Once the task is complete, clean up its own empty/completed tabs so obsolete ChatGPT pages do not accumulate.

## Limits and records

If Chrome, the requested model/mode, or the needed chat cannot be accessed, stop only the dependent consultation and report the concrete blocker. Continue independent work when possible. Preserve existing records; save a new consultation under `.agent/consultations/` for project-wide work or next to the episode for episode-specific work, using the project template. Record composer ownership/state, task ID, exact prompt, visible send confirmation, and whether the composer was empty at release. Do not inspect hidden application storage or rely on undocumented UI behavior.
