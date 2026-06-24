"""
LinkedIn Post Validator
Usage:
    python validate_post.py post.txt
    echo "post text" | python validate_post.py
    python -c "from validate_post import validate_post; print(validate_post('your text'))"
"""

import re
import sys


RULES = [
    {
        "id": "explicit_url",
        "label": "Explicit URL in body",
        "pattern": re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE),
        "severity": "error",
        "message": lambda m: f"Found explicit URL(s): {', '.join(m)} → move to first comment",
    },
    {
        "id": "implied_url",
        "label": "Implied URL (word.word LinkedIn auto-links)",
        # Two+ letter/digit sequences joined by a dot — LinkedIn hyperlinks these automatically
        "pattern": re.compile(r"\b[a-zA-Z0-9]+(?:\.[a-zA-Z]{2,})+\b"),
        "filter": lambda match: not match.startswith("#") and "@" not in match,
        "severity": "warning",
        "message": lambda m: f"Found implied URL(s): {', '.join(m)} → rewrite to avoid dot-separated patterns",
    },
    {
        "id": "em_dash",
        "label": "Em dash (—)",
        "pattern": re.compile(r"—"),
        "severity": "error",
        "message": lambda m: f"Found {len(m)} em dash(es) — replace with a comma, period, or line break",
    },
    {
        "id": "bullet_points",
        "label": "Bullet points (use numbered lists only)",
        # Lines starting with •, ·, *, or - followed by a space
        "pattern": re.compile(r"^[ \t]*[•·\-\*][ \t]+", re.MULTILINE),
        "severity": "error",
        "message": lambda m: f"Found {len(m)} bullet point(s) — convert to numbered list (1. 2. 3.)",
    },
    {
        "id": "engagement_bait",
        "label": "Engagement bait phrases",
        "pattern": re.compile(
            r"\b(like if|share (this|for)|comment yes|tag (a |someone|your)|repost if)\b",
            re.IGNORECASE,
        ),
        "severity": "error",
        "message": lambda m: f"Found engagement bait: {', '.join(m)} → remove or rewrite",
    },
    {
        "id": "hashtag_count",
        "label": "Too many hashtags (max 5)",
        "pattern": re.compile(r"#[\wא-ת]+"),
        "threshold": 5,
        "severity": "error",
        "message": lambda m: f"Found {len(m)} hashtags — reduce to 3-5 max",
    },
    {
        "id": "mentions_count",
        "label": "Too many @mentions (max 5)",
        "pattern": re.compile(r"@\w+"),
        "threshold": 5,
        "severity": "error",
        "message": lambda m: f"Found {len(m)} @mentions — reduce to 5 max to avoid spam flag",
    },
]


def validate_post(text: str) -> dict:
    """
    Validate a LinkedIn post text against all rules.

    Returns:
        {
            "valid": bool,
            "errors": [str, ...],
            "warnings": [str, ...]
        }
    """
    errors = []
    warnings = []

    for rule in RULES:
        raw_matches = rule["pattern"].findall(text)

        # Apply optional per-rule filter
        if "filter" in rule:
            raw_matches = [m for m in raw_matches if rule["filter"](m)]

        if not raw_matches:
            continue

        # Rules with a count threshold only fire when the threshold is exceeded
        if "threshold" in rule and len(raw_matches) <= rule["threshold"]:
            continue

        msg = f"[{rule['label']}] {rule['message'](raw_matches)}"

        if rule["severity"] == "warning":
            warnings.append(msg)
        else:
            errors.append(msg)

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    result = validate_post(text)

    if result["valid"] and not result["warnings"]:
        print("✓ Post passed all validation checks.")
        sys.exit(0)

    if result["errors"]:
        print("\n❌ ERRORS (must fix before posting):")
        for e in result["errors"]:
            print(f"  • {e}")

    if result["warnings"]:
        print("\n⚠  WARNINGS (review these):")
        for w in result["warnings"]:
            print(f"  • {w}")

    sys.exit(1 if result["errors"] else 0)


if __name__ == "__main__":
    main()
