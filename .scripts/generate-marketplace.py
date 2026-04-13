#!/usr/bin/env python3
"""
Crawls top-level skill directories and generates .claude-plugin/marketplace.json.
Requires Python 3.8+, no third-party dependencies.
"""

import json
import os
import re
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
marketplace_file = os.path.join(repo_root, ".claude-plugin", "marketplace.json")

os.makedirs(os.path.join(repo_root, ".claude-plugin"), exist_ok=True)


def extract_frontmatter_field(skill_md: str, field: str) -> str:
    """Extract a scalar value from YAML frontmatter, handling quoted and block values."""
    in_frontmatter = False
    lines = skill_md.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break  # end of frontmatter
        if not in_frontmatter:
            continue
        m = re.match(rf'^{re.escape(field)}:\s*(.*)', line)
        if m:
            value = m.group(1).strip()
            # Strip YAML block scalars (>-, |-, >, |) and quotes
            value = re.sub(r'^[>|][+-]?\s*', '', value)
            value = re.sub(r'^["\']|["\']$', '', value)
            if value:
                return value
            # Multi-line block scalar: collect next non-empty indented line
            for cont in lines[i + 1:]:
                if cont.startswith(" ") or cont.startswith("\t"):
                    return cont.strip()
                if cont.strip():
                    break
    return ""


plugins = []
entries = sorted(os.listdir(repo_root))

for name in entries:
    path = os.path.join(repo_root, name)
    if not os.path.isdir(path) or name.startswith("."):
        continue
    skill_md_path = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md_path):
        continue

    with open(skill_md_path, encoding="utf-8", errors="replace") as f:
        content = f.read()

    description = extract_frontmatter_field(content, "description")
    if not description:
        description = extract_frontmatter_field(content, "metadata.short-description")
    if not description:
        description = "No description provided"

    plugins.append({
        "name": name,
        "description": description,
        "source": f"./{name}",
    })

catalog = {
    "name": "JetBrains-Skills-Marketplace",
    "plugins": plugins,
}

with open(marketplace_file, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Generated {marketplace_file} with {len(plugins)} skills.")
