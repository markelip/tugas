from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load variabel dari file .env (hanya berfungsi secara lokal)
load_dotenv()

# Ambil API Key dari environment
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ API Key tidak ditemukan! Cek .env atau Variables di Railway!")

print(f"✅ API Key ditemukan: {API_KEY[:5]}...")  # Debugging, cuma nampilin sebagian
print(f"🔍 API Key dari Railway: {API_KEY}")  # Cek API Key terbaca atau nggak

# Konfigurasi API Key & Model
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    print(f"⚠️ Gagal menghubungkan ke Gemini API: {e}")
    model = None

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
        if model is None:
            bot_response = "⚠️ AI sedang tidak tersedia, coba lagi nanti!"
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
    port = int(os.getenv("PORT", 5000))  # Gunakan PORT dari Railway
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
