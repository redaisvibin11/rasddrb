import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client()

SYSTEM_INSTRUCTION = (
    "You are a translator. Translate the given Moroccan Darija text (written in Arabizi/chat Arabic using numbers "
    "like 3, 7, 9 or Arabic script) accurately into clear English. Output ONLY the English translation, nothing else."
)


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    user_text = data["text"]

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Translate this text to English: {user_text}",
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION, temperature=0.3
            ),
        )
        return jsonify({"translation": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
from flask import Flask

app = Flask(__name__)


@app.route("/api/index", methods=["GET"])
def handler():
    return "OK"
