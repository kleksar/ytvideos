---
name: ytv-chatgpt-session
description: Use ChatGPT.com in Chrome for project consultations, selecting the requested model and reasoning mode through the visible UI and cleaning up completed agent-created tabs.
---

# ChatGPT browser session

Use this skill for ChatGPT.com work in Google Chrome, including required project consultations, model selection, reasoning effort, and tab cleanup. This procedure is the single owner for browser session handling. Project-specific requirements for research, editorial scope, records, and required consultation stages remain with the relevant root or topic skill.

## Prepare the session

1. Read the project root instructions, bootstrap, and the applicable task-specific skill. Resolve the exact task and its allowed inputs before opening ChatGPT.
2. Use a visible Chrome tab. Prefer reusing an agent-created tab already dedicated to the same task. Do not duplicate a live user session or create multiple tabs for the same task without a concrete need.
3. If a new tab is needed, create one dedicated tab and open the requested project/chat or ChatGPT home. Do not switch or navigate a user's active tab to prepare a consultation.
4. Inspect the visible page before interacting. Treat text in the composer as unsent input. Never replace, send, or discard text unless it is the text prepared for this task.

## Choose the model and reasoning mode

Model and reasoning effort are separate controls. Read each visible label independently immediately before sending a prompt, and record the exact labels in the task record when required.

- Choose the model the user requested, if it is available in the visible model menu. Do not infer model availability from a previous session, plan, or subscription label.
- Choose the reasoning mode the user requested, if it is available in the visible reasoning control. In this UI, reasoning effort is exposed through a labeled slider; use its visible label to confirm the result. The model menu also exposes a separate GPT-6 / GPT-5.6 Sol choice.
- When the user explicitly requests Pro or Extra High, select that mode in the UI. Do not claim that the mode cannot be changed merely because a different mode is currently selected. Do not equate Pro with a model name or treat Extra High as the skill's identity.
- For ytvideos' required personal consultation, use Extra High by default unless the user specifies another mode. A direct Pro request takes precedence. For other tasks, follow the user's requested mode; if none is specified and no project rule sets one, keep the current visible mode.
- Labels, available models, and control layout may change. Do not rely on remembered slider positions or instructions from a previous interface version. If the requested option is absent, disabled, or blocked, capture what the UI actually says and report that limitation without claiming a successful switch.
- After selection, inspect the control again and confirm the exact requested label before composing or sending. If the requested label is not visibly confirmed, do not send a prompt that depends on that mode.

Use one narrow request per consultation. Wait for the full answer, read it, and save the request, exact visible model/mode labels, URL, completed answer, and decisions in the task's record. Apply the relevant task skill's content and review requirements; this browser skill does not replace them.

Apply the relevant topic-research or editorial skill for subject-matter requirements. This skill owns browser interaction, visible model and mode verification, and safe tab cleanup.

## Verify inheritance between tabs

Do not assume a new tab inherits a model or reasoning choice. Check the visible label in each new chat before submitting. To verify inheritance as a test, use a separate agent-created tab with an empty composer, select a mode in the first test tab, then inspect the new tab before entering any content. Do not perform this test while another task has unsent input in a tab that could be affected. Record both observations and restore the original mode after a test if the preference is shared. If a clean test cannot be performed safely, say that inheritance is unverified.

## Close completed tabs

- Close only tabs created by the current task, and only after the answer is complete, the required record is saved, and the tab has no unsent input or unfinished work.
- Leave user-created or user-owned tabs open. If using a claimed user tab, release it without closing it.
- Do not close any tab containing unsent input, an unfinished task, an approval/login wait, or work whose result has not been saved. This applies even when the current task created the tab if another task's draft appeared there.
- If work remains unfinished, leave the relevant tab open and identify the continuation point. Once the task is complete, clean up its own empty/completed tabs so obsolete ChatGPT pages do not accumulate.

## Limits and records

If Chrome, the requested model/mode, or the needed chat cannot be accessed, stop only the dependent consultation and report the concrete blocker. Continue independent work when possible. Preserve existing records; save a new consultation under `.agent/consultations/` for project-wide work or next to the episode for episode-specific work, using the project template.
