#!/usr/bin/env python3
"""
Fix missing YAML frontmatter fields in skill files (Phase 1 — Metadata normalization).

Automatically infers and fills:
  - category   (from directory name)
  - name       (from file stem, if missing)
  - difficulty (from section count heuristic; defaults to "intermediate")
  - platforms  (defaults to full 7-platform list)
  - tags       (from category mapping + skill name)

Usage:
    python3 .github/scripts/fix_frontmatter_fields.py [--dry-run] [path ...]
"""

import sys
import re
import argparse
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent.parent / "skills"

ALL_PLATFORMS = "[opencode, openclaw, claude, cursor, codex, cline, kimi]"

# Category → default tags mapping
CATEGORY_TAGS: dict[str, list[str]] = {
    "admin":             ["administration", "operations", "management"],
    "aerospace":         ["aerospace", "engineering", "aviation"],
    "agriculture":       ["agriculture", "farming", "sustainability"],
    "ai-ml":             ["ai", "machine-learning", "data-science"],
    "automotive":        ["automotive", "engineering", "manufacturing"],
    "biotech":           ["biotech", "life-sciences", "research"],
    "blockchain":        ["blockchain", "web3", "cryptocurrency"],
    "business":          ["business", "strategy", "management"],
    "construction":      ["construction", "engineering", "project-management"],
    "construction-worker":["construction", "skilled-trades", "labor"],
    "content":           ["content", "writing", "marketing"],
    "crafts":            ["crafts", "skilled-trades", "artisan"],
    "creative":          ["creative", "design", "arts"],
    "cybersecurity":     ["cybersecurity", "security", "risk-management"],
    "data":              ["data", "analytics", "data-science"],
    "education":         ["education", "teaching", "learning"],
    "energy":            ["energy", "sustainability", "engineering"],
    "entertainment":     ["entertainment", "creative", "media"],
    "environmental":     ["environment", "sustainability", "research"],
    "executive":         ["executive", "leadership", "strategy"],
    "factory-worker":    ["manufacturing", "operations", "labor"],
    "farmer":            ["agriculture", "farming", "sustainability"],
    "finance":           ["finance", "analysis", "investment"],
    "freelancer":        ["freelance", "business", "consulting"],
    "government":        ["government", "policy", "public-sector"],
    "healthcare":        ["healthcare", "medicine", "clinical"],
    "hospitality":       ["hospitality", "service", "customer-experience"],
    "hr":                ["hr", "people-management", "recruiting"],
    "international":     ["international", "global", "cross-cultural"],
    "it-support":        ["it-support", "technical-support", "operations"],
    "legal":             ["legal", "compliance", "risk-management"],
    "logistics":         ["logistics", "supply-chain", "operations"],
    "management":        ["management", "leadership", "strategy"],
    "manufacturing":     ["manufacturing", "engineering", "operations"],
    "marketing":         ["marketing", "growth", "strategy"],
    "media":             ["media", "content", "communications"],
    "nonprofit":         ["nonprofit", "social-impact", "management"],
    "product":           ["product", "strategy", "user-experience"],
    "real-estate":       ["real-estate", "investment", "property"],
    "research":          ["research", "analysis", "methodology"],
    "retail":            ["retail", "customer-experience", "operations"],
    "sales":             ["sales", "business-development", "crm"],
    "science":           ["science", "research", "analysis"],
    "security":          ["security", "risk-management", "compliance"],
    "social-work":       ["social-work", "counseling", "community"],
    "software":          ["software", "engineering", "development"],
    "sports":            ["sports", "coaching", "performance"],
    "transportation":    ["transportation", "logistics", "operations"],
    "travel":            ["travel", "hospitality", "planning"],
    "wellness":          ["wellness", "health", "coaching"],
}

# Skills with known expert-level content
EXPERT_SKILLS = {
    "ceo", "cto", "skill-writer", "software-architect", "prompt-engineer"
}


