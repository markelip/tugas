from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env (bisa diabaikan di Railway, karena pakai Environment Variable)
load_dotenv()

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# API key dari environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Pakai model yang bener
model = genai.GenerativeModel("models/gemini-pro")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    prompt = f"""
    Kamu adalah chatbot AI bernama BotFarouq. Jawab dengan gaya Gen Z yang santai, lucu, dan pintar. Boleh pakai emoji, bahasa gaul, dan jokes receh.

    User: {user_input}
    Bot:
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
