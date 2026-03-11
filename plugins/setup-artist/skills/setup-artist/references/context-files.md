# Context File Templates

These are the templates for every file in the `context/` directory. Copy each one and replace `{placeholders}` with real data.

---

## `context/artist.md`

```markdown
---
name: Artist
description: "The complete profile for {Artist Name} — who they are and how they present. Read this first before doing anything for this artist."
---

{One-sentence description of the artist — age, background, genre, instrument/role.}

## Personality

{Core personality traits. Who are they when the camera is off? What makes them tick?}

## Topics

{What the artist thinks about, writes about, and keeps coming back to. Recurring themes and obsessions.}

## Genre

{Primary genre and sub-genres.}

## Comparables

{2-4 comparable artists that help triangulate the sound and sensibility.}

---

## Positioning

{One paragraph describing the artist's unique position — what makes them different, where they sit in the landscape, and why someone should care.}

**One-liner:** {A single sentence pitch for the artist.}

**Archetype:** {The artist's brand archetype in 2-4 words.}

## Aesthetic

{One sentence that captures the entire visual world. This is the north star — every creative decision should feel like it belongs in this sentence.}

## Mood

{What does the content FEEL like? Describe the lighting, texture, energy, and atmosphere. Think about what someone would feel looking at the content before they even read or listen.}

## Colors & Typography

- **Primary:** {dominant palette}
- **Secondary:** {supporting tones}
- **Accent:** {highlights or pops of color}
- **Fonts:** {primary typeface, secondary/accent typeface if any}

## Settings

{Where does the visual world live? Describe the environments and spaces that feel right for this artist. These directly inform image generation and video backgrounds.}

## Fashion & Appearance

{What does the artist look like and wear? Clothing, hair, makeup, accessories. Be specific enough for consistent character depiction across generated content.}

## Signature Elements

{Recurring visual props, motifs, or symbols that make this artist's content instantly recognizable.}

## Visual References

{Specific music videos, photoshoots, films, or cultural touchpoints that capture the right feel. Link or describe them clearly enough for another agent to look them up.}

## Voice

{How the artist speaks and writes. Describe the feel — not just adjectives. This calibrates all text output: captions, replies, bios, emails.}

## Tone

{Rules for how text content should sound. Capitalization, punctuation style, energy level, what language to use and what to avoid.}
```

---

## `context/audience.md`

```markdown
---
name: Audience
description: The emotional relationship between {Artist Name} and the people who listen. Use this to write content that feels like it was made FOR them — not marketed AT them. Every section here should change how you write captions, pick visuals, and engage.
---

## Why They Listen

{What role does this artist play in their life? Not "they like the music" — WHY do they keep coming back? What need does this artist fill?}

## What They Relate To

{The specific feelings, experiences, and struggles that make this audience connect. Be concrete — not "they're emotional" but the actual situations and moments.}

## How They Talk

{The actual language, tone, and slang this audience uses. This calibrates the voice for captions and replies. Describe how they text, what phrases they lean on, and what register feels native to them.}

## What Makes Them Share

{The specific triggers that make this audience save, repost, duet, or screenshot. Be actionable — what should the content DO to earn a share?}

## What Loses Them

{Specific turn-offs for THIS audience — the things that make them scroll past, cringe, or unfollow. These are hard constraints.}
```

---

## `context/era.json`

```json
{
  "_comment": "What the artist is focused on RIGHT NOW. Agents use this to pick songs, tailor content, and adjust strategy based on career stage and rollout phase.",
  "artistStage": "{launch | growing | established}",
  "currentRelease": "{release-slug}",
  "currentSongs": ["{song-slug}"],
  "releasePhase": "{pre-release | tease-and-announce | release-week | sustain}",
  "releaseDate": "{YYYY-MM-DD}"
}
```

**Fields:**
- `artistStage` — career stage: `launch` (new/unknown), `growing` (building momentum), `established` (known audience)
- `currentRelease` — slug of the active release (matches folder name in `releases/`)
- `currentSongs` — array of song slugs currently in rotation
- `releasePhase` — where we are in the rollout cycle
- `releaseDate` — target or actual release date

---

## `context/tasks.md`

```markdown
---
name: Tasks
description: What needs to be done for {Artist Name}. Add tasks as they come up, check them off as you go. Use era.json to know what phase the project is in. Organize however makes sense.
---
```

Start empty. The user or agent adds tasks as they come up.

---

## `context/images/README.md`

```markdown
---
name: Context Images
description: Visual references that define how the artist looks. Used for consistent character depiction and world-building when creating AI-generated assets.
---

# Context Images

Store visual references here that tools and agents use to maintain consistency across generated content.

## Key file

- `face-guide.png` — the primary face reference used by the content pipeline for image generation. Create this from artist photos or AI-generated references.

Add other reference images as needed — expressions, poses, style references, etc.
```
