# linkedin-post-writer-and-validator

A Claude Code skill for writing and validating LinkedIn posts optimized for reach.

---

## The problem

Most people who sit down to write a LinkedIn post get stuck — not because they don't have something to say, but because they don't know *how* to say it in a way that actually gets read.

They write something honest and thoughtful, hit publish, and get 12 impressions.

Meanwhile, posts that feel shallower somehow reach thousands.

The gap isn't authenticity — it's structure. LinkedIn's algorithm rewards specific patterns: a hook that stops the scroll, white space that invites mobile readers, a closing question that pulls comments. Without knowing these patterns, good ideas get buried.

On top of that, LinkedIn silently penalizes posts that contain URLs — even implied ones. A pattern like `bit.ly` or `go.co` in the body of a post is auto-hyperlinked by LinkedIn and triggers a reach penalty of up to 60%. Most people never know why their post underperformed.

---

## What this skill does

This is a **Claude Code skill** — install it once, and Claude knows how to help you write and validate LinkedIn posts in any conversation.

**Writing:** Claude guides you through a proven post structure (hook → problem → solution → proof → CTA), adapted for Hebrew or English, with formatting rules tuned for mobile and LinkedIn's 2026 Interest Graph algorithm.

**Validation:** Before you post, a Python script (`validate_post.py`) scans your draft with regex and flags anything that will hurt reach:

- Explicit URLs in the body (`http://`, `www.`)
- Implied URLs — `word.word` patterns LinkedIn auto-hyperlinks (e.g. `bit.ly`, `go.co`)
- Em dashes `—`, en dashes `–`, semicolons `;`, and curly quotes `“ ”` (typography noise)
- Bullet points instead of numbered lists
- Engagement bait phrases
- More than 5 hashtags or @mentions
- AI "tells" (warnings): machine-lexicon words (tapestry, symphony, leverage / מארג, סימפוניה, למנף), academic transition phrases (Furthermore / יתרה מכך), manufactured confidence phrases ("Here's the thing" / "הנה העניין"), and the negation-contrast structure ("not X, not Y... it's Z")

---

## This is meant to inspire

This skill is published as-is, as a starting point. Fork it. Adapt the rules to your voice, your audience, your language. Add your own hook templates, your own avoid-list, your own validation checks.

The goal isn't to make every post sound the same — it's to remove the invisible friction between a good idea and a post that actually reaches people.

---

## Install

```bash
npx skills add NetanelRotem/linkedin-post-writer-and-validator
```

Requires [Claude Code](https://claude.ai/code).

---

## Validate a post manually

```bash
python validate_post.py my-post.txt
```

Or pipe directly:

```bash
echo "your post text here" | python validate_post.py
```

Exit code `0` = clean. Exit code `1` = errors found.
