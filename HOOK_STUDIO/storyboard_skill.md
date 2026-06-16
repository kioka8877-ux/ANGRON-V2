---
name: angron-storyboard
description: >
  Animation storyboard validation gate for the ANGRON-V2 manimgl video pipeline.
  Use this skill whenever the user says "storyboard cycle XXX", "lance le storyboard",
  "valide les animations", "prépare les scènes", or invokes /angron-storyboard.
  This skill MUST be used before creating any scenes_XXX.py file for CRUOR — it is
  the mandatory gate between F02_LACERAT (audio/timestamps) and F03_CRUOR (manimgl render).
  It reads the script and timestamps from GitHub, calls an LLM oracle to propose 10 scene
  concepts for portrait 1080x1920 vertical video, presents textual croquis for operator
  approval, then generates and pushes the validated scenes_XXX.py file.
---

# ANGRON-V2 — Storyboard Gate (F02.5)

This skill is the validation checkpoint between audio production (LACERAT) and manimgl rendering (CRUOR). Its job is to ensure the operator has approved the animation design BEFORE a single frame is rendered. Never skip this gate.

## When invoked

The operator will provide:
- A GitHub token (ghp_...)
- A cycle ID (e.g., "004", "005")
- Optionally: the repo name (default: `kioka8877-ux/ANGRON-V2`)

## Step 1 — Read source materials from GitHub

Using the GitHub API with the provided token, fetch these files:

```
GET /repos/{owner}/{repo}/contents/.angron/ledger.json
GET /repos/{owner}/{repo}/contents/F01_SANGUIS/OUT/  (list, find script_{cycle}.md)
GET /repos/{owner}/{repo}/contents/F02_LACERAT/OUT/  (list, find timestamps_{cycle}.json or similar)
```

Decode the base64 content of each file. If timestamps file does not exist, look for any JSON file in F02_LACERAT/OUT/ that contains timing data.

Parse:
- `ledger.json` → current cycle ID, mode (hook/math_script/math_no_script), format (short/long)
- Script content → full narration text, sections, tone
- Timestamps → list of segments with start_time, end_time, text

## Step 2 — Call the LLM oracle

Call the AI Gateway to get animation proposals. The oracle's role is to think like a visual storyteller who knows manimgl well.

```python
import os, requests, json

response = requests.post(
    f"{os.environ['AI_GATEWAY_BASE_URL']}/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['AI_GATEWAY_API_KEY']}",
        "Content-Type": "application/json"
    },
    json={
        "model": "anthropic/claude-sonnet-4.6",
        "max_tokens": 4000,
        "messages": [{
            "role": "user",
            "content": ORACLE_PROMPT  # see below
        }]
    }
)
```

**ORACLE_PROMPT template:**

```
You are a manimgl animation director for short-form vertical video (1080x1920, 9:16).
The video engine is manimgl v1.7.2 with InteractiveScene.

Available primitives (use these, not others):
- Text(string, font="Liberation Sans", weight=BOLD, font_size=N)
- Tex(r"latex without dollar signs") — ONLY for math equations
- Write(mobject), FadeIn(mobject), FadeOut(mobject) — one object at a time
- GrowArrow(arrow), GrowFromCenter(shape)
- Transform(old, new), ReplacementTransform(old, new)
- Circle, Rectangle, Arrow, Line, Dot, NumberLine
- VGroup for grouping, .arrange(DOWN/RIGHT, buff=N)
- self.play(..., run_time=N)
- self.wait(N)

Frame constraints (portrait 4.5 units wide x 8.0 units tall):
- Font sizes: titles max 52, body max 40, labels max 28
- Never put more than 3 text elements side by side
- Vertical spacing: use buff=0.4 minimum between elements

Script content:
{SCRIPT}

Timestamps (seconds):
{TIMESTAMPS}

Mode: {MODE}
Format: {FORMAT}

Produce EXACTLY 10 scene proposals. Each proposal must be a JSON object in this array:
[
  {
    "scene_id": "S01",
    "class_name": "S01HookQuestion",
    "title": "Short title",
    "duration_s": 8,
    "concept": "One sentence describing what the viewer sees",
    "storyboard": "ASCII sketch of the layout (use | - + chars)",
    "primitives": ["Write", "FadeIn", "GrowArrow"],
    "mobjects": ["title_text", "arrow_left", "arrow_right"],
    "entry": "How elements appear",
    "exit": "How elements leave (FadeOut each one)",
    "why": "Why this animation serves the narration at this timestamp"
  }
]

Return ONLY the JSON array, no prose.
```

Fill in `{SCRIPT}`, `{TIMESTAMPS}`, `{MODE}`, `{FORMAT}` from the fetched materials.

## Step 3 — Present 10 croquis to the operator

Parse the oracle's JSON array. For each of the 10 scenes, format a readable croquis block:

