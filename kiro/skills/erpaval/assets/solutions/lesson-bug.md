---
title: <short descriptive title>
track: bug
category: build-errors                      # build-errors | test-failures | deploy-errors
module: <path or package>
component: <library or subsystem>
severity: medium                            # low | medium | high | critical
tags: [<tag>, <tag>, <tag>]
symptoms:
  - <observable symptom>
  - <observable symptom>
root_cause: |
  <multi-line explanation of why this happened>
resolution_type: config-change              # config-change | code-fix | dependency-upgrade | workaround
applies_when:
  - <condition>
  - <condition>
---

# Fix

<the resolution steps, with code or config examples>

# Why this matters

<consequences of ignoring this lesson>
