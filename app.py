from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # ⬅️ Tambahan ini
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, origins=["https://b4f70631.tugas.pages.dev"])  # ⬅️ Izinkan domain Cloudflare

# Load variabel dari file .env (lokal)
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ API Key tidak ditemukan! Cek .env atau Railway Variables!")

print(f"✅ API Key ditemukan: {API_KEY[:5]}...")

# Konfigurasi API
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    print(f"⚠️ Gagal konek ke Gemini: {e}")
    model = None

# Balasan preset
responses = {
    "A": "📢 Kabar terkini: Chatbot ini sedang dikembangkan!",
    "B": "🤖 Chatbot adalah program yang bisa ngobrol sama manusia.",
    "C": "🛠️ Cara pakai: Ketik A, B, C, atau pesan bebas!",
    "D": "👋 Makasih udah pakai Chatbot by Farouq!",
}

@app.route("/")
def index():
    return "✅ Backend aktif di Railway!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip().upper()

    if user_message in responses:
        bot_response = responses[user_message]
    else:
        if model is None:
            bot_response = "⚠️ AI nggak tersedia, coba lagi nanti!"
        else:
            try:
                response = model.generate_content(
                    user_message, generation_config={"max_output_tokens": 50}
                )
                bot_response = response.text or "❌ AI gak ngasih jawaban."
            except Exception as e:
                bot_response = f"⚠️ Error dari AI: {str(e)}"

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
