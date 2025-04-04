from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv, dotenv_values

app = Flask(__name__)

# Load variabel dari file .env
load_dotenv()

# Coba ambil API Key dari os.getenv atau dotenv_values
API_KEY = os.getenv("GEMINI_API_KEY") or dotenv_values(".env").get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ API Key tidak ditemukan! Cek .env atau Variables di Railway!")

print(f"✅ API Key ditemukan: {API_KEY[:5]}...")  # Debugging, cuma nampilin sebagian

# Konfigurasi API Key
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    raise RuntimeError(f"⚠️ Gagal menghubungkan ke Gemini API: {str(e)}")

# Daftar balasan otomatis berdasarkan input user
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
            response = model.generate_content(
                user_message, generation_config={"max_output_tokens": 30}
            )
            bot_response = response.text if response and response.text else "❌ Tidak bisa mendapatkan respons dari AI"
        except Exception as e:
            bot_response = f"⚠️ Terjadi kesalahan saat memproses AI: {str(e)}"

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
