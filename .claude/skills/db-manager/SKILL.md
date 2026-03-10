---
name: db-manager
description: >
  Use this skill whenever the user asks something related to current project DB with posgres, turn on the windoes postgres database service
---

---

## Workflow

1. If prompted to turn on postgres windows service, admin elevation is required. Run:
    ```powershell
    Start-Process powershell -ArgumentList '-Command Start-Service postgresql-x64-16' -Verb RunAs -Wait
    ```
  - Check service running with
    ```powershell
    Get-Service postgresql-x64-16
    ```
  - Note: Running `Start-Service postgresql-x64-16` directly will fail with a permissions error. Always use `Start-Process` with `-Verb RunAs` to elevate.
  
## When NOT to Use This Skill
