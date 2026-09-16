import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize Gemini Client
# Set GEMINI_API_KEY in your Vercel Dashboard -> Settings -> Environment Variables
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API is running"}), 200


@app.route("/translate", methods=["POST"])
@app.route("/api/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        if not client:
            return jsonify({"error": "GEMINI_API_KEY is not configured on Vercel"}), 500

        prompt = f"Translate the following Moroccan Darija text to English. Return only the translated English text:\n\n{text}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return jsonify({"translation": response.text.strip()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Required for local testing (`python api/index.py`)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
