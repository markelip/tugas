from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load variabel dari file .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API Key tidak ditemukan! Cek file .env")

# Konfigurasi API Key
genai.configure(api_key=API_KEY)

# Pilih model
model = genai.GenerativeModel("gemini-1.5-flash")

# Daftar balasan otomatis berdasarkan input user
responses = {
    "A": "📢 Kabar terkini: Chatbot ini sedang dikembangkan!",
    "B":
    "🤖 Chatbot adalah program yang bisa berkomunikasi dengan manusia melalui teks atau suara.",
    "C":
    "🛠️ Cara menggunakan chatbot ini: Ketik pilihan A, B, C, atau pesan bebas!",
    "D": "👋 Terima kasih sudah menggunakan Chatbot by Farouq! Sampai jumpa!",
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip().upper()

    # Cek apakah user memilih menu yang tersedia
    if user_message in responses:
        bot_response = responses[user_message]
    else:
        try:
            response = model.generate_content(
                user_message, generation_config={"max_output_tokens": 30})
            bot_response = response.text if response and response.text else "❌ Tidak bisa mendapatkan respons dari AI"
        except Exception as e:
            bot_response = f"⚠️ Terjadi kesalahan: {str(e)}"

    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
