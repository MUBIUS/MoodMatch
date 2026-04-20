# Run MoodMatch with Gemini Backend

1. Set your Gemini API key in the shell:
   - PowerShell:
     - `$env:GEMINI_API_KEY="your_api_key_here"`

2. Start backend + frontend server:
   - `python server.py`

3. Open:
   - `http://127.0.0.1:5500`

Notes:
- The key is read only on backend from `GEMINI_API_KEY`.
- Browser never sees your API key.
