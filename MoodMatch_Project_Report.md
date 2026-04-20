# Experiment No : 08

## Aim : Mini Project Report (AAI Application)

## Project Title : MoodMatch - Mood-to-Anything Recommender

## 1. Introduction
Recommendation Systems are widely used in real-world applications such as entertainment, e-learning, and gaming platforms. Traditional recommenders often rely on historical user-item interactions, but many users also need recommendations based on their **current mood** or situational intent.

This mini project, **MoodMatch**, is an interactive mood-driven recommendation system. The user enters a natural-language mood statement (for example: *"stressed but need to focus"*), chooses a category (Games, Music, Movies, or Study), and receives ranked recommendations with match percentages and short reasoning.

The project demonstrates a practical hybrid recommendation workflow:
- Natural language mood understanding using an LLM backend,
- Knowledge-based mapping from mood to semantic content descriptors,
- Content-oriented scoring and transparent recommendation display.

The interface is implemented as a simple and visually engaging single-page application, while the backend handles model inference and secure API/model integration.

---

## 2. Problem Statement
Many students understand recommendation systems in theory but find it difficult to connect concepts such as knowledge-based and content-based recommendation to an interactive real-world use case.

Static examples also fail to explain *why* a recommendation was made for a specific emotional context.

Hence, there is a need for an educational system that:
- accepts user mood in natural language,
- generates category-aware recommendations in real time,
- shows confidence/match values with explanation,
- and presents the process in an interpretable, user-friendly interface.

---

## 3. Objectives
- To build a mood-aware recommendation application for multiple categories.
- To implement a hybrid recommendation flow using LLM understanding + structured scoring.
- To provide explainable outputs via tags, match %, and short reasons.
- To design an interactive web UI with responsive dark-theme visualization.
- To support free/local inference mode (Ollama) for cost-free academic demonstration.

---

## 4. Software Requirements
**Operating System:** Windows 10 / Windows 11  
**Programming Language:** Python 3.9+ , HTML/CSS/JavaScript  
**Tools / IDE:** VS Code / Cursor, Command Prompt / PowerShell  
**Framework / UI:** Vanilla Web UI + Python HTTP backend  
**Model Runtime:** Ollama (local), optional Gemini API backend

**Libraries / Components Used:**
- Python built-in `http.server` (backend endpoint serving + API routing)
- Python built-in `urllib` (LLM API calls)
- HTML + CSS + JavaScript (frontend interface)
- Ollama local server (free local model inference)

---

## 5. Methodology

### Step 1: User Input Collection
- User enters mood text (max 150 characters).
- User selects one category from: Games, Music, Movies, Study.

### Step 2: Request Handling
- Frontend sends a POST request to backend endpoint `/api/recommend`.
- Request contains:
  - mood text
  - selected category

### Step 3: Recommendation Generation (Hybrid Flow)
- Backend builds a structured prompt for the language model.
- Model returns a JSON array of 5 recommendations with:
  - title
  - tags
  - match score
  - short reason

- Primary mode: local Ollama model (free and offline-capable after setup).  
- Optional mode: Gemini API (when key is available and quota permits).

### Step 4: Validation and Normalization
- Backend/frontend safely parse and validate model output.
- Invalid or malformed response is handled gracefully.
- Match values are normalized and output is limited to top 5 items.

### Step 5: Visualization and Interaction
- Frontend renders animated recommendation cards.
- Each card includes:
  - title
  - tag chips
  - match bar with percentage
  - short rationale
- Additional info shown:
  - coverage metric
  - novelty metric
  - brief “How this works” explanation box

---

## 6. Results
The system successfully generates mood-aligned recommendations for different categories in real time through the interactive UI.

Observed outcomes:
- Correct request-response pipeline from UI -> backend -> model -> UI.
- Recommendations displayed with interpretable attributes (match %, tags, reason).
- Local Ollama integration works without paid API usage.
- Interface remains responsive and suitable for classroom demonstration.

Example tested mood:
- Input: *"happy and want something light"*  
- Category: *Movies*  
- Output: Five suitable recommendations with high match scores and clear reasoning.

---

## 7. Future Scope
- Add persistent user profiles and preference memory for personalization.
- Introduce explicit weighting between mood relevance and novelty.
- Add feedback loop (like/dislike) to improve future recommendations.
- Support multilingual mood input.
- Expand categories (Books, Podcasts, Activities, Food).
- Compare multiple model backends (Ollama vs cloud LLMs) on quality and latency.
- Deploy backend and frontend as hosted demo for remote access.

---

## 8. References
- F. Ricci, L. Rokach, and B. Shapira, *Recommender Systems Handbook*, Springer.
- Charu C. Aggarwal, *Recommender Systems: The Textbook*, Springer.
- Ollama Documentation: https://ollama.com/docs
- Stream and API Design Inspiration: https://developer.mozilla.org/
- Google Gemini API Docs: https://ai.google.dev/

---

## 9. Conclusion
The **MoodMatch** mini project demonstrates a practical and explainable recommendation system aligned with AAI syllabus goals. By combining natural-language mood understanding, hybrid recommendation logic, and an interactive visual interface, the project converts recommendation theory into a tangible application.

Using local Ollama-based inference also makes the system cost-effective and suitable for academic environments where free and reproducible demonstrations are important.
