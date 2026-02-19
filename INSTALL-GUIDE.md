# Awesome Skills — 平台安装指南 / Platform Installation Guide

> 按平台查找安装命令 | Find installation commands by platform

---

## 目录 / Contents

- [OpenCode / OpenClaw（推荐）](#opencode--openclaw推荐)
- [Claude Code](#claude-code)
- [Cursor](#cursor)
- [OpenAI Codex](#openai-codex)
- [Cline](#cline)
- [Kimi Code](#kimi-code)
- [热门技能速查](#热门技能速查)
- [技能目录](#技能分类目录)

---

## OpenCode / OpenClaw（推荐）

OpenCode 和 OpenClaw 原生支持技能安装，使用 `Read ... and install` 命令。

### 安装单个技能
```
Read https://github.com/theneoai/awesome-skills/blob/main/skills/executive/ceo.md and install ceo skill
```

### 安装技能包
```
Read https://github.com/theneoai/awesome-skills/blob/main/packages/executive.md and install executive package
```

### 安装全部技能
```
Read https://theneoai.github.io/awesome-skills/INSTALL.md and install all skills
```

**技能存储位置：**
- OpenClaw: `~/.openclaw/workspace/skills/[skill-name]/SKILL.md`
- OpenCode: `~/.opencode/skills/[skill-name]/SKILL.md`

---

## Claude Code

Claude Code 通过 `CLAUDE.md` 文件或 `/load` 命令加载技能。

### 方法 1：项目级安装（推荐）

将以下内容追加到项目 `CLAUDE.md`：
```bash
cat >> CLAUDE.md << 'EOF'
Read https://github.com/theneoai/awesome-skills/blob/main/skills/executive/ceo.md and apply the CEO skill guidelines to this project.
EOF
```

### 方法 2：单次会话加载
```
Read https://github.com/theneoai/awesome-skills/blob/main/skills/executive/ceo.md and install ceo skill
```

### 方法 3：手动复制 System Prompt

1. 打开技能文件（如 `skills/executive/ceo.md`）
2. 复制 `§1.1 Role Definition` 代码块中的内容
3. 粘贴到 Claude Project 的"Project Instructions"（全局持久化）

**技能存储位置：**
- 项目级：`./CLAUDE.md`
- 全局：Claude Project Instructions（需要 Claude.ai 账户）

---

## Cursor

Cursor 通过 `.cursorrules` 文件应用技能。

### 安装单个技能

```bash
# 方法 1：命令行追加
curl -s https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/executive/ceo.md >> .cursorrules

# 方法 2：在 Cursor 内提示
Read https://github.com/theneoai/awesome-skills/blob/main/skills/executive/ceo.md and append the skill rules to .cursorrules
```

### 安装多个技能

```bash
for skill in ceo cto software-architect; do
  curl -s "https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/executive/${skill}.md" >> .cursorrules
  echo "" >> .cursorrules
done
```

**技能存储位置：** `.cursorrules`（项目根目录）

---

## OpenAI Codex

Codex 通过系统提示词（System Prompt）加载技能。

### 安装方式

```
Read https://github.com/theneoai/awesome-skills/blob/main/skills/executive/ceo.md, extract the system prompt and guidelines, and apply as system context for this session.
```

### 持久化安装

1. 打开 Codex 配置文件 `~/.codex/config.yaml`
2. 在 `system_prompt` 字段中粘贴技能的 `§1.1 Role Definition` 内容

> ⚠️ **注意**：Codex 平台的技能持久化依赖具体配置方式，建议参考 Codex 官方文档。

---

## Cline

Cline 通过 MCP 配置或系统提示词加载技能。

### 安装方式

```
Read https://github.com/theneoai/awesome-skills/blob/main/skills/executive/ceo.md and apply the CEO skill to this session.
```

**技能存储位置：** `~/.cline/skills/[skill-name]/cline.md`（需手动创建）

---

## Kimi Code

Kimi Code 与 Cline 类似，支持通过提示词加载技能。

### 安装方式

```
Read https://github.com/theneoai/awesome-skills/blob/main/skills/executive/ceo.md and install ceo skill for this session.
```

> ⚠️ **注意**：Kimi Code 平台适配仍在测试中，安装效果可能因版本而异。

---

## 热门技能速查

| 技能 | 安装命令 |
|------|---------|
| **CEO** | `Read .../skills/executive/ceo.md and install ceo skill` |
| **CTO** | `Read .../skills/executive/cto.md and install cto skill` |
| **CFO** | `Read .../skills/executive/cfo.md and install cfo skill` |
| **Software Architect** | `Read .../skills/software/software-architect.md and install software-architect skill` |
| **Prompt Engineer** | `Read .../skills/ai-ml/prompt-engineer.md and install prompt-engineer skill` |
| **LLM Research Scientist** | `Read .../skills/ai-ml/llm-research-scientist.md and install llm-research-scientist skill` |
| **Clinical Physician** | `Read .../skills/healthcare/clinical-physician.md and install clinical-physician skill` |
| **Legal Counsel** | `Read .../skills/legal/legal-counsel.md and install legal-counsel skill` |

**URL 前缀：** `https://github.com/theneoai/awesome-skills/blob/main/`

---

## 技能分类目录

| 分类 | 路径 | 技能数 |
|------|------|--------|
| 高管 Executive | `skills/executive/` | 4 |
| AI & ML | `skills/ai-ml/` | 9 |
| 软件开发 Software | `skills/software/` | 12+ |
| 金融 Finance | `skills/finance/` | 20+ |
| 医疗 Healthcare | `skills/healthcare/` | 40+ |
| 法律 Legal | `skills/legal/` | 15+ |
| 教育 Education | `skills/education/` | 60+ |
| 创意 Creative | `skills/creative/` | 14+ |
| 网络安全 Cybersecurity | `skills/cybersecurity/` | 10+ |
| 人力资源 HR | `skills/hr/` | 10+ |

**查看全部 464 个技能 → [CATALOG.md](./CATALOG.md)**

---

## 安装验证

安装技能后，用以下方式验证效果：

1. 提问一个该领域的专业问题
2. 检查 AI 是否使用了框架式回答（而非泛泛而谈）
3. 对比安装前后的回答风格

**示例验证问题（CEO 技能）：**
> "我们公司现金流紧张，应该裁员还是融资？"

**期望行为：** AI 提供分析框架（财务指标、利益相关者分析、方案对比），而非直接给出"应该XX"的简单答案。

---

**← [快速安装](./INSTALL.md)** | **[技能目录](./CATALOG.md)** | **[贡献指南](./CONTRIBUTING.md)**
