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
4. Inspect the visible page before interacting. Treat any existing composer text as an unsent draft. Do not append, replace, send, or clear it until ownership is established.

## Coordinate the shared composer

In this setup, an unsent composer draft can appear across ChatGPT tabs in the same browser profile. Treat it as one shared mutable slot, based on the user's observed workflow; do not assume every account, profile, or interface version behaves identically. This is a coordination precaution, not a claim that the UI prevents concurrent work.

Use the local advisory lock before opening/focusing ChatGPT or touching a composer:

```sh
python3 .agents/skills/ytv-chatgpt-session/scripts/composer_lock.py --task-id paper-046-story-v1
```

Use a unique short task ID, such as the example above. Keep the command running while inspecting the composer, entering text, selecting a model/mode, sending, and verifying the send. The lock file contains only a short task ID, PID, and acquisition time, not the prompt. If another process holds it, the helper reports its task ID and exits without waiting. Prepare prompts, read completed responses, and save records outside the lock. Release the lock with Ctrl+C only after the composer is empty and the submitted user message is visibly present, or after safely clearing this task's own unsent draft. If the tool/session is interrupted, the OS releases the lock; the metadata file may remain, but that alone does not mean the lock is still held.

Before typing, save the exact prompt in the task's consultation record. Then check the visible composer:

- If it is empty, enter the saved prompt.
- If its full text exactly matches this task's recorded prompt and task ID, treat it as this task's interrupted draft and resume without pasting again.
- If any text differs, contains additions, or cannot be tied to this task, stop. Do not edit, send, or clear it; report the visible state and coordinate with its owner.

After entering text, inspect the composer and compare it with the saved prompt before sending. If it differs, do not send or overwrite the unexpected text. Use the visible Send control, then verify that the user message appears in the conversation and the composer is empty. If submission status is uncertain, inspect the current conversation and composer before acting again. If the exact prompt is already a posted user message, do not resend it. Never retry just because a click or tool call returned an ambiguous result.

For recovery after interruption, reacquire the lock and inspect the current conversation. Compare any composer text to the exact saved prompt and check whether that prompt already appears as a sent message. Continue an unsent request at most once after ownership and status are clear. If abandoning it, first preserve the prompt, URL, task ID, and observed send status in the task record; clear the composer only when its entire visible contents exactly match this task's saved draft. Verify it is empty afterward. If any text is mixed, changed, or ambiguous, leave it untouched and report the block so the coordinator can resolve ownership.

The lock coordinates agents sharing this local runtime. It does not coordinate another device, profile, or machine; for those, establish one active composer owner through the shared task coordination channel. Other tasks may prepare work or review completed responses in parallel, but only one task edits/sends through the shared composer at a time.

## Choose the model and reasoning mode

Model and reasoning effort are separate controls. Read each visible label independently immediately before sending a prompt, and record the exact labels in the task record when required.

- Choose the model the user requested, if it is available in the visible model menu. Do not infer model availability from a previous session, plan, or subscription label.
- Choose the reasoning mode the user requested, if it is available in the visible reasoning control. In this UI, reasoning effort is exposed through a labeled slider; use its visible label to confirm the result. The model menu also exposes a separate GPT-6 / GPT-5.6 Sol choice.
- When the user explicitly requests Pro or Extra High, select that mode in the UI. Do not claim that the mode cannot be changed merely because a different mode is currently selected. Do not equate Pro with a model name or treat Extra High as the skill's identity.
- For ytvideos' required personal consultation, use Extra High by default unless the user specifies another mode. A direct Pro request takes precedence. For other tasks, follow the user's requested mode; if none is specified and no project rule sets one, keep the current visible mode.
- Labels, available models, and control layout may change. Do not rely on remembered slider positions or instructions from a previous interface version. If the requested option is absent, disabled, or blocked, capture what the UI actually says and report that limitation without claiming a successful switch.
- After selection, inspect the control again and confirm the exact requested label before sending. If the requested label is not visibly confirmed, do not send a prompt that depends on that mode.

Use one narrow request per consultation. Wait for the full answer, read it, and save the request, exact visible model/mode labels, URL, completed answer, and decisions in the task's record. Apply the relevant task skill's content and review requirements; this browser skill does not replace them.

## Verify inheritance between tabs

Do not assume a new tab inherits a model or reasoning choice. Check the visible label in each new chat before submitting. To verify inheritance as a test, use a separate agent-created tab with an empty composer, select a mode in the first test tab, then inspect the new tab before entering any content. Do not perform this test in a profile with active user sessions or unsent input. Record both observations and restore the original mode after a test if the preference is shared. If a clean isolated test is unavailable, say that inheritance is unverified.

## Close completed tabs

- Close only tabs created by the current task, and only after the answer is complete, the required record is saved, and the tab has no unsent input or unfinished work.
- Leave user-created or user-owned tabs open. If using a claimed user tab, release it without closing it.
- Never close a tab containing an unsent request until the request is either visibly submitted and recorded or safely cleared under the exact-content ownership check above. Do not close tabs with unknown drafts, approval/login waits, or unfinished work.
- If work remains unfinished and the draft cannot be cleared safely, leave the tab open and identify the continuation point. Once the task is complete, clean up its own empty/completed tabs so obsolete ChatGPT pages do not accumulate.

## Limits and records

If Chrome, the requested model/mode, or the needed chat cannot be accessed, stop only the dependent consultation and report the concrete blocker. Continue independent work when possible. Preserve existing records; save a new consultation under `.agent/consultations/` for project-wide work or next to the episode for episode-specific work, using the project template. Record composer ownership/state, task ID, exact prompt, visible send confirmation, and whether the composer was empty at release. Do not inspect hidden application storage or rely on undocumented UI behavior.
