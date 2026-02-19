## New Skill: [Skill Name] / 新技能：[技能名称]

### Skill Info / 技能信息

| Field | Value |
|-------|-------|
| **File** | `skills/[category]/[skill-name].md` |
| **Category** | |
| **Difficulty** | expert / intermediate / beginner |
| **Quality Tier** | ⭐ Expert Verified / ✅ Community Verified / 📝 Basic |

---

### Checklist / 提交前检查

**Frontmatter (YAML metadata)**
- [ ] `name`: lowercase, hyphen-separated
- [ ] `display_name`: bilingual (English / 中文)
- [ ] `author`: your GitHub username
- [ ] `version`: `1.0.0`
- [ ] `difficulty`: expert / intermediate / beginner
- [ ] `category`: matches directory name
- [ ] `tags`: 3-5 searchable tags
- [ ] `platforms`: list of supported platforms
- [ ] `description`: 1-3 sentences (no HTML comments in frontmatter)

**Content Structure (for ⭐ Expert Verified)**
- [ ] `## 1. System Prompt` with `### 1.1 Role Definition` code block
- [ ] `### 1.2 Decision Framework` with evaluation gate table
- [ ] `### 1.3 Thinking Patterns` table
- [ ] `## 2. What This Skill Does` with 5+ specific capabilities
- [ ] `## 3. Risk Disclaimer` with 4+ domain-specific risks
- [ ] At least 3 professional frameworks in `## 4-6`
- [ ] At least 3 scenario examples with input/output in `## 7`
- [ ] Platform installation commands in `## 8`

**Quality Bar**
- [ ] Validator passes: `python3 .github/scripts/validate_skills.py skills/[path]`
- [ ] AI behavior measurably changes after installing this skill (tested manually)
- [ ] Content is domain-specific, not generic template text

---

### Description / 描述

**What does this skill do?**

**Who should install it?**

**What's the key behavior change after installing?**

**How did you verify it works?**
