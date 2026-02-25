#!/usr/bin/env python3
"""
Phase 3: 技能文件去冗余 (Skill File De-duplication)

This script:
1. Removes/simplifies redundant license sections from all skill files
2. Simplifies platform installation sections in v2.0+ skill files
   (replaces detailed multi-platform config with a simplified section
    referencing _common/installation.md)
"""

import os
import re
import sys

SKILLS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'skills')
SKILLS_DIR = os.path.abspath(SKILLS_DIR)

# --- License replacement patterns ---

# Pattern 1: v1.0 style "## 📄 License / 许可证" section
V1_LICENSE_PATTERN = re.compile(
    r'\n## 📄 License / 许可证\n\n.*?(?=\Z)',
    re.DOTALL
)
V1_LICENSE_REPLACEMENT = '\n## 📄 License / 许可证\n\nMIT with Attribution — See [LICENSE](../../LICENSE) | [COMMON.md](../../COMMON.md)\n'

# Pattern 2: v2.0 numbered license section "## N. 许可证 / License"
V2_LICENSE_PATTERN = re.compile(
    r'\n## \d+\. 许可证 / License\n\n'
    r'MIT License with Attribution Requirement\n'
    r'Copyright \(c\) 2026 neo\.ai\n\n'
    r'See \[LICENSE\]\([^)]+\) for full text\.\n\n'
    r'\*\*About Author:\*\*\n'
    r'.*?'
    r'(?=\n---\n\n\*\*Tags:\*\*|\Z)',
    re.DOTALL
)
V2_LICENSE_REPLACEMENT = ''  # Remove entirely - tags section follows

# Pattern 2b: Numbered license + About Author, then tags
V2_FULL_LICENSE_PATTERN = re.compile(
    r'\n## \d+\. 许可证 / License\n\n'
    r'MIT License with Attribution Requirement\n'
    r'Copyright \(c\) 2026 neo\.ai\n\n'
    r'See \[LICENSE\]\([^)]+\) for full text\.\n\n'
    r'\*\*About Author:\*\*\n'
    r'(?:- \*\*[^*]+\*\*:.*\n)*'
    r'\n---\n\n',
    re.DOTALL
)

# Pattern 3: "## License / 许可证" (used in some files)
V2B_LICENSE_PATTERN = re.compile(
    r'\n## (?:License|License / 许可证)\n\n'
    r'MIT License with Attribution Requirement.*?'
    r'(?=\Z|\n## )',
    re.DOTALL
)

# Pattern 4: Inline at end of file (e.g. software-architect.md)
INLINE_LICENSE_PATTERN = re.compile(
    r'\n+MIT License with Attribution.*?\| \[LICENSE\]\([^)]+\)\n',
    re.DOTALL
)

# Pattern 5: "## 16. License & Author / 许可证与作者"
V3_LICENSE_PATTERN = re.compile(
    r'\n## 16\. License & Author / 许可证与作者\n\n.*?\Z',
    re.DOTALL
)
V3_LICENSE_REPLACEMENT = '\n## 16. License & Author / 许可证与作者\n\nMIT with Attribution — See [LICENSE](../../LICENSE) | [COMMON.md](../../COMMON.md)\n'


def get_relative_depth(filepath):
    """Calculate relative path depth from skills directory.

    For skills/admin/chef.md -> rel='admin/chef.md' -> parts=['admin','chef.md'] -> depth=2
    To reach project root from skills/admin/chef.md: need '../../' = '../' * 2
    """
    rel = os.path.relpath(filepath, SKILLS_DIR)
    parts = rel.split(os.sep)
    return len(parts)


def get_common_path(filepath):
    """Get relative path to _common/installation.md from the given skill file."""
    depth = get_relative_depth(filepath)
    # To reach skills/_common from skills/category/file.md: '../' * (depth-1) + '_common/'
    # depth-1 = number of directory levels above the file within skills/
    ups = '../' * (depth - 1)
    return f'{ups}_common/installation.md'


def get_license_path(filepath):
    """Get relative path to LICENSE from skill file."""
    depth = get_relative_depth(filepath)
    # To reach project root from skills/category/file.md: '../' * (depth+1)
    # (depth-1) ups to reach skills/, then one more to reach project root
    ups = '../' * depth
    return f'{ups}LICENSE'


def get_common_doc_path(filepath):
    """Get relative path to COMMON.md from skill file."""
    depth = get_relative_depth(filepath)
    ups = '../' * depth
    return f'{ups}COMMON.md'


