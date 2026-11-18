#!/usr/bin/env python3
"""Search the Opus 5.5 video prompt library.

Usage:
  python3 find_prompt.py "solar system"                 # keyword search (all words must match)
  python3 find_prompt.py --category 3d --tag threejs    # filter by category / tech tag
  python3 find_prompt.py --full-only "explainer"         # skip entries whose prompt is partial
  python3 find_prompt.py --show <slug>                  # print one full prompt
  python3 find_prompt.py --random --category motion     # pick one at random
  python3 find_prompt.py --stats                        # counts per category and tag

Categories: motion, 3d, explainer, interactive
Tags: canvas, svg, threejs, shader, gsap, css, audio, playable, particles,
      pixel, webgl, physics, ai-image
Standard library only; reads ../library/videos.json.
"""
import argparse
import collections
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "library", "videos.json")


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="*", help="keywords matched against prompt, author and slug")
    ap.add_argument("--category", "-c", choices=["motion", "3d", "explainer", "interactive"])
    ap.add_argument("--tag", "-t", action="append", default=[], help="tech tag; repeatable (all must match)")
    ap.add_argument("--full-only", action="store_true", help="only entries with a complete prompt")
    ap.add_argument("--limit", "-n", type=int, default=15)
    ap.add_argument("--show", metavar="SLUG", help="print the full entry for one slug")
    ap.add_argument("--random", action="store_true", help="pick one matching entry at random and show it")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()

    items = load()

    if a.stats:
        print("total", len(items))
        for k, v in collections.Counter(i["category"] for i in items).most_common():
            print(f"category {k}: {v}")
        for k, v in collections.Counter(t for i in items for t in i["tech_tags"]).most_common():
            print(f"tag {k}: {v}")
        return

    if a.show:
        hit = next((i for i in items if i["slug"] == a.show), None)
        if not hit:
            sys.exit(f"no entry with slug {a.show!r}")
        return show(hit)

    words = [w.lower() for w in a.query]
    res = []
    for i in items:
        if a.category and i["category"] != a.category:
            continue
        if any(t not in i["tech_tags"] for t in a.tag):
            continue
        if a.full_only and i["prompt_partial"]:
            continue
        hay = " ".join([i["prompt"] or "", i["author"], i["slug"]]).lower()
        if all(w in hay for w in words):
            res.append(i)

    if not res:
        sys.exit("no matches")
    if a.random:
        return show(random.choice(res))

    print(f"{len(res)} matches" + (f" (showing {a.limit})" if len(res) > a.limit else ""))
    for i in res[: a.limit]:
        p = " ".join((i["prompt"] or "").split())
        flag = " [partial]" if i["prompt_partial"] else ""
        print(f"- {i['slug']} | {i['category']} | {','.join(i['tech_tags'])}{flag}\n    {p[:160]}")


def show(i):
    print(f"slug: {i['slug']}\ncategory: {i['category']}\ntags: {', '.join(i['tech_tags'])}")
    print(f"author: @{i['author']} ({i['post_url']})")
    if i.get("skillry_url"):
        print(f"preview: {i['skillry_url']}")
    print(f"partial: {i['prompt_partial']}\n\n--- prompt ---\n{i['prompt']}")


if __name__ == "__main__":
    main()
