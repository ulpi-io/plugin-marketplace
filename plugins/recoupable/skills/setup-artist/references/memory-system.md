# Memory System Templates

Two files to create in `memory/`.

---

## `memory/README.md`

```markdown
---
name: Memory
description: "How the memory system works. Read this before writing to any memory file. This directory holds everything agents have LEARNED about {Artist Name} — not who the artist IS (that's context/), and not reference material (that's library/)."
---

# Memory

This directory is the artist's **learned knowledge** — what agents discover through doing the work. It grows over time as agents interact with the artist, create content, manage releases, and learn what works.

## Structure

memory/
├── README.md          ← You are here
├── MEMORY.md          ← Core index: always read first (keep under ~200 lines)
├── {topic}.md         ← Topic files: detailed notes (created as needed)
├── log/               ← Session logs: raw, append-only (created on first session)
│   └── YYYY-MM-DD.md
└── archive/           ← Past era memories (created when eras change)
    └── {era-slug}/

Only `README.md` and `MEMORY.md` ship at creation. Everything else is created by agents as they work.

## Memory Scope — The Most Important Concept

Not all knowledge has the same lifespan. Before saving ANYTHING to memory, determine its **scope**:

| Scope | Meaning | Where it goes | Example |
|-------|---------|---------------|---------|
| `permanent` | True about the artist regardless of era or phase | `MEMORY.md` | "The artist prefers lowercase in all captions" |
| `era` | True for the current release cycle — may change next era | `MEMORY.md` (tagged with era) | "Going for a darker visual tone this release" |
| `session` | A decision made about a specific piece of content or task | `log/YYYY-MM-DD.md` only | "User wanted blue hair on this image" |

### How to Decide Scope

**When in doubt, ASK.** If a user gives feedback while working on something specific, clarify before saving:

> "Got it — blue hair for this one. Should I make that the default going forward, or just for this piece?"

**Rules of thumb:**
- If the user is reacting to a specific output → it's probably **session** scope. Log it, don't memorize it.
- If the user says "always," "from now on," or "I prefer" → it's probably **permanent** or **era** scope.
- If it relates to the current release strategy, visual direction, or campaign → it's **era** scope.
- If it's about core identity, voice, or lasting preferences → it's **permanent** scope.

### Tagging Era-Scoped Memories

When writing era-scoped memories to `MEMORY.md`, tag them so they can be identified later:

```
## Visual Direction (era: debut-ep)
- Going darker and moodier for this release
- Blue/purple palette instead of the usual warm tones
```

When `era.json` changes, these tagged sections become candidates for archiving.

## Files

### `MEMORY.md` — Core Index

The single most important file. **Read this first every session.**

- Contains curated, distilled knowledge about the artist
- Bounded: keep it under ~200 lines
- **Edit, don't just append** — update facts when they change, remove what's outdated
- When a section gets too detailed, move it into a topic file and leave a reference
- Tag era-specific entries so they can be archived when the era changes

### Topic Files (`{topic}.md`)

Created by agents when `MEMORY.md` sections grow too long. Examples:
- `content-learnings.md` — what works and doesn't for this artist's content
- `audience-insights.md` — patterns in audience behavior
- `process-notes.md` — how things work for this artist

**Format:**

---
name: {Topic Name}
description: "{What this file covers and when to read it.}"
era: {release-slug}
---

### `log/` — Session Logs

Raw, append-only logs of what happened each session. Created on first use. **Session-scoped decisions live here — not in MEMORY.md.**

**Format:** `log/YYYY-MM-DD.md`

Multiple entries per day are appended to the same file. Don't edit past entries.

### `archive/` — Past Era Memories

When an era changes, move era-tagged sections from `MEMORY.md` and era-scoped topic files here to keep the active memory clean and relevant.

## Session Lifecycle

### Start of Session
1. Read `memory/MEMORY.md` — get current knowledge
2. Check for today's log (`memory/log/YYYY-MM-DD.md`) — resume context if exists
3. Read `context/era.json` — know the current phase

### During Session
- Learn something durable → determine **scope**, then **update** `MEMORY.md` (permanent/era) or **append** to log (session)
- Discover a correction → **edit** `MEMORY.md` (replace the old fact)
- User gives feedback on specific content → **append** to today's log. Do NOT promote to `MEMORY.md` unless the user confirms it's a lasting preference
- Complete something or make a decision → **append** to today's log
- Need detailed history → **read** topic files or past logs

### End of Session
- Review: did anything important happen that's not in `MEMORY.md`?
- If `MEMORY.md` is getting long → move details into topic files

### When Era Changes (New Release Cycle)
1. Review all era-tagged entries in `MEMORY.md`
2. Ask the user: "We're starting a new era. Do these still apply?" (list the era-tagged items)
3. Archive what's no longer relevant → move to `archive/{old-era-slug}/`
4. Keep anything the user confirms is still true (update the era tag or promote to permanent)

### Periodic Maintenance
- Review recent logs → promote key insights to `MEMORY.md` (only if confirmed as lasting)
- Remove or update outdated facts in `MEMORY.md`

## What Goes Where

| I learned... | Scope | Write it to... |
|-------------|-------|---------------|
| A durable fact about the artist or their work | permanent | `MEMORY.md` (edit/update) |
| A preference for this release cycle | era | `MEMORY.md` (tagged with era) |
| A decision about a specific piece of content | session | `log/YYYY-MM-DD.md` (append only) |
| Detailed performance data or analysis | era | A topic file (e.g., `content-learnings.md`) |
| Something that corrects a previous belief | permanent | `MEMORY.md` (replace the old fact) |
| User feedback on one specific output | session | `log/YYYY-MM-DD.md` — ask before promoting |

## What Does NOT Go Here

| This kind of information... | Goes in... |
|----------------------------|-----------|
| Who the artist is (identity, brand, voice) | `context/artist.md` |
| Who the audience is | `context/audience.md` |
| Current release and phase | `context/era.json` |
| Reference docs, research, reports | `library/` |
| To-do items and tasks | `context/tasks.md` |
| Service connections and credentials | `config/SERVICES.md` |
```

---

## `memory/MEMORY.md`

```markdown
---
name: Memory
description: "Curated knowledge about {Artist Name}. Read this first every session. Keep concise — move details into topic files when sections grow."
---

# Memory

<!-- 
  This file is the core index of everything agents have learned about this artist.
  
  Guidelines:
  - Keep under ~200 lines
  - EDIT existing facts when they change — don't just append
  - When a section gets too detailed, move it to a topic file (e.g., content-learnings.md)
    and leave a one-line reference here
  - Delete or update anything that's no longer true
  
  SCOPE RULES:
  - Only write PERMANENT or ERA-scoped knowledge here
  - Tag era-scoped entries like: ## Section Name (era: release-slug)
  - Session-specific feedback belongs in log/YYYY-MM-DD.md — NOT here
  - When in doubt about scope, ASK the user before saving
  
  Structure will emerge naturally. Let the work define what sections you need.
-->
```
