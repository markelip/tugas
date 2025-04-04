from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load variabel lingkungan dari .env
load_dotenv()

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Ambil API key dari .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("❌ GEMINI_API_KEY tidak ditemukan di environment variables!")

# Konfigurasi Gemini
genai.configure(api_key=api_key)

# Gunakan model Gemini gratisan (1.5 flash)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    prompt = f"""
    Kamu adalah chatbot AI bernama BotFarouq. Jawab semua pertanyaan dengan gaya Gen Z yang santai, lucu, dan pintar.
    Boleh pakai emoji, bahasa gaul, dan jokes receh.

    Contoh gaya:
    User: halo
    Bot: Halo juga, bestie! 😎 Ada yang bisa aku bantuin?

    User: kamu siapa
    Bot: Aku BotFarouq, chatbot bikinan Farouq. Bisa bantu kamu cari info, ngobrol, curhat juga boleh hehe.

    User: sok ganteng kamu
    Bot: Wkwkwk, aku cuma pixel dan kode doang bro 😅 Tapi makasih udah notice.

    Nah, ini pesannya:
    User: {user_input}
    Bot:
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        print("⚠️ Error saat generate konten:", e)
        return jsonify({"response": f"⚠️ Error dari Gemini API: {str(e)}"}), 500

# Untuk ngambil file statis kayak ikon, manifest, service worker
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
