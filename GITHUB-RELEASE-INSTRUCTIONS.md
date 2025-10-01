# GitHub Release Instructions - v2.1

## Quick Steps

1. **Go to Releases Page**
   ```
   https://github.com/alexander-stage-hoco/claude-development-framework/releases
   ```

2. **Click "Draft a new release"**

3. **Configure Release**:
   - **Tag**: Select `v2.1-learnings-applied` (already pushed)
   - **Title**: `v2.1 "Agent Excellence" - Enhanced Subagents & Context Efficiency`
   - **Description**: Copy content from `RELEASE-NOTES-v2.1.md`
   - **This is a pre-release**: ❌ (unchecked - this is stable)
   - **Set as latest release**: ✅ (checked)

4. **Click "Publish release"**

---

## Detailed Steps

### Step 1: Navigate to Repository

Open your browser and go to:
```
https://github.com/alexander-stage-hoco/claude-development-framework
```

### Step 2: Access Releases

Click on "Releases" in the right sidebar (or navigate to):
```
https://github.com/alexander-stage-hoco/claude-development-framework/releases
```

### Step 3: Draft New Release

Click the **"Draft a new release"** button (top right)

### Step 4: Choose Tag

In the "Choose a tag" dropdown:
- Select **`v2.1-learnings-applied`**
- This tag should already exist (we pushed it)
- If not visible, type `v2.1-learnings-applied` and it will find it

### Step 5: Set Release Title

In the "Release title" field, enter:
```
v2.1 "Agent Excellence" - Enhanced Subagents & Context Efficiency
```

### Step 6: Add Release Description

**Option A: Copy Full Release Notes**

1. Open `RELEASE-NOTES-v2.1.md` in your editor
2. Copy the ENTIRE contents
3. Paste into the description field

**Option B: Use Abbreviated Version**

Copy this abbreviated version:

```markdown
# v2.1 "Agent Excellence" 🎯

Major enhancement to subagent system through community research and domain-specific optimizations.

## Highlights

✨ **All 6 Agents Optimized** with community best practices (v2.0-agents-optimized)
- Trigger keywords for 2-3x more invocations
- Strategic model selection (opus/sonnet)
- Prompt compaction (50-70% reduction)
- Enhanced descriptions and categorized checklists

🎓 **3 Agents Enhanced** with domain expertise (v2.1-learnings-applied)
- `service-designer` ← api-designer (8 learnings)
- `service-optimizer` ← ml-engineer (8 learnings)
- `uc-service-tracer` ← security-auditor (10 learnings)

📊 **Context Efficiency Documented**
- TIER 1: 3.3% overhead (recommended)
- Measured all 5 tiers with token counts
- Updated 4 key files with loading strategies

🧹 **Repository Streamlined** (81% reduction in research materials)

## Research Scope

- 20 agents analyzed from top repositories
- wshobson/agents (12.5k⭐) + VoltAgent (1.6k⭐)
- 26 domain-specific learnings applied
- Complete traceability maintained

## Upgrade

✅ **No breaking changes** - fully backward compatible

**Recommended**:
- Start sessions with TIER 1 only (4 files, 3.3% overhead)
- Review enhanced agent capabilities in `agent-research/LEARNINGS-APPLIED.md`
- Run `./scripts/estimate-context.sh` to check context usage

## Documentation

📖 Full release notes: [RELEASE-NOTES-v2.1.md](./RELEASE-NOTES-v2.1.md)

## Metrics

- **Agents Enhanced**: 3/6 (50%)
- **Total Learnings**: 26 (8+8+10)
- **Avg Process Increase**: +86% steps
- **Avg Quality Checks**: +86% checks
- **Context Efficiency**: Measured & documented

## Tags

- `v2.0` - Base framework
- `v2.0-agents-optimized` - Community patterns applied
- `v2.1-learnings-applied` - Domain learnings applied ⭐ (this release)

---

**Framework**: Claude Development Framework v2.1
**Date**: 2025-10-01

🎉 Thank you for using the framework!
```

### Step 7: Release Settings

**Important checkboxes**:
- ✅ **Set as the latest release** (checked)
- ❌ **This is a pre-release** (unchecked - this is stable)

**Target branch**:
- Should be `main` (default)

### Step 8: Publish

Click **"Publish release"** button at the bottom

---

## After Publishing

### Verify Release

1. **Check release page**: Should show v2.1 as "Latest"
2. **Verify tag**: `v2.1-learnings-applied` should be visible
3. **Check downloads**: Release assets should be available

### Share Release

**URLs to share**:
- Release page: `https://github.com/alexander-stage-hoco/claude-development-framework/releases/tag/v2.1-learnings-applied`
- Repository: `https://github.com/alexander-stage-hoco/claude-development-framework`

**Announcement template**:
```
🎉 Claude Development Framework v2.1 "Agent Excellence" released!

Major enhancements:
✨ All 6 agents optimized with community best practices
🎓 3 agents enhanced with domain-specific learnings
📊 Context efficiency measured & documented
🧹 Repository streamlined

No breaking changes - fully backward compatible.

Release notes: https://github.com/alexander-stage-hoco/claude-development-framework/releases/tag/v2.1-learnings-applied
```

---

## Troubleshooting

### Tag Not Found

If `v2.1-learnings-applied` doesn't appear:
1. Verify tag was pushed: `git ls-remote --tags origin`
2. Refresh browser page
3. Type tag name manually in the dropdown

### Release Notes Formatting

GitHub uses Markdown rendering:
- Headers should render correctly
- Tables should display properly
- Code blocks should be syntax-highlighted
- Emojis should display

### Edit After Publishing

If you need to edit:
1. Go to the release page
2. Click "Edit release" (top right)
3. Make changes
4. Click "Update release"

---

## Alternative: Using GitHub CLI

If you have `gh` CLI installed:

```bash
gh release create v2.1-learnings-applied \
  --title "v2.1 \"Agent Excellence\" - Enhanced Subagents & Context Efficiency" \
  --notes-file RELEASE-NOTES-v2.1.md \
  --latest
```

This automatically creates the release with:
- Tag: v2.1-learnings-applied
- Title: From --title flag
- Description: From RELEASE-NOTES-v2.1.md
- Marked as latest

---

## Done!

Your v2.1 release is now public and users can:
- Download the release
- Clone with tag: `git clone --branch v2.1-learnings-applied <repo-url>`
- See release notes on GitHub
- Track version history

**Next**: Consider announcing on relevant communities, social media, or forums.
