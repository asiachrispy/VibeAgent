---
name: ui-ux-pro-max
description: "UI/UX design intelligence. 50 styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples."
compatibility: "OpenCode with Python 3.x"
---

# UI/UX Pro Max - Design Intelligence

Searchable database of UI styles, color palettes, font pairings, chart types, product recommendations, UX guidelines, and stack-specific best practices.

## 重要说明

本技能包依赖外部 Python 脚本和数据库，当前环境可能不完整。使用前请确保：

1. **外部依赖存在**：
   - `.shared/ui-ux-pro-max/scripts/search.py` 脚本必须存在
   - `.shared/ui-ux-pro-max/data/` 数据库文件必须存在

2. **Python 环境可用**：
   - Python 3.x 已安装
   - 可以执行 `python3` 或 `python` 命令

3. **与其他技能的协作**：
   - 本技能由 `dev-builder` 或主控在需要 UI 代码时自动调用
   - 本技能专注于 UI 视觉实现，不涉及需求分析或功能逻辑

**如果外部依赖缺失**：
- 本技能将无法正常工作
- 建议跳过 UI 视觉优化，直接使用 dev-builder 实现功能代码
- 或手动创建外部依赖环境

---

## OpenCode Tool Mapping

| Codex Tool    | OpenCode Equivalent    |
|---------------------|------------------------|
| `TodoWrite`         | `update_plan`          |
| `Task` subagents    | `@mention` system      |
| `Skill` tool        | `use_skill` tool       |
| File operations     | Native OpenCode tools  |

## When to Use

Use this skill when:
- User requests UI/UX work (design, build, create, implement, review, fix, improve)
- User wants to build frontend pages (landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app)
- User asks about design patterns, color palettes, typography, or UI components

## 启动前检查

在开始任何工作前，必须执行以下检查：

### 1. Python 环境检查

```bash
python3 --version || python --version
```

- 如果 Python 3.x 未安装：
  - 立即停止执行
  - 报告错误："Python 3.x 未安装，无法使用本技能"
  - 提供安装指南（见下方的 Prerequisites 章节）

- 如果 Python 3.x 已安装：
  - 记录 Python 版本
  - 继续执行

### 2. 外部脚本检查

检查 `.shared/ui-ux-pro-max/scripts/search.py` 是否存在：

```bash
ls -la .shared/ui-ux-pro-max/scripts/search.py
```

- 如果脚本不存在：
  - 警告用户："外部搜索脚本不存在，无法使用 UI/UX 数据库"
  - 提供两个选项：
    1. **降级模式**：使用内置的通用 UI/UX 最佳实践（不依赖外部数据库）
    2. **中止模式**：建议用户先安装外部依赖再重试
  - 默认选择降级模式，继续执行

### 3. 外部数据库检查（可选）

如果搜索脚本存在，检查数据库文件：

```bash
ls -la .shared/ui-ux-pro-max/data/
```

- 如果数据库不存在或损坏：
  - 警告用户："UI/UX 数据库缺失或损坏，搜索功能不可用"
  - 降级到通用模式，使用内置指导

### 4. 与其他技能的上下文检查

本技能通常在以下场景被调用：

- **由 dev-builder 调用**：当实现 UI 组件或页面时
- **由主控直接调用**：当用户明确请求 UI/UX 设计指导时

检查调用上下文：

- 如果由 dev-builder 调用：
  - 读取 Product-Spec.md 了解需求
  - 读取 UI-Prompts.md（如果存在）了解设计参考
  - 专注于实现具体的 UI 代码

- 如果由主控直接调用：
  - 询问用户的具体需求（产品类型、风格偏好、技术栈）
  - 提供设计建议和代码示例

### 5. 降级模式准备

如果外部依赖缺失，准备降级模式：

- 使用内置的通用 UI/UX 指南（见本文件的 Common Rules 和 Pre-Delivery Checklist）
- 根据用户描述的产品类型，提供风格建议
- 不使用 `search.py` 脚本，直接基于常见模式提供建议

---

## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on user's OS:

**macOS:**

```bash
brew install python3
```

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install python3
```

**Windows:**

```powershell
winget install Python.Python.3.12
```

---

## How to Use

### Step 1: Analyze User Requirements

Extract key information from user request:

- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Search Relevant Domains

Use `update_plan` to track your search tasks, then execute multiple searches to gather comprehensive information.

```bash
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**Recommended search order:**

