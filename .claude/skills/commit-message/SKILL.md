---
name: commit-message
description: >
  Use this skill whenever the user wants to commit changes, write a commit message,
  or commit and push to a branch. Triggers include: "commit my changes", "push to branch",
  "write a commit message", "stage and commit", or any request to save and publish code
  changes to version control. Use for single commits and for commit-then-push workflows.
  Do NOT use for pull requests or code reviews.
---

# Commit Message Skill

Generate clean, descriptive commit messages and handle commit/push workflows.

---

## Workflow

### 1. Commit Only
When the user wants to commit without pushing:

```bash
git add .
git commit -m "<type>: <short summary of changes>"
```

### 2. Commit and Push
When the user wants to commit and push to the current branch:

```bash
git add .
git commit -m "<type>: <short summary of changes>"
git push origin HEAD
```

---

## Writing the Commit Message

1. **Check what changed** — run `git diff --staged` or `git status` to understand the actual changes
2. **Pick a type** from the list below
3. **Write a concise summary** (under 72 characters) in the imperative mood ("add", "fix", "update" — not "added" or "fixing")

### Commit Types

| Type | When to use |
|------|-------------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `refactor` | Code restructure without behavior change |
| `style` | Formatting, whitespace, no logic change |
| `docs` | Documentation updates |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, config |
| `remove` | Deleting files or dead code |

### Examples

```
feat: add user authentication flow
fix: resolve null pointer in payment handler
refactor: extract validation logic into helper
docs: update README with setup instructions
chore: bump lodash to 4.17.21
```

---

## When NOT to Use This Skill

- Creating or reviewing pull requests
- Rebasing, cherry-picking, or complex git history operations
- Resolving merge conflicts