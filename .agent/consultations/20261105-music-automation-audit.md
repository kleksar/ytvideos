# Music automation audit consultation
Task ID: music-automation-check-20261105
Prompt: For a video workflow that documents approved music and uses an FFmpeg renderer, which concrete evidence distinguishes an automatic rule requiring music in every new film from an editor manually supplying a prepared audio mix? Answer concisely without assumptions about any specific codebase.
Status: prepared.
URL: https://chatgpt.com/c/6aecdc80-c50c-83ed-8f2d-11f2304d5716
Visible effort: Extra High; model name not separately displayed. Exact prompt posted and composer empty, lock released VERIFIED. The response initially failed to load; reopened under lock and recovered with the visible load-again control without resending. Completed answer transcribed from visible UI:

The distinction is established by the source of the audio input and where the requirement is enforced.

Evidence: project configuration — automatic music requirement enabled by default or enforced globally versus explicit audio path or mix supplied per project; validation — missing music causes validation/render failure versus missing optional audio accepted or handled manually; renderer invocation — pipeline resolves/selects music automatically versus FFmpeg receives an explicitly prepared mix; catalog integration — approved catalog queried by workflow versus editor selects tracks and prepares the mix; tests — new project without audio still gets music automatically or is rejected versus tests verify supplied mix is rendered correctly; provenance — logs identify automatic selection and source assets versus editor-provided file and hash.

Strongest practical verification: create a clean new film project without supplying an audio file; run normal production workflow; inspect generated render, FFmpeg arguments and execution logs; establish whether music was automatically selected and incorporated, or whether renderer simply consumed an explicitly supplied mix.

Important distinction: a mandatory validation rule proves music is required. Automatic catalog selection proves music is automatically assigned. An FFmpeg -i music.wav argument proves only that FFmpeg received an audio input. It does not establish who selected or prepared it. Documentation, an approved music catalog, and an FFmpeg capability alone do not prove that every new film automatically receives music.

Decision: read the actual production rule and renderer and report the difference; no new project or render because the user requested read-only inspection.
