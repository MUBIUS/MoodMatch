# 🎭 MoodMatch — Mood-to-Anything Recommender

> A hybrid knowledge-based + AI recommendation system that takes your current vibe in natural language and returns personalized recommendations across games, music, movies, or study topics.

---

## 📌 Project Overview

**Subject:** Recommendation Systems (CSDO8022)  
**Concept Coverage:** Hybrid RS (Module 5), Knowledge-Based RS (Module 4), Content-Based Filtering (Module 3), Evaluation Metrics (Module 6)  
**Stack:** HTML + CSS + Vanilla JS (single file, no build step)  
**AI Backend:** Claude API (`claude-sonnet-4-20250514`) via `fetch()`  
**Build Time:** ~30 minutes with vibe coding

The user types something like `"stressed but need focus"` or `"happy and want something chill"` and the app:
1. Parses the mood using Claude API
2. Maps it to content tags internally (knowledge-based layer)
3. Returns 4–6 ranked recommendations with match scores and reasoning (content-based layer)
4. Displays evaluation stats (coverage, novelty) — hybrid RS explanation

---

## 🗂️ File Structure

```
moodmatch/
└── index.html        ← entire app lives here (single file)
```

No npm. No framework. No build. Just one HTML file.

---

## 🎨 Visual Design Spec

**Aesthetic:** Dark, moody, slightly cinematic. Think music streaming app meets terminal.

**Color Palette (CSS variables):**
```css
--bg:        #0a0a0f
--surface:   #13131a
--card:      #1c1c27
--accent:    #7c6aff   /* purple-violet */
--accent2:   #ff6a8a   /* rose pink */
--text:      #e8e8f0
--muted:     #6b6b80
--border:    #2a2a3a
```

**Typography:**
- Headings: `'Syne'` from Google Fonts (bold, geometric)
- Body: `'DM Sans'` from Google Fonts (clean, readable)

**Layout:**
- Centered single-column, max-width 680px
- Large mood input at the top (textarea, glowing border on focus)
- Category pill selector below input (Games / Music / Movies / Study)
- Results appear below as animated cards
- Each card has: Title, Match % bar, 2-line reasoning, tag chips

**Animations:**
- Cards fade + slide up on appear (`@keyframes slideUp`)
- Input border pulses with a soft glow while API call is loading
- Match % bar fills with a width transition on render
- Skeleton loader cards while waiting for API response

---

## 🧩 App Sections

### 1. Header
```
MOODMATCH
Type your vibe. Get your match.
```
Subtitle in muted color. No logo needed.

### 2. Mood Input
- `<textarea>` placeholder: `"e.g. stressed but need to focus..."`
- Max 150 characters, show char counter bottom-right
- On focus: border glows with `--accent` color

### 3. Category Selector
Four pill buttons (single-select):
- 🎮 Games
- 🎵 Music  
- 🎬 Movies
- 📚 Study

Default selected: **Games**. Selected pill gets accent background.

### 4. Recommend Button
- Label: `Find My Match →`
- Full-width, accent background, rounded
- Disabled + spinner while loading

### 5. Results Grid
Appears below the button after API responds.

**Each result card contains:**
- Title (bold)
- Genre/type tags (small chips, muted border)
- Match score bar: label "Match" + colored progress bar (0–100%)
- 2-line "Why this?" explanation in muted italic text

**Card border:** thin `--border` line, subtle left accent bar colored by match score (high = `--accent`, mid = yellow, low = `--muted`)

### 6. RS Concept Footer (inside results section)
After results load, show a small info box:
```
⚙️ How this works
This uses a Hybrid Recommendation approach:
Knowledge-Based layer maps your mood → content tags.
Content-Based layer scores each item by tag overlap.
```
Keep it minimal. One sentence per layer.

---

## 🔌 Claude API Integration

### Endpoint
```
POST https://api.anthropic.com/v1/messages
```

### Headers
```json
{
  "Content-Type": "application/json",
  "x-api-key": "YOUR_API_KEY_HERE",
  "anthropic-version": "2023-06-01",
  "anthropic-dangerous-direct-browser-access": "true"
}
```

