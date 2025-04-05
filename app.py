from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

responses = {
    "A": "📢 Info: Chatbot ini lagi dikembangin!",
    "B": "🤖 Chatbot bisa ngobrol dengan manusia via teks.",
    "C": "🛠️ Cara pakai: ketik A, B, C, atau pesan bebas.",
    "D": "👋 Makasih udah pakai chatbot ini!"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip().upper()
    if message in responses:
        return jsonify({"response": responses[message]})
    try:
        response = model.generate_content(message, generation_config={"max_output_tokens": 50})
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