1. **Product** - Get style recommendations for product type
2. **Style** - Get detailed style guide (colors, effects, frameworks)
3. **Typography** - Get font pairings with Google Fonts imports
4. **Color** - Get color palette (Primary, Secondary, CTA, Background, Text, Border)
5. **Landing** - Get page structure (if landing page)
6. **Chart** - Get chart recommendations (if dashboard/analytics)
7. **UX** - Get best practices and anti-patterns
8. **Stack** - Get stack-specific guidelines (default: html-tailwind)

### Step 3: Stack Guidelines (Default: html-tailwind)

If user doesn't specify a stack, **default to `html-tailwind`**.

```bash
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

---

## Search Reference

### Available Domains

| Domain       | Use For                              | Example Keywords                                         |
| ------------ | ------------------------------------ | -------------------------------------------------------- |
| `product`    | Product type recommendations         | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style`      | UI styles, colors, effects           | glassmorphism, minimalism, dark mode, brutalism          |
| `typography` | Font pairings, Google Fonts          | elegant, playful, professional, modern                   |
| `color`      | Color palettes by product type       | saas, ecommerce, healthcare, beauty, fintech, service    |
| `landing`    | Page structure, CTA strategies       | hero, hero-centric, testimonial, pricing, social-proof   |
| `chart`      | Chart types, library recommendations | trend, comparison, timeline, funnel, pie                 |
| `ux`         | Best practices, anti-patterns        | animation, accessibility, z-index, loading               |
| `prompt`     | AI prompts, CSS keywords             | (style name)                                             |

### Available Stacks

| Stack           | Focus                                          |
| --------------- | ---------------------------------------------- |
| `html-tailwind` | Tailwind utilities, responsive, a11y (DEFAULT) |
| `react`         | State, hooks, performance, patterns            |
| `nextjs`        | SSR, routing, images, API routes               |
| `vue`           | Composition API, Pinia, Vue Router             |
| `svelte`        | Runes, stores, SvelteKit                       |
| `swiftui`       | Views, State, Navigation, Animation            |
| `react-native`  | Components, Navigation, Lists                  |
| `flutter`       | Widgets, State, Layout, Theming                |
| `shadcn`        | shadcn/ui components, theming, forms, patterns |

---

## 与其他技能的协作

### 与 dev-builder 协作
- **调用关系**：dev-builder 在实现 UI 代码时，会调用本技能
- **职责划分**：
  - dev-builder 负责功能逻辑、业务代码、API 集成
  - 本技能负责 UI 视觉、样式、布局、交互效果
- **协作方式**：
  - dev-builder 使用 `Task` 工具调用本技能的子代理
  - 本技能返回 UI 代码片段或完整的组件实现
  - dev-builder 将 UI 代码集成到项目中

### 与 ui-prompt-generator 协作
- **关系**：ui-prompt-generator 提供设计参考，本技能实现代码
- **输入**：如果 UI-Prompts.md 存在，本技能读取其内容：
  - 设计风格（glassmorphism, minimalism 等）
  - 配色方案（主色、辅助色、强调色）
  - 布局结构
- **输出**：根据设计参考实现对应的 UI 代码
- **优势**：确保生成的代码与设计稿一致

### 与 product-spec-builder 协作
- **间接关系**：通过 dev-builder 间接协作
- **输入**：读取 Product-Spec.md 了解：
  - 目标用户（决定视觉风格）
  - 核心功能（决定 UI 组件）
  - AI 增强功能（决定智能交互）
- **输出**：实现符合产品定位的 UI 代码

### 协作流程示例

```
用户请求：实现一个 SaaS 产品的登录页面

1. product-spec-builder:
   生成产品文档：目标用户是企业用户，风格专业、简洁

2. ui-prompt-generator（可选）:
   生成设计提示词：Material Design 风格，蓝色系配色

3. dev-builder:
   - 读取 Product-Spec.md 和 UI-Prompts.md
   - 实现登录功能逻辑（验证、API 调用）
   - 调用 ui-ux-pro-max 实现 UI 代码

4. ui-ux-pro-max（本技能）:
   - 根据 Product-Spec.md 确定风格（专业、简洁）
   - 根据 UI-Prompts.md 确定配色（蓝色系）
   - 搜索 Material Design 最佳实践（如果外部依赖可用）
   - 生成登录页面 UI 代码（表单、按钮、布局）
   - 返回给 dev-builder
```

### 协作原则

