#!/usr/bin/env python3
"""
Normalize research folder structure and add front-matter to all files.
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

# Standard file names expected
STANDARD_FILES = [
    "01_overview.md",
    "02_architecture.md", 
    "03_prompt_design.md",
    "04_codebase_setup.md",
    "05_enhancements.md"
]

# Mapping of old names to new names
RENAME_MAP = {
    "02_architecture-deep-dive.md": "02_architecture.md",
    "03_codebase-setup.md": "04_codebase_setup.md",
    "04_prompt-structure.md": "03_prompt_design.md"
}

def add_front_matter(file_path, topic, model):
    """Add front-matter to a markdown file if it doesn't have one."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has front-matter
    if content.startswith('---'):
        return False
    
    # Add front-matter
    front_matter = f"""---
topic: "{topic}"
model: "{model}"
stage: research
version: 1
---

"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(front_matter + content)
    
    return True

def normalize_research_folder(research_dir, topic):
    """Normalize a research directory structure."""
    for model_dir in ["o3", "claude-4-sonnet", "claude-4-opus"]:
        model_path = Path(research_dir) / model_dir
        if not model_path.exists():
            print(f"Creating {model_path}")
            model_path.mkdir(parents=True, exist_ok=True)
        
        # Rename files to standard format
        for old_name, new_name in RENAME_MAP.items():
            old_path = model_path / old_name
            new_path = model_path / new_name
            if old_path.exists() and not new_path.exists():
                print(f"Renaming {old_path} -> {new_path}")
                shutil.move(str(old_path), str(new_path))
        
        # Add front-matter to all files
        for file_name in STANDARD_FILES:
            file_path = model_path / file_name
            if file_path.exists():
                if add_front_matter(file_path, topic, model_dir):
                    print(f"Added front-matter to {file_path}")
            else:
                # Create missing files with basic template
                print(f"Creating missing file: {file_path}")
                create_template_file(file_path, topic, model_dir, file_name)
        
        # Remove extra files
        for file_path in model_path.glob("*.md"):
            if file_path.name not in STANDARD_FILES:
                print(f"Removing extra file: {file_path}")
                file_path.unlink()

def create_template_file(file_path, topic, model, file_name):
    """Create a template file with front-matter and basic content."""
    title_map = {
        "01_overview.md": "Overview",
        "02_architecture.md": "Architecture Deep Dive",
        "03_prompt_design.md": "Prompt Design",
        "04_codebase_setup.md": "Codebase Setup",
        "05_enhancements.md": "Enhancements and Future Work"
    }
    
    title = title_map.get(file_name, "Research")
    
    content = f"""---
topic: "{topic}"
model: "{model}"
stage: research
version: 1
---

# {topic.replace('-', ' ').title()} {title} - {model.upper()} Analysis

## Overview

[To be completed by {model} model]

## Key Insights

1. **Insight 1**: [Description]
2. **Insight 2**: [Description]
3. **Insight 3**: [Description]

## Technical Details

[Detailed technical analysis]

## Recommendations

[Model-specific recommendations]

---

## DocOps Footer

### Change Log
- **v1.0** ({datetime.now().strftime('%Y-%m-%d')}): Initial research documentation
  - Created template structure
  - Added placeholders for content

### Next Actions
1. Complete detailed analysis
2. Add code examples
3. Include architecture diagrams
4. Document best practices
5. Identify enhancement opportunities
"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Main function to normalize all research folders."""
    # Normalize chatgpt-agent-research
    print("Normalizing chatgpt-agent-research...")
    normalize_research_folder("chatgpt-agent-research", "chatgpt-agent")
    
    # Normalize codebase-generation-prompt-research
    print("\nNormalizing codebase-generation-prompt-research...")
    normalize_research_folder("codebase-generation-prompt-research", "codebase-generation-prompt")
    
    print("\nNormalization complete!")

if __name__ == "__main__":
    main() 