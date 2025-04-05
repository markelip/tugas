from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ API Key tidak ditemukan! Cek .env atau Variables di Railway!")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

responses = {
    "A": "📢 Kabar terkini: Chatbot ini sedang dikembangkan!",
    "B": "🤖 Chatbot adalah program yang bisa berkomunikasi dengan manusia melalui teks atau suara.",
    "C": "🛠️ Cara menggunakan chatbot ini: Ketik pilihan A, B, C, atau pesan bebas!",
    "D": "👋 Terima kasih sudah menggunakan Chatbot by Farouq! Sampai jumpa!",
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip().upper()

    if user_message in responses:
        bot_response = responses[user_message]
    else:
        try:
            response = model.generate_content(user_message, generation_config={"max_output_tokens": 60})
            bot_response = response.text or "❌ Tidak bisa mendapatkan respons dari AI"
        except Exception as e:
            bot_response = f"⚠️ Terjadi kesalahan AI: {str(e)}"

    return jsonify({"response": bot_response})

@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