- **不越界**：本技能只负责 UI 视觉代码，不涉及业务逻辑
- **可复用**：提供的 UI 代码应该是可复用的组件
- **响应式**：UI 代码应该适配不同屏幕尺寸
- **可访问**：UI 代码应该遵循无障碍标准（WCAG）
- **性能优化**：UI 代码应该考虑性能（避免不必要的重渲染）

---

## Example Workflow

**User request:** "Build a landing page for a professional skincare service."

**AI should:**

```bash
# 1. Search product type
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --domain product

# 2. Search style (based on industry: beauty, elegant)
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "elegant minimal soft" --domain style

# 3. Search typography
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "elegant luxury" --domain typography

# 4. Search color palette
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --domain color

# 5. Search landing page structure
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "hero-centric social-proof" --domain landing

# 6. Search UX guidelines
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "animation" --domain ux
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "accessibility" --domain ux

# 7. Search stack guidelines (default: html-tailwind)
python3 ../../.shared/ui-ux-pro-max/scripts/search.py "layout responsive" --stack html-tailwind
```

**Then:** Synthesize all search results and implement the design.

---

## Tips for Better Results

1. **Be specific with keywords** - "healthcare SaaS dashboard" > "app"
2. **Search multiple times** - Different keywords reveal different insights
3. **Combine domains** - Style + Typography + Color = Complete design system
4. **Always check UX** - Search "animation", "z-index", "accessibility" for common issues
5. **Use stack flag** - Get implementation-specific best practices
6. **Iterate** - If first search doesn't match, try different keywords

---

## Common Rules for Professional UI

These are frequently overlooked issues that make UI look unprofessional:

### Icons & Visual Elements

| Rule                       | Do                                              | Don't                                  |
| -------------------------- | ----------------------------------------------- | -------------------------------------- |
| **No emoji icons**         | Use SVG icons (Heroicons, Lucide, Simple Icons) | Use emojis like 🎨 🚀 ⚙️ as UI icons   |
| **Stable hover states**    | Use color/opacity transitions on hover          | Use scale transforms that shift layout |
| **Correct brand logos**    | Research official SVG from Simple Icons         | Guess or use incorrect logo paths      |
| **Consistent icon sizing** | Use fixed viewBox (24x24) with w-6 h-6          | Mix different icon sizes randomly      |

### Interaction & Cursor

| Rule                   | Do                                                    | Don't                                        |
| ---------------------- | ----------------------------------------------------- | -------------------------------------------- |
| **Cursor pointer**     | Add `cursor-pointer` to all clickable/hoverable cards | Leave default cursor on interactive elements |
| **Hover feedback**     | Provide visual feedback (color, shadow, border)       | No indication element is interactive         |
| **Smooth transitions** | Use `transition-colors duration-200`                  | Instant state changes or too slow (>500ms)   |

### Light/Dark Mode Contrast

| Rule                      | Do                                  | Don't                                   |
| ------------------------- | ----------------------------------- | --------------------------------------- |
| **Glass card light mode** | Use `bg-white/80` or higher opacity | Use `bg-white/10` (too transparent)     |
| **Text contrast light**   | Use `#0F172A` (slate-900) for text  | Use `#94A3B8` (slate-400) for body text |
| **Muted text light**      | Use `#475569` (slate-600) minimum   | Use gray-400 or lighter                 |
| **Border visibility**     | Use `border-gray-200` in light mode | Use `border-white/10` (invisible)       |

### Layout & Spacing

| Rule                     | Do                                  | Don't                                  |
| ------------------------ | ----------------------------------- | -------------------------------------- |
| **Floating navbar**      | Add `top-4 left-4 right-4` spacing  | Stick navbar to `top-0 left-0 right-0` |
| **Content padding**      | Account for fixed navbar height     | Let content hide behind fixed elements |
| **Consistent max-width** | Use same `max-w-6xl` or `max-w-7xl` | Mix different container widths         |

---

## Pre-Delivery Checklist

Before delivering UI code, verify these items:

### Visual Quality

- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Brand logos are correct (verified from Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] Use theme colors directly (bg-primary) not var() wrapper

### Interaction

- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode

- [ ] Light mode text has sufficient contrast (4.5:1 minimum)
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Test both modes before delivery

### Layout

- [ ] Floating elements have proper spacing from edges
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 320px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility

- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected

---

## 错误处理

### Python 未安装

**症状**：执行 `python3` 命令失败

