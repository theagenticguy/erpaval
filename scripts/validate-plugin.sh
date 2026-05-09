#!/usr/bin/env bash
# Validate the standalone erpaval-plugin: configs parse, tools/hooks load,
# named cross-reference invariants hold. Wired via `mise run validate`.
# Exit code: 0 on success, 1 on first failure (named diagnostic emitted).

set -uo pipefail
cd "$(dirname "$0")/.."

fail() { echo "FAIL: $*" >&2; exit 1; }
ok()   { echo "  ok: $*"; }

echo "[1/3] Configs parse"
for f in .claude-plugin/plugin.json .mcp.json hooks/hooks.json; do
  python3 -c "import json; json.load(open('$f'))" || fail "JSON parse: $f"
  ok "$f"
done

echo "[2/3] Tools and hooks load"
for tool in skills/erpaval/tools/erpaval-new.py skills/erpaval/tools/erpaval-recall.py skills/erpaval/tools/erpaval-validate.py; do
  uv run "$tool" --help >/dev/null 2>&1 || fail "tool --help: $tool"
  ok "$tool --help"
done
for hook in hooks/validate_packet.py hooks/compound_nudge.py hooks/session_start_bootstrap.py; do
  python3 -c "import ast; ast.parse(open('$hook').read())" || fail "AST parse: $hook"
  ok "$hook ast"
done

echo "[3/3] Cross-reference invariants"
# I1: no personal-plugins: prefix in shipping code
if grep -rn "personal-plugins:" skills/ agents/ hooks/ .mcp.json .claude-plugin/ 2>/dev/null; then
  fail "I1: personal-plugins: prefix found in shipping code"
fi
ok "I1 (no personal-plugins: prefix)"

# I2: cross-skill loads resolve to bundled skills only
BUNDLED=$(ls -1 skills/ | sort -u)
REFERENCED=$(grep -rEoh '\$\{CLAUDE_PLUGIN_ROOT\}/skills/[a-z-]+' skills/ 2>/dev/null | sed 's|.*/skills/||' | sort -u)
for ref in $REFERENCED; do
  echo "$BUNDLED" | grep -qx "$ref" || fail "I2: cross-skill load to non-bundled skill: $ref"
done
ok "I2 (cross-skill loads resolve to bundled: $(echo $BUNDLED | wc -w | tr -d ' ') skills)"

# I3: subagent_type uses bare names (no plugin: prefix)
if grep -rEn 'subagent_type:\s*"?[a-z-]+:[a-z-]+' skills/ agents/ 2>/dev/null; then
  fail "I3: subagent_type uses namespaced name (expected bare)"
fi
ok "I3 (subagent_type uses bare names)"

echo "PASS: erpaval-plugin validates"