```
╔══════════════════════════════════════════════╗
║  S01 — HookQuestion  (8s)                   ║
╠══════════════════════════════════════════════╣
║  CONCEPT                                     ║
║  Texte de la question apparait mot par mot   ║
║                                              ║
║  LAYOUT                                      ║
║  ┌────────────────────┐                      ║
║  │   "Pourquoi ?"     │  ← Write()          ║
║  │   ────────────     │                      ║
║  │   sous-titre       │  ← FadeIn()         ║
║  └────────────────────┘                      ║
║                                              ║
║  PRIMITIVES : Write, FadeIn, self.wait       ║
║  MOBJECTS   : question_text, subtitle        ║
║  SORTIE     : FadeOut chaque element         ║
║  POURQUOI   : Hook visuel avant la demo      ║
╚══════════════════════════════════════════════╝
```

Display all 10 croquis in sequence, then use AskUserQuestion to collect feedback:

```
Questions:
1. "Validez-vous les 10 scenes telles quelles, ou y a-t-il des corrections ?"
   Options: ["Valider tout", "Modifier certaines scenes", "Refaire les propositions"]

2. If "Modifier certaines scenes": "Quelles scenes modifier et comment ?"
   (free text via Other option)
```

If the operator asks for changes, update the relevant scene proposals in the array and re-present the modified croquis before asking for final confirmation.

If the operator asks to redo proposals entirely, call the oracle again with additional instructions appended to the prompt describing what was wrong.

## Step 4 — Generate scenes_XXX.py

Once the operator validates, generate the complete Python file.

### File structure

```python
from manimlib import *

# ── S01 ──────────────────────────────────────────────────────────────
class S01HookQuestion(InteractiveScene):
    CONFIG = {
        "camera_config": {
            "pixel_width": 1080,
            "pixel_height": 1920,
            "fps": 60,
        },
    }

    def construct(self):
        # ... animations based on approved croquis ...
        self.play(*[FadeOut(m) for m in list(self.mobjects)])
```

### Critical constraints (enforce these without exception)

| Rule | Correct | Wrong |
|------|---------|-------|
| Import | `from manimlib import *` | `from manim import *` |
| Base class | `InteractiveScene` | `Scene` |
| Resolution | `CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}` on EVERY class | Missing CONFIG |
| Regular text | `Text("hello", font="Liberation Sans", weight=BOLD, font_size=40)` | `Tex("hello")` |
| Math text | `Tex(r"F = \rho v^2")` — no dollar signs | `Tex(r"$F = \rho v^2$")` |
| FadeOut | `self.play(*[FadeOut(m) for m in list(self.mobjects)])` | `self.play(FadeOut(a, b, c))` |
| FadeOut single | `self.play(FadeOut(obj))` | never multi-arg |
| Arrows | ASCII only in scripts (`->`) | Unicode `→` causes bash breakage |
| Frame width | keep elements within x ∈ [-2.0, 2.0] | x > 2.2 clips off-screen |

### Scene naming

Class names must match exactly what the oracle proposed: `S01HookQuestion`, `S02FootKick`, etc. The render script detects them by alphabetical order.

### End of each scene

Every `construct()` method must end with:
```python
self.wait(0.5)
self.play(*[FadeOut(m) for m in list(self.mobjects)])
```

## Step 5 — Push to GitHub

Push `scenes_{cycle}.py` to `F03_CRUOR/CODEBASE/scenes_{cycle}.py` in the repo using the GitHub API:

```
PUT /repos/{owner}/{repo}/contents/F03_CRUOR/CODEBASE/scenes_{cycle}.py
```

Payload:
```json
{
  "message": "[STORYBOARD] scenes_{cycle}.py — {N} scenes validated",
  "content": "<base64 of file>",
  "sha": "<existing SHA if file exists, omit if new>"
}
```

Check if the file already exists first with a GET request to get its SHA. If it exists, include the SHA in the PUT to avoid conflicts.

## Step 6 — Confirm to operator

After a successful push, report:

```
Storyboard cycle {cycle} valide et pousse.

  scenes_{cycle}.py -> F03_CRUOR/CODEBASE/
  {N} scenes : S01 ... S{N}
  Total estime : ~{sum of duration_s}s

Prochaine etape : dispatcher le workflow CRUOR.
```

## Error handling

- If ledger.json is missing or projet_actif is null: ask the operator for the cycle ID explicitly
- If the oracle returns malformed JSON: retry once with "Return ONLY valid JSON array, no markdown, no prose" prepended
- If a GitHub push fails with 409 (conflict): fetch the current SHA and retry
- If AI Gateway returns 403 (model_access_denied): stop immediately and report it — do not retry with a different model

## Persistence note

This skill file is stored in the GitHub repo at `HOOK_STUDIO/storyboard_skill.md`. When this sandbox is reset, reinstall with:
```bash
mkdir -p ~/.claude/skills/angron-storyboard
# copy storyboard_skill.md content to ~/.claude/skills/angron-storyboard/SKILL.md
```
