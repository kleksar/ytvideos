# Caption exception review — Franklin 047

- Task: `franklin-caption-exception-2026-11-05`
- ChatGPT URL: https://chatgpt.com/c/6aec5434-1758-83eb-a4b4-32c1b1c33d3b
- Visible model label: `ChatGPT` (no specific model name exposed in the control).
- Visible reasoning label: `Extra High`, slider `4 из 5`.
- Exact saved prompt: `CAPTION_EXCEPTION_CONSULTATION_PROMPT.md`; SHA-256 recorded in the session output.
- Send verified: exact prompt appeared as a posted user message; composer was empty on release; answer completed.

## Consultation result

ChatGPT recommended six groups and said this avoided splitting “had abandoned” or “finally sunk.” It could not access Chalkboard SE Bold in its environment, so its table measured DejaVu Sans Bold at 84 px, not the production font:

| Group | ChatGPT's substitute-font width |
|---|---:|
| Before Erebus was found, | 1217 px |
| searchers knew where | 1065 px |
| Franklin's crews | 764 px |
| had abandoned the ships, | 1230 px |
| but not where either | 982 px |
| had finally sunk. | 784 px |

It supplied a Swift/CoreText snippet for measuring Chalkboard SE Bold on macOS. It identified these exception boundaries: `where | Franklin's` (open subordinate clause), `crews | had` (subject–predicate split), and `either | had` (same issue in the second subordinate clause); it said the other boundaries are natural. It scoped the exception to this sentence only and required a PASS using the actual font.

## Local font check and decision

The production machine has `/System/Library/Fonts/Supplemental/ChalkboardSE.ttc`, index 2, at 84 px. Pillow `getlength()` against the exact production font measured the following five-group plan; all are below the profile's 1298 px safe width:

| Group | Chalkboard SE Bold width |
|---|---:|
| Before Erebus was found, | 1027.0 px |
| searchers knew where | 894.1 px |
| Franklin's crews had abandoned | 1273.9 px |
| the ships, but not where | 995.9 px |
| either had finally sunk. | 949.9 px |

Use these five groups. This preserves every word and punctuation, uses the fewest groups that fit the width, and avoids the subject–predicate breaks in ChatGPT's six-group recommendation. Two forced boundaries remain: `where | Franklin's` and `abandoned | the ships`. Both have user approval in `CAPTION_EXCEPTION_APPROVAL.md`; the full line sequence must still be reviewed in the subtitle sample. The local width measurement is a text-metrics check, not rendered-pixel or screen-coverage QA.
