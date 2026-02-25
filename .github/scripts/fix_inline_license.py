#!/usr/bin/env python3
"""Fix inline author/license patterns in skill files."""
import os
import re

SKILLS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'skills')
SKILLS_DIR = os.path.abspath(SKILLS_DIR)

fixed = 0

for root, dirs, files in os.walk(SKILLS_DIR):
    dirs[:] = [d for d in dirs if not d.startswith('_')]
    for f in files:
        if not f.endswith('.md'):
            continue
        path = os.path.join(root, f)
        with open(path) as fh:
            content = fh.read()

        # Pattern: inline author/license at very end of file
        # "**Author**: neo.ai 🤖 | **License**: MIT with Attribution"
        new_content = re.sub(
            r'\n\*\*Author\*\*:.*?\| \*\*License\*\*: MIT with Attribution\n*$',
            '\n',
            content
        )

        if new_content != content:
            with open(path, 'w') as fh:
                fh.write(new_content)
            fixed += 1

print(f'Fixed {fixed} files with inline author/license pattern')
