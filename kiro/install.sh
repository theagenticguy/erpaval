#!/usr/bin/env bash
# ERPAVal Kiro CLI distribution installer.
#
# Wires the bundled skills, hooks, agents, and MCP config into a target
# Kiro home (`~/.kiro/` by default, or `<cwd>/.kiro/` with `--workspace`).
# Idempotent: re-running leaves the install in the same state.
#
# Usage:
#   ./install.sh                # install to ~/.kiro/
#   ./install.sh --workspace    # install to <cwd>/.kiro/
#   ./install.sh --dry-run      # print planned actions, no writes
#   ./install.sh --uninstall    # remove installer-created symlinks only
#
# After install, run:
#   kiro-cli chat --agent erpaval-orchestrator

set -euo pipefail

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ERPAVAL_VERSION="1.1.1"
ERPAVAL_BUNDLE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Symlinks the installer manages. Format: "<source>::<dest-suffix>".
# Dest is resolved relative to TARGET at runtime.
LINK_SPECS=(
    "skills/erpaval::skills/erpaval"
    "skills/product-discovery::skills/product-discovery"
    "skills/product-design-shared::skills/product-design-shared"
    "hooks::erpaval/hooks"
    "skills::erpaval/skills"
)

# Agent JSON sources to render with ${ERPAVAL_HOME} substitution.
AGENT_JSONS=(
    "erpaval-orchestrator.json"
    "erpaval-researcher.json"
    "erpaval-explorer.json"
)

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------

WORKSPACE_MODE=0
DRY_RUN=0
UNINSTALL=0

for arg in "$@"; do
    case "$arg" in
        --workspace) WORKSPACE_MODE=1 ;;
        --dry-run)   DRY_RUN=1 ;;
        --uninstall) UNINSTALL=1 ;;
        -h|--help)
            sed -n '2,15p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *)
            echo "Unknown flag: $arg" >&2
            echo "Run with --help for usage." >&2
            exit 64
            ;;
    esac
done

if [[ "$WORKSPACE_MODE" -eq 1 ]]; then
    TARGET="$(pwd)/.kiro"
else
    TARGET="${HOME}/.kiro"
fi

ERPAVAL_HOME="${TARGET}/erpaval"

echo "ERPAVal Kiro CLI distribution installer v${ERPAVAL_VERSION}"
echo "Bundle:  ${ERPAVAL_BUNDLE}"
echo "Target:  ${TARGET}"
echo "Installing to ${ERPAVAL_HOME}"
if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "(dry run — no changes will be made)"
fi
echo ""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

run_or_print() {
    # Print the command; only run it when not in dry-run mode.
    echo "  \$ $*"
    if [[ "$DRY_RUN" -ne 1 ]]; then
        "$@"
    fi
}

ensure_dir() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        run_or_print mkdir -p "$dir"
    fi
}

# Create or refresh a symlink. Idempotent.
link() {
    local src="$1"
    local dst="$2"
    if [[ ! -e "$src" ]]; then
        echo "  skip (source missing): $src" >&2
        return
    fi
    run_or_print ln -sfn "$src" "$dst"
}

# Render an agent JSON with ${ERPAVAL_HOME} substituted.
render_agent_json() {
    local src="$1"
    local dst="$2"
    if [[ ! -f "$src" ]]; then
        echo "  warning: agent JSON not found, skipping: $src" >&2
        return
    fi
    if [[ "$DRY_RUN" -eq 1 ]]; then
        echo "  \$ sed 's|\${ERPAVAL_HOME}|${ERPAVAL_HOME}|g' < ${src} > ${dst}"
    else
        sed "s|\${ERPAVAL_HOME}|${ERPAVAL_HOME}|g" <"$src" >"$dst"
        echo "  rendered ${dst}"
    fi
}

# ---------------------------------------------------------------------------
# Uninstall path
# ---------------------------------------------------------------------------

