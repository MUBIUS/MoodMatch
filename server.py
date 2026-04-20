import json
import os
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


HOST = "127.0.0.1"
PORT = 5500
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:latest")
MODELS = [
  "gemini-2.0-flash",
  "gemini-1.5-flash",
  "gemini-1.5-flash-8b"
]


SYSTEM_PROMPT = """You are a recommendation engine. The user gives you their current mood or vibe in natural language. You must return a JSON array of 5 recommendations for the given category.

Each item must follow this exact structure:
{
  "title": "string",
  "tags": ["tag1", "tag2", "tag3"],
  "match": number between 60 and 99,
  "reason": "One sentence explanation of why this matches the mood. Max 20 words."
}

Return ONLY a raw JSON array. No markdown, no explanation, no backticks. Just the array.
"""


def parse_json_array(raw_text):
  text = raw_text.strip()
  try:
    return json.loads(text)
  except json.JSONDecodeError:
    fenced_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if fenced_match:
      return json.loads(fenced_match.group(1).strip())
    first = text.find("[")
    last = text.rfind("]")
    if first >= 0 and last > first:
      return json.loads(text[first:last + 1])
    raise


def call_ollama(mood, category):
  user_prompt = f'Mood: "{mood}"\nCategory: "{category}"'
  payload = {
    "model": OLLAMA_MODEL,
    "stream": False,
    "messages": [
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": user_prompt}
    ]
  }

  req = Request(
    url=f"{OLLAMA_URL}/api/chat",
    method="POST",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
  )

  try:
    with urlopen(req, timeout=180) as response:
      body = response.read().decode("utf-8")
  except HTTPError as err:
    detail = err.read().decode("utf-8", errors="replace")
    raise RuntimeError(f"Ollama API error ({err.code}): {detail}") from err
  except URLError as err:
    raise RuntimeError(f"Cannot reach Ollama at {OLLAMA_URL}. Start Ollama first.") from err

  data = json.loads(body)
  try:
    text = data["message"]["content"]
  except (KeyError, TypeError) as err:
    raise RuntimeError("Ollama response format was unexpected.") from err

  parsed = parse_json_array(text)
  if not isinstance(parsed, list):
    raise RuntimeError("Ollama did not return a JSON array.")
  return parsed[:5]


def call_gemini(mood, category):
  api_key = os.environ.get("GEMINI_API_KEY", "").strip()
  if not api_key:
    raise RuntimeError("Server is missing GEMINI_API_KEY.")

  user_prompt = f'Mood: "{mood}"\nCategory: "{category}"'
  last_error = None

  for model in MODELS:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
      "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
      "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
      "generationConfig": {
        "temperature": 0.7,
        "responseMimeType": "application/json"
      }
    }

    req = Request(
      url=url,
      method="POST",
      data=json.dumps(payload).encode("utf-8"),
      headers={"Content-Type": "application/json"}
    )

    try:
      with urlopen(req, timeout=25) as response:
        body = response.read().decode("utf-8")
      data = json.loads(body)
      text = data["candidates"][0]["content"]["parts"][0]["text"]
      parsed = parse_json_array(text)
      if not isinstance(parsed, list):
        raise RuntimeError("Gemini did not return a JSON array.")
      return parsed[:5]
    except HTTPError as err:
      detail = err.read().decode("utf-8", errors="replace")
      # 404 means model unsupported for this account/version. Try next model.
      if err.code == 404:
        last_error = RuntimeError(f"Model unavailable: {model}")
        continue
      raise RuntimeError(f"Gemini API error ({err.code}): {detail}") from err
    except URLError as err:
      raise RuntimeError(f"Network error while calling Gemini: {err.reason}") from err
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as err:
      raise RuntimeError("Gemini response format was unexpected.") from err

  raise RuntimeError(str(last_error) if last_error else "No Gemini model available.")


class MoodMatchHandler(SimpleHTTPRequestHandler):
  def do_POST(self):
    if self.path != "/api/recommend":
      self.send_error(404, "Endpoint not found")
      return

    content_length = int(self.headers.get("Content-Length", "0"))
    raw_body = self.rfile.read(content_length).decode("utf-8")

    try:
      payload = json.loads(raw_body or "{}")
      mood = str(payload.get("mood", "")).strip()
      category = str(payload.get("category", "Games")).strip()

      if not mood:
        self.send_json({"error": "Mood is required."}, status=400)
        return

      # Prefer local Ollama for free usage; fallback to Gemini only if key is set.
      if os.environ.get("GEMINI_API_KEY", "").strip():
        recommendations = call_gemini(mood=mood, category=category)
      else:
        recommendations = call_ollama(mood=mood, category=category)
      self.send_json({"recommendations": recommendations})
    except json.JSONDecodeError:
      self.send_json({"error": "Invalid JSON request body."}, status=400)
    except Exception as err:
      self.send_json({"error": str(err)}, status=500)

  def send_json(self, payload, status=200):
    body = json.dumps(payload).encode("utf-8")
    self.send_response(status)
    self.send_header("Content-Type", "application/json; charset=utf-8")
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)


if __name__ == "__main__":
  server = ThreadingHTTPServer((HOST, PORT), MoodMatchHandler)
  print(f"Serving MoodMatch at http://{HOST}:{PORT}")
  print(f"Using Ollama model: {OLLAMA_MODEL} @ {OLLAMA_URL}")
  print("Optional: set GEMINI_API_KEY to use Gemini instead.")
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    pass
  finally:
    server.server_close()