def remove_license_section(content, filepath):
    """Remove or simplify license section from skill file content."""
    common_path = get_common_doc_path(filepath)
    license_path = get_license_path(filepath)

    modified = False

    # Pattern 5: "## 16. License & Author" (skill-writer style)
    if re.search(r'\n## 16\. License & Author', content):
        new_content = re.sub(
            r'\n## 16\. License & Author / 许可证与作者\n\n.*?\Z',
            f'\n## 16. License & Author / 许可证与作者\n\nMIT with Attribution — See [{license_path}]({license_path}) | [{common_path}]({common_path})\n',
            content,
            flags=re.DOTALL
        )
        if new_content != content:
            return new_content, True

    # Pattern 2: Numbered license section "## N. 许可证 / License" (v2.0 style)
    # This typically ends at the ---\n\n**Tags:** line
    m = re.search(r'\n(## \d+\. 许可证 / License\n)', content)
    if m:
        start = m.start()
        # Find what comes after the license section (tags or end of file)
        rest = content[m.end():]
        # Find end: either "---\n\n**Tags:**" or end of file
        tags_match = re.search(r'(\n---\n\n\*\*Tags:\*\*.*)', rest, re.DOTALL)
        if tags_match:
            # Keep the tags part
            new_content = content[:start] + '\n' + tags_match.group(1)
        else:
            # No tags, just end
            new_content = content[:start] + '\n'
        if new_content != content:
            return new_content, True

    # Pattern for "## License / 许可证" or "## License"
    m = re.search(r'\n(## (?:License|License / 许可证)\n)', content)
    if m:
        start = m.start()
        new_content = content[:start] + '\n'
        if new_content != content:
            return new_content, True

    # Pattern 3: v1.0 style "## 📄 License / 许可证"
    m = re.search(r'\n(## 📄 License / 许可证\n)', content)
    if m:
        start = m.start()
        # Replace with simplified version
        new_content = content[:start] + f'\n## 📄 License / 许可证\n\nMIT with Attribution — See [{license_path}]({license_path})\n'
        if new_content != content:
            return new_content, True

    # Pattern 4: Inline MIT License at end (no header)
    m = re.search(r'\n+MIT License with Attribution.*?(?:\| \[LICENSE\]\([^)]+\))?\n*$', content, re.DOTALL)
    if m:
        new_content = content[:m.start()] + '\n'
        if new_content != content:
            return new_content, True

    return content, False


def simplify_platform_section(content, filepath, skill_name, skill_path):
    """Simplify the platform-specific configuration section."""
    common_install_path = get_common_path(filepath)

    # Build the skill's GitHub URL
    github_url = f'https://github.com/theneoai/awesome-skills/blob/main/{skill_path}'

    simplified_section = f'''
→ 详见 [通用安装指南]({common_install_path})

**快速安装（OpenCode / OpenClaw）：**
```
Read {github_url} and install {skill_name} skill
```
'''

    # Pattern A: "## 4. 平台特定配置 / Platform-Specific Configuration" (most v2 files)
    m = re.search(
        r'(\n## \d+\. 平台特定配置 / Platform-Specific Configuration\n)',
        content
    )
    if m:
        section_start = m.start()
        header = m.group(1)
        # Find next section at same level (##) or end of file
        rest = content[m.end():]
        next_section = re.search(r'\n## ', rest)
        if next_section:
            section_end = m.end() + next_section.start()
            new_content = content[:section_start] + header + simplified_section + content[section_end:]
        else:
            new_content = content[:section_start] + header + simplified_section
        if new_content != content:
            return new_content, True

    # Pattern B: "## N. Platform Installation / 平台安装"
    m = re.search(
        r'(\n## \d+\. Platform Installation / 平台安装\n)',
        content
    )
    if m:
        section_start = m.start()
        header = m.group(1)
        rest = content[m.end():]
        next_section = re.search(r'\n## ', rest)
        if next_section:
            section_end = m.end() + next_section.start()
            new_content = content[:section_start] + header + simplified_section + content[section_end:]
        else:
            new_content = content[:section_start] + header + simplified_section
        if new_content != content:
            return new_content, True

    # Pattern C: v2.0 CEO style "## 4. 平台特定配置" - same as A but just in case

    return content, False


def process_skill_file(filepath):
    """Process a single skill file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    content = original_content
    changes = []

    # Calculate relative path from skills dir
    rel_path = os.path.relpath(filepath, SKILLS_DIR)

    # Extract skill name from frontmatter or filename
    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    if name_match:
        skill_name = name_match.group(1).strip()
    else:
        skill_name = os.path.splitext(os.path.basename(filepath))[0]

    # Check if this is a v2.0+ file with platform installation section
    has_platform_section = bool(re.search(
        r'\n## \d+\. 平台特定配置 / Platform-Specific Configuration\n|\n## \d+\. Platform Installation / 平台安装\n',
        content
    ))

    # 1. Simplify platform section (for v2.0+ files only)
    if has_platform_section:
        # rel_path is like "executive/ceo.md"
        content, changed = simplify_platform_section(content, filepath, skill_name, f'skills/{rel_path}')
        if changed:
            changes.append('simplified platform section')

    # 2. Remove/simplify license section
    content, changed = remove_license_section(content, filepath)
    if changed:
        changes.append('cleaned license section')

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes

    return False, []


def main():
    """Process all skill files."""
    total = 0
    modified = 0
    errors = []

    for root, dirs, files in os.walk(SKILLS_DIR):
        # Skip _common directory
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for filename in sorted(files):
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(root, filename)
            total += 1

            try:
                changed, changes = process_skill_file(filepath)
                if changed:
                    modified += 1
                    rel = os.path.relpath(filepath, SKILLS_DIR)
                    print(f'  ✓ {rel}: {", ".join(changes)}')
            except Exception as e:
                rel = os.path.relpath(filepath, SKILLS_DIR)
                errors.append((rel, str(e)))
                print(f'  ✗ {rel}: ERROR - {e}', file=sys.stderr)

    print(f'\nSummary: {modified}/{total} files modified')
    if errors:
        print(f'Errors: {len(errors)}')
        for path, err in errors:
            print(f'  - {path}: {err}')
    return len(errors)


if __name__ == '__main__':
    sys.exit(main())
