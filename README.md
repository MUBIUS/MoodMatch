# MoodMatch - Mood-to-Anything Recommender

MoodMatch is an interactive recommendation system that takes your mood in natural language and returns personalized recommendations across:

- Games
- Music
- Movies
- Study

It is designed as a simple, visually engaging educational mini project for recommendation systems concepts.

---

## Features

- Natural-language mood input (for example: `"stressed but need to focus"`)
- Category-based recommendation generation
- 5 ranked recommendations with:
  - title
  - tag chips
  - match percentage
  - short explanation (`why this matches`)
- Animated dark-themed UI
- Skeleton loaders and graceful error handling
- Backend-powered model integration (API key never exposed in browser)

---

## Recommendation Approach

MoodMatch demonstrates a **hybrid recommendation-style flow**:

1. **Mood understanding** via LLM prompt interpretation  
2. **Knowledge-based mapping** of mood + category intent  
3. **Content-style output scoring** with transparent tags and match%

It also displays simple metrics (coverage and novelty) for explainability.

---

## Tech Stack

- **Frontend:** HTML, CSS, Vanilla JavaScript (`index.html`)
- **Backend:** Python (`server.py`, built-in `http.server`)
- **Model Runtime (default):** Ollama local model (free)
- **Optional Cloud Runtime:** Gemini API (if key is configured)

---

## Project Structure

```text
Mini Project/
├── index.html
├── server.py
├── README.md
├── .gitignore
├── RUN_GEMINI.md
└── MoodMatch_Project_Report.md
```

---

## Prerequisites

- Python 3.9+
- Ollama installed and running
  - Download: [https://ollama.com/download](https://ollama.com/download)

---

## Run with Ollama (Recommended and Free)

### 1) Pull a local model (once)

You can use a model you already have. Example:

```powershell
ollama pull qwen3:latest
```

### 2) Start the backend server

From project folder:

```powershell
Remove-Item Env:GEMINI_API_KEY -ErrorAction SilentlyContinue
$env:OLLAMA_MODEL="qwen3:latest"
python server.py
```

### 3) Open the app

Go to:

`http://127.0.0.1:5500`

---

## Optional: Run with Gemini API

If you want cloud inference instead of local Ollama:

```powershell
$env:GEMINI_API_KEY="YOUR_KEY_HERE"
python server.py
```

When `GEMINI_API_KEY` is present, backend can use Gemini path; otherwise it uses Ollama.

---

## API Endpoint

Backend endpoint used by frontend:

- `POST /api/recommend`

Request body:

```json
{
  "mood": "happy and want something light",
  "category": "Movies"
}
```

Response body:

```json
{
  "recommendations": [
    {
      "title": "Example Title",
      "tags": ["tag1", "tag2", "tag3"],
      "match": 88,
      "reason": "Short reason why this matches."
    }
  ]
}
```

---

## Troubleshooting

- **Port already in use (`5500`)**
  - Stop existing process using port 5500, then restart `python server.py`.

- **Slow first response with Ollama**
  - First generation can take longer due to model warm-up.
  - Subsequent calls are usually faster.

- **Gemini quota/rate-limit errors (`429`)**
  - Your API key/project may have exhausted quota; switch to Ollama for free local usage.

---

## Academic Context

This mini project aligns with Recommendation Systems coursework by showcasing:

- practical hybrid recommendation pipeline,
- interpretable recommendation outputs,
- real-time interactive user experience.

---

## License

For educational and academic use.