def count_h2_sections(body: str) -> int:
    return len(re.findall(r"^##\s+\S", body, re.MULTILINE))


def infer_difficulty(fm: dict, body: str) -> str:
    """Heuristic: expert > 8 sections, intermediate = 3-8, beginner < 3."""
    name = fm.get("name", "")
    if name in EXPERT_SKILLS:
        return "expert"
    sections = count_h2_sections(body)
    if sections >= 8:
        return "expert"
    elif sections >= 3:
        return "intermediate"
    else:
        return "beginner"


def infer_tags(category: str, skill_name: str) -> str:
    base_tags = CATEGORY_TAGS.get(category, ["professional", "expert"])
    # Derive a skill-specific tag from the file name
    skill_tag = skill_name.replace("-", " ").split()[0] if skill_name else ""
    # Avoid duplicating existing tags
    if skill_tag and skill_tag not in base_tags and len(skill_tag) > 2:
        tags = base_tags[:2] + [skill_tag]
    else:
        tags = base_tags[:3]
    return "[" + ", ".join(tags) + "]"


def parse_and_patch_frontmatter(content: str, path: Path) -> tuple[str, bool]:
    """
    Parse frontmatter, fill missing fields, return (new_content, changed).
    Uses line-by-line reconstruction to preserve original formatting.
    """
    if not content.startswith("---"):
        return content, False

    parts = content.split("---", 2)
    if len(parts) < 3:
        return content, False

    fm_raw, body = parts[1], parts[2]

    # Parse existing fields (simple key: value scan, no full YAML parse)
    existing = {}
    for line in fm_raw.splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if m:
            existing[m.group(1)] = m.group(2).strip()

    # Determine derived values
    category = path.parent.name  # directory name = category
    name = existing.get("name") or path.stem

    patches: dict[str, str] = {}

    if "category" not in existing or not existing["category"]:
        patches["category"] = category

    if "difficulty" not in existing or not existing["difficulty"]:
        patches["difficulty"] = infer_difficulty(existing, body)

    if "platforms" not in existing or not existing["platforms"]:
        patches["platforms"] = ALL_PLATFORMS

    if "tags" not in existing or not existing["tags"]:
        patches["tags"] = infer_tags(category, name)

    if not patches:
        return content, False

    # Reconstruct frontmatter: insert missing fields after `version:` line,
    # or before the closing line if version not present
    lines = fm_raw.splitlines()
    insert_after = -1
    for i, line in enumerate(lines):
        if re.match(r"^version:", line):
            insert_after = i
            break

    insert_lines = []
    for field in ["difficulty", "category", "tags", "platforms"]:
        if field in patches:
            insert_lines.append(f"{field}: {patches[field]}")

    if insert_after >= 0:
        lines = lines[: insert_after + 1] + insert_lines + lines[insert_after + 1 :]
    else:
        lines = lines + insert_lines

    new_fm = "\n".join(lines)
    new_content = "---" + new_fm + "---" + body
    return new_content, True


def fix_file(path: Path, dry_run: bool = False) -> bool:
    content = path.read_text(encoding="utf-8")
    new_content, changed = parse_and_patch_frontmatter(content, path)
    if not changed:
        return False
    if dry_run:
        print(f"[dry-run] Would patch: {path}")
    else:
        path.write_text(new_content, encoding="utf-8")
        print(f"Patched: {path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill missing YAML frontmatter fields.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("paths", nargs="*", default=[str(SKILLS_DIR)])
    args = parser.parse_args()

    files: list[Path] = []
    for t in args.paths:
        p = Path(t)
        if p.is_file() and p.suffix == ".md":
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.rglob("*.md")))

    changed = 0
    for path in files:
        if fix_file(path, dry_run=args.dry_run):
            changed += 1

    action = "Would patch" if args.dry_run else "Patched"
    print(f"\n{action} {changed} of {len(files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
