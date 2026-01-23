# VibeAgent - Agent Guidelines

## Project Overview

**VibeAgent** is an AI agent framework using OpenAgents Control for plan-first development workflows. This repository contains agent configurations, commands, and context files for agentic coding systems.

**Core Philosophy**: Modular, Functional, Maintainable

**Type**: Agent/Configuration Framework (no traditional build/test pipeline)

---

## Build/Test/Lint Commands

This is an **agent configuration repository** (Markdown files, agent definitions, context files). There are **no traditional build/test commands** because this is not a source code project with a compilation pipeline.

### For Agent Development

When modifying agents, commands, or context files:

```bash
# Verify agent file structure (agent files are YAML frontmatter + Markdown)
# Check for valid YAML syntax if editing .opencode/agent/*.md or .opencode/command/*.md

# No npm/yarn build commands - this is documentation/config only
# No Jest/Vitest/Pytest - no executable code to test

# The primary "validation" is ensuring:
# 1. Agent frontmatter is valid (YAML)
# 2. Context file paths resolve correctly (@ references)
# 3. Dependencies are properly declared
```

### For Plugin/Tool Development

If developing in `.opencode/plugin/` or `.opencode/tool/`:

```bash
# Navigate to plugin or tool directory
cd .opencode/plugin  # or .opencode/tool

# Install dependencies (if package.json exists)
npm install

# Run tests (if test framework configured)
npm test

# Lint (if ESLint configured)
npm run lint
```

---

## Code Style Guidelines

### Core Standards (from `.opencode/context/core/`)

**File Location**: `.opencode/context/core/standards/code-quality.md`

| Principle | Practice |
|-----------|----------|
| **Modular** | Single responsibility per module, < 100 lines per component (ideally < 50) |
| **Functional** | Pure functions, immutability, composition over inheritance |
| **Maintainable** | Self-documenting, testable, predictable |

### Critical Patterns

**ALWAYS DO:**
- ✅ Write pure functions (same input = same output, no side effects)
- ✅ Use immutability (create new data, don't modify existing)
- ✅ Keep functions small (< 50 lines)
- ✅ Use explicit dependencies (dependency injection)
- ✅ Handle errors gracefully
- ✅ Validate input at boundaries
- ✅ Use environment variables for secrets
- ✅ Write self-documenting code

**NEVER DO:**
- ❌ Mutation of existing data
- ❌ Side effects in pure functions
- ❌ Deep nesting (> 3 levels) - use early returns
- ❌ God modules (> 200 lines)
- ❌ Global state
- ❌ Hardcoded credentials
- ❌ Expose sensitive info in logs
- ❌ Skip input validation

### Import/Export Conventions

When writing agent/command files in `.opencode/`:

```markdown
---
# YAML frontmatter at top
description: "What this agent/command does"
---

# Context Loading (for commands)
@.opencode/context/core/essential-patterns.md
@[additional context files]

# Markdown content follows
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| **Files** | lowercase-with-dashes | `openagent.md`, `commit.md` |
| **Directories** | lowercase-with-dashes | `subagents/`, `context/` |
| **Functions/Methods** | verbPhrases | `getUser`, `validateEmail` |
| **Predicates** | `isValid`, `hasPermission` | `isValidEmail`, `hasAccess` |
| **Variables** | descriptive, camelCase | `userCount`, `isActive` |
| **Constants** | UPPER_SNAKE_CASE | `MAX_RETRIES`, `API_BASE_URL` |
| **Classes/Types** | PascalCase | `UserService`, `ValidationError` |

### Error Handling

```typescript
// ✅ Explicit error handling with validation
function parseJSON(text: string) {
  try {
    return { success: true, data: JSON.parse(text) };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ✅ Validate at boundaries
function createUser(userData: UserInput) {
  const validation = validateUserData(userData);
  if (!validation.isValid) {
    return { success: false, errors: validation.errors };
  }
  return { success: true, user: saveUser(userData) };
}
```

### Type Patterns (TypeScript)

- Use **explicit typing** for public APIs
- Prefer **interfaces** for object shapes (vs types)
- Use **type** for unions, intersections, computed types
- Never use `as any`, `@ts-ignore`, `@ts-expect-error`
- Use **discriminated unions** for error handling:
  ```typescript
  type Result<T, E = Error> =
    | { success: true; data: T }
    | { success: false; error: E };
  ```

### File Structure Patterns

```
component/
├── index.js      # Public interface (barrel exports)
├── core.js       # Core logic (pure functions)
├── utils.js      # Helpers
└── tests/        # Tests
```

### Agent/Command Structure

Agents (`.opencode/agent/`):
```markdown
---
id: agent-name
name: AgentName
description: "Brief description"
category: core|development|meta
type: core|subagent
version: 1.0.0
mode: primary|subagent
temperature: 0.2

dependencies:
  - subagent:task-manager
  - context:core/standards/code

tools:
  read: true
  write: true
  bash: true

permissions:
  bash:
    "rm -rf *": "ask"
  edit:
    "**/*.env*": "deny"

tags:
  - universal
  - coordination
---

<context>
  <system_context>What this agent does</system_context>
  <domain_context>Domain it operates in</domain_context>
  <task_context>Primary task type</task_context>
</context>

# Agent Instructions

[Detailed instructions for agent behavior]
```

Commands (`.opencode/command/`):
```markdown
---
description: "What this command does"
agent: target-agent
---

# Command Name

You are doing specific task.

**Request:** $ARGUMENTS

**Context Loaded:**
@.opencode/context/core/essential-patterns.md

Execute task now.
```

### Comment/Documentation Conventions

- Use **context-specific documentation** in `.opencode/context/` files
- For public APIs: include JSDoc/docstring with:
  - Description (WHAT it does)
  - Examples (HOW to use)
  - Parameters (@param) with types
  - Returns (@return) with types
- Explain **WHY** in complex logic, not just WHAT
- Remove redundant comments (don't comment the obvious)

---

## Context Loading Rules

**For Commands:**
- Load context immediately using `@` references
- Maximum 4 context files per command (250-450 lines total)
- Keep context files focused (50-150 lines each)

**For Agents:**
- Context loaded based on task type
- Look up additional context deterministically
- Always load project standards before code changes

---

## Security Guidelines

- Agents have restricted permissions by default
- Sensitive operations require explicit approval
- No direct file system modifications without validation
- Use environment variables for secrets
- Never log passwords, tokens, or API keys

---

## Quality Standards

Before any significant work:

1. ✅ Load relevant context files (standards, patterns, workflows)
2. ✅ Follow modular, functional patterns
3. ✅ Use pure functions when possible
4. ✅ Handle errors gracefully
5. ✅ Validate input at boundaries
6. ✅ No hardcoded secrets
7. ✅ Write self-documenting code

**Golden Rule:** If you can't easily test it, refactor it.

---

## Related Context Files

- `.opencode/context/core/essential-patterns.md` - Essential development patterns
- `.opencode/context/core/standards/code-quality.md` - Comprehensive code standards
- `.opencode/context/core/standards/security-patterns.md` - Security patterns
- `.opencode/context/core/standards/test-coverage.md` - Testing standards
- `.opencode/context/core/standards/documentation.md` - Documentation guidelines
