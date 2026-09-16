import os

from flask import Flask, jsonify, request
from google import genai

app = Flask(__name__)

MODEL = "gemini-2.0-flash"

SYSTEM_PROMPT = (
    "You are a translator for Moroccan Darija. "
    "Translate the user's Darija text into natural English. "
    "Reply with the translation only, no explanations or quotes."
)

_client = None


def get_client():
    """Create the Gemini client lazily so a missing key doesn't crash cold start."""
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set in the environment.")
        _client = genai.Client(api_key=api_key)
    return _client


# Several paths are registered because Vercel rewrites keep the destination
# path when the request reaches the function.
@app.route("/", methods=["POST"])
@app.route("/translate", methods=["POST"])
@app.route("/api/index", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        client = get_client()
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{SYSTEM_PROMPT}\n\nDarija text:\n{text}",
        )
        translation = (response.text or "").strip()
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 500

    if not translation:
        return jsonify({"error": "Empty response from the model"}), 502

    return jsonify({"translation": translation})


@app.route("/", methods=["GET"])
@app.route("/translate", methods=["GET"])
@app.route("/api/index", methods=["GET"])
def health():
    return jsonify(
        {"status": "ok", "key_loaded": bool(os.environ.get("GEMINI_API_KEY"))}
    )


# Local development only. Vercel imports `app` directly and ignores this block.
if __name__ == "__main__":
    app.run(port=7860, debug=True)