### System Prompt
```
You are a recommendation engine. The user gives you their current mood or vibe in natural language. You must return a JSON array of 5 recommendations for the given category.

Each item must follow this exact structure:
{
  "title": "string",
  "tags": ["tag1", "tag2", "tag3"],
  "match": number between 60 and 99,
  "reason": "One sentence explanation of why this matches the mood. Max 20 words."
}

Return ONLY a raw JSON array. No markdown, no explanation, no backticks. Just the array.
```

### User Message Template
```
Mood: "${userMood}"
Category: "${selectedCategory}"
```

### Response Parsing
```javascript
const raw = data.content[0].text.trim();
const recommendations = JSON.parse(raw);
```

Wrap in try/catch. On error, show: `"Couldn't read your vibe. Try describing it differently."`

---

## 🔁 App Logic Flow

```
User types mood → selects category → clicks button
  → disable button, show skeleton cards
  → call Claude API with system prompt + user message
  → parse JSON response
  → render 5 result cards with animation
  → show RS concept footer
  → re-enable button
```

---

## 📐 Result Card HTML Structure

```html
<div class="card">
  <div class="card-accent-bar"></div>  <!-- left colored bar -->
  <div class="card-content">
    <h3 class="card-title">Dark Souls III</h3>
    <div class="card-tags">
      <span class="tag">challenging</span>
      <span class="tag">focus</span>
      <span class="tag">atmospheric</span>
    </div>
    <div class="match-bar-wrapper">
      <span class="match-label">Match</span>
      <div class="match-bar">
        <div class="match-fill" style="width: 88%"></div>
      </div>
      <span class="match-score">88%</span>
    </div>
    <p class="card-reason">Demands full attention — perfect for channeling stress into flow.</p>
  </div>
</div>
```

---

## 🦴 Skeleton Loader

Show 3 skeleton cards while loading:

```html
<div class="card skeleton">
  <div class="skel-line wide"></div>
  <div class="skel-line medium"></div>
  <div class="skel-line short"></div>
</div>
```

CSS: Use a shimmer animation (`background: linear-gradient(...)` shifting via keyframes).

---

## ⚙️ API Key Handling

Add an `<input type="password">` field at the very top of the page labeled **"Anthropic API Key"** — store the value in a JS variable. No hardcoding. No localStorage. Just a visible input the user fills before using the app.

Style it like a secondary input, muted, small font.

---

## 📋 Sample Moods to Test With

| Mood Input | Category | Expected Vibe |
|---|---|---|
| "stressed but need to focus" | Games | Challenging, absorbing games |
| "happy and want something light" | Movies | Feel-good comedies |
| "melancholic and reflective" | Music | Ambient, lo-fi, indie |
| "bored and need mental stimulation" | Study | Interesting rabbit holes |
| "anxious, need distraction" | Games | Easy, satisfying games |

---

## ✅ Checklist for Vibe Coder

- [ ] Single `index.html` file, no external dependencies except Google Fonts + Anthropic API
- [ ] API key input field at top of page
- [ ] Mood textarea with char counter
- [ ] 4 category pill buttons, single-select
- [ ] `Find My Match →` button with loading state
- [ ] Skeleton loader (3 cards) during API call
- [ ] 5 animated result cards with title, tags, match bar, reason
- [ ] RS concept explanation box below results
- [ ] Error handling with user-friendly message
- [ ] Dark theme, `Syne` + `DM Sans` fonts, accent color `#7c6aff`
- [ ] Mobile responsive (single column, 95% width on small screens)

---

## 🧠 RS Concepts Demonstrated

| Feature | RS Concept |
|---|---|
| Mood → tag mapping via Claude | Knowledge-Based Recommendation (Module 4) |
| Match % based on tag overlap | Content-Based Filtering (Module 3) |
| Claude + rule layer combined | Hybrid / Ensemble RS (Module 5) |
| Match %, reasoning transparency | Evaluation: Confidence & Trust (Module 6.1) |

---

*Built for CSDO8022 — Recommendation Systems, BE Computer Engineering, Sem 7*
