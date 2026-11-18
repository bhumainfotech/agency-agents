#!/usr/bin/env python3
"""Regenerate references/<category>.md from library/videos.json."""
import json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NAMES = {"motion": "Motion graphics", "3d": "3D scenes", "explainer": "Explainers", "interactive": "Games & interactive"}

items = json.load(open(os.path.join(ROOT, "library", "videos.json"), encoding="utf-8"))
for cat, title in NAMES.items():
    rows = sorted([i for i in items if i["category"] == cat], key=lambda i: (i["prompt_partial"], i["slug"]))
    out = [
        f"# {title} ({len(rows)} prompts)\n",
        "One line per prompt: `slug` · tech tags · first words of the prompt. Entries marked *(partial)* only have the creator's post text, not a full prompt.",
        "Open the full prompt with `python3 scripts/find_prompt.py --show <slug>` or read `library/prompts/<slug>.md`.\n",
    ]
    for i in rows:
        p = " ".join((i["prompt"] or "").split()).replace("|", "/").replace("`", "'")
        p = p[:140] + ("…" if len(p) > 140 else "")
        part = " *(partial)*" if i["prompt_partial"] else ""
        out.append(f"- `{i['slug']}` · {', '.join(i['tech_tags'])}{part} · {p}")
    with open(os.path.join(ROOT, "references", f"{cat}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"{cat}: {len(rows)}")