if [[ "$UNINSTALL" -eq 1 ]]; then
    echo "Uninstalling: removing installer-created symlinks only."
    echo "(user data — sessions, lessons, custom mcp.json — is preserved.)"
    echo ""
    for spec in "${LINK_SPECS[@]}"; do
        dst="${TARGET}/${spec##*::}"
        if [[ -L "$dst" ]]; then
            run_or_print rm -f "$dst"
        fi
    done
    # Remove rendered agent JSONs only if they exist and are files (not symlinks).
    for agent in "${AGENT_JSONS[@]}"; do
        dst="${TARGET}/agents/${agent}"
        if [[ -f "$dst" && ! -L "$dst" ]]; then
            run_or_print rm -f "$dst"
        fi
    done
    # Symlinked mcp.json (only if it points back into the bundle).
    mcp_dst="${TARGET}/settings/mcp.json"
    if [[ -L "$mcp_dst" ]]; then
        run_or_print rm -f "$mcp_dst"
    fi
    echo ""
    echo "Uninstalled. Skill content under ${TARGET}/skills/ is preserved if any was a real dir."
    exit 0
fi

# ---------------------------------------------------------------------------
# Install path
# ---------------------------------------------------------------------------

# 1. Create target directory tree. Only create dirs that are NOT going to be
#    replaced by a symlink in step 2 — `ln -sfn <src> <dst>` against an existing
#    *empty directory* creates the symlink INSIDE the directory rather than
#    replacing it.
echo "Step 1/4: ensure target directories exist."
for sub in skills agents agents/prompts settings erpaval erpaval/settings; do
    ensure_dir "${TARGET}/${sub}"
done
echo ""

# 2. Symlink bundle dirs into the target. If a stale symlink exists at the
#    destination, `ln -sfn` replaces it. If a real (empty) directory exists,
#    we remove it first so the link can take its place.
echo "Step 2/4: link bundle dirs into target."
for spec in "${LINK_SPECS[@]}"; do
    src="${ERPAVAL_BUNDLE}/${spec%%::*}"
    dst="${TARGET}/${spec##*::}"
    if [[ -d "$dst" && ! -L "$dst" ]]; then
        # Empty dir from a prior step or older install — safe to remove because
        # we're about to symlink the same logical location.
        if [[ -z "$(ls -A "$dst" 2>/dev/null)" ]]; then
            run_or_print rmdir "$dst"
        else
            echo "  warning: ${dst} is a non-empty directory; skipping link to avoid overwriting" >&2
            continue
        fi
    fi
    link "$src" "$dst"
done
echo ""

# 3. mcp.json — only if absent or user agrees to overwrite.
echo "Step 3/4: link or skip mcp.json."
mcp_src="${ERPAVAL_BUNDLE}/settings/mcp.json"
mcp_dst="${TARGET}/settings/mcp.json"
if [[ -e "$mcp_dst" && ! -L "$mcp_dst" ]]; then
    if [[ "$DRY_RUN" -eq 1 ]]; then
        echo "  would prompt: ${mcp_dst} exists; overwrite? (skipping in dry-run)"
    else
        printf "  %s exists. Overwrite with bundled mcp.json? [y/N] " "$mcp_dst"
        read -r reply
        if [[ "$reply" =~ ^[Yy]$ ]]; then
            link "$mcp_src" "$mcp_dst"
        else
            echo "  kept existing ${mcp_dst}"
        fi
    fi
else
    link "$mcp_src" "$mcp_dst"
fi
echo ""

# 4. Render agent JSONs and prompts with ${ERPAVAL_HOME} substituted.
echo "Step 4/4: render agent JSONs and prompts."
for agent in "${AGENT_JSONS[@]}"; do
    render_agent_json "${ERPAVAL_BUNDLE}/agents/${agent}" "${TARGET}/agents/${agent}"
done
prompts_src="${ERPAVAL_BUNDLE}/agents/prompts"
if [[ -d "$prompts_src" ]]; then
    for prompt in "$prompts_src"/*.md; do
        [[ -f "$prompt" ]] || continue
        prompt_name="$(basename "$prompt")"
        render_agent_json "$prompt" "${TARGET}/agents/prompts/${prompt_name}"
    done
fi
echo ""

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------

if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "Dry run complete. Re-run without --dry-run to apply."
else
    echo "Installed. Run: kiro-cli chat --agent erpaval-orchestrator"
fi
