#!/bin/bash
# .scripts/generate-marketplace.sh

MARKETPLACE_FILE=".claude-plugin/marketplace.json"
mkdir -p .claude-plugin

# 1. Collect the plugins into an array first
plugins_json=$(find . -maxdepth 2 -name "SKILL.md" | while read -r file; do
  dir=$(dirname "$file")
  # Skip root or hidden directories
  [[ "$dir" == "." || "$dir" == "./.scripts" || "$dir" == "./.github" ]] && continue
  
  name=$(basename "$dir")
  # Extract description, defaulting to name if missing
  desc=$(grep -m 1 "description:" "$file" | sed 's/description: //;s/"//g' || echo "Skill for $name")
  
  # Return a JSON object for this plugin
  jq -n --arg n "$name" --arg d "$desc" --arg s "./$dir" \
    '{name: $n, description: $d, source: $s}'
done | jq -s '.')

# 2. Wrap everything in the final schema including the missing 'owner'
jq -n --argjson p "$plugins_json" '{
  name: "JetBrains-Skills",
  description: "Curated agent skills collection",
  owner: {
    name: "JetBrains"
  },
  plugins: $p
}' > $MARKETPLACE_FILE