**处理方式**：
- 立即停止执行
- 报告错误："Python 3.x 未安装，无法使用 UI/UX Pro Max 技能"
- 提供安装指南（见 Prerequisites 章节）
- 建议用户：安装 Python 后重试，或跳过 UI/UX 优化

### 外部脚本缺失

**症状**：`.shared/ui-ux-pro-max/scripts/search.py` 不存在

**处理方式**：
- 警告用户："外部 UI/UX 数据库不可用，将使用通用模式"
- 切换到降级模式：
  - 使用内置的通用 UI/UX 指南
  - 基于常见模式提供建议
  - 不执行 `search.py` 脚本
- 继续执行，但说明功能受限

### 外部数据库缺失

**症状**：`.shared/ui-ux-pro-max/data/` 目录不存在或为空

**处理方式**：
- 警告用户："UI/UX 数据库文件缺失，搜索功能不可用"
- 切换到降级模式
- 继续执行，但说明搜索功能受限

### 脚本执行失败

**症状**：执行 `search.py` 时抛出异常

**处理方式**：
- 捕获异常并记录错误信息
- 警告用户："搜索脚本执行失败，将使用通用模式"
- 切换到降级模式
- 继续执行，但说明搜索功能不可用

### 搜索结果为空

**症状**：搜索返回无结果或结果不匹配

**处理方式**：
- 尝试不同的关键词
- 尝试不同的搜索域（domain）
- 如果仍然无结果，使用内置指导
- 告诉用户："未找到匹配的搜索结果，使用通用最佳实践"

### 产品文档缺失（dev-builder 调用时）

**症状**：由 dev-builder 调用，但 Product-Spec.md 不存在

**处理方式**：
- 警告 dev-builder："产品文档不存在，无法获取设计需求"
- 询问 dev-builder 是否继续（使用通用模式）
- 如果继续，基于用户提供的直接需求执行
- 如果不继续，中止执行

### 设计参考缺失（ui-prompt-generator 未执行）

**症状**：UI-Prompts.md 不存在

**处理方式**：
- 警告用户："未找到 UI 设计参考，将使用通用设计风格"
- 询问用户的设计偏好：
  - 风格：minimalism / modern / playful / professional
  - 配色：冷色 / 暖色 / 中性色 / 渐变
- 根据用户偏好提供设计建议

### 降级模式说明

当外部依赖缺失时，进入降级模式：

**可用功能**：
- ✅ 使用内置的通用 UI/UX 指南
- ✅ 基于 Common Rules 提供设计建议
- ✅ 使用 Pre-Delivery Checklist 验证代码
- ❌ 无法使用搜索数据库
- ❌ 无法获取特定行业的最佳实践

**降级模式工作流程**：
1. 基于用户的产品类型，选择通用的风格建议
2. 使用 Common Rules 避免常见错误
3. 使用 Pre-Delivery Checklist 确保质量
4. 参考网络资源（如果允许）补充设计建议

**退出降级模式**：
- 当用户安装了外部依赖后，可以恢复完整模式
- 提示用户："现在可以安装 UI/UX 数据库以获得更好的设计建议"

---

## 降级模式使用指南

### 降级模式下的设计决策

**基于产品类型选择风格**：

| 产品类型 | 推荐风格 | 推荐配色 |
|---------|---------|---------|
| SaaS | Material Design | 蓝色系 |
| 电商 | Modern Minimalist | 暖色/渐变 |
| 管理后台 | Clean Professional | 中性色 |
| 博客/Portfolio | Flat Design | 柔和色 |
| 创意工具 | Creative | 鲜艳色 |

**基于技术栈选择实现方式**：

| 技术栈 | 推荐方式 |
|-------|---------|
| html-tailwind | 使用 Tailwind CSS 工具类 |
| React | 使用 React 组件 + Tailwind |
| Vue | 使用 Vue 组件 + Tailwind |
| Next.js | 使用 Next.js 组件 + Tailwind |

### 降级模式下的代码生成

**不使用搜索脚本**，直接基于以下原则生成代码：

1. **遵循 Common Rules**：确保不犯常见错误
2. **使用 Pre-Delivery Checklist**：验证代码质量
3. **响应式设计**：适配不同屏幕尺寸
4. **无障碍标准**：遵循 WCAG 2.1 AA 级
5. **性能优化**：避免不必要的重渲染

### 降级模式的局限性

- 无法获取特定行业的最佳实践
- 无法获取最新的设计趋势
- 无法访问设计案例库
- 可能需要更多的人工调整

建议用户优先安装外部依赖，以获得更好的设计建议。
