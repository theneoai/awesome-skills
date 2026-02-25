#!/usr/bin/env python3
"""Fix second variant of inline author/license patterns in skill files."""
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

        original = content

        # Pattern 1: "**Author / 作者**: neo.ai 🤖 | **License / 许可证**: MIT with Attribution"
        content = re.sub(
            r'\n\*\*Author / 作者\*\*:.*?\| \*\*License / 许可证\*\*: MIT with Attribution\n*$',
            '\n',
            content
        )

        # Pattern 2: Any remaining inline MIT with Attribution at end
        content = re.sub(
            r'\n[^\n]*MIT with Attribution\n*$',
            '\n',
            content
        )

        if content != original:
            with open(path, 'w') as fh:
                fh.write(content)
            fixed += 1

print(f'Fixed {fixed} files')
