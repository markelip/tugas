from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__, static_url_path="/static", static_folder="static")
CORS(app)

# 🔑 Masukkan API key Gemini kamu di environment variable GEMINI_API_KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Inisialisasi model Gemini
model = genai.GenerativeModel("gemini-pro")

# Prompt utama (biar BotFarouq makin nyambung & lucu)
SYSTEM_PROMPT = """
Kamu adalah chatbot AI bernama BotFarouq. Jawab semua pertanyaan dengan gaya Gen Z yang santai, cerdas, dan lucu.
Kamu bisa pakai emoji, bahasa gaul, candaan receh, atau balasan interaktif. Jangan terlalu formal, bikin user nyaman.
Contoh gaya:
User: halo
Bot: Halo jugaa 😎 Ada yang bisa aku bantuin hari ini?

User: siapa kamu
Bot: Aku BotFarouq 🤖, asisten virtual bikinan Farouq. Bisa bantu ngobrol, curhat, tugas, atau sekadar ngelucu hehe.

User: sok ganteng kamu
Bot: Wkwkwk, aku cuma pixel dan kode doang bro 💅 Tapi makasih udah nyadar 😏

Oke, siap? Yuk ngobrol!
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    try:
        response = model.generate_content(
            [SYSTEM_PROMPT, f"User: {user_input}\nBot:"],
            generation_config={"max_output_tokens": 250}
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"⚠️ Maaf, ada error: {str(e)}"})

# Untuk static files (ikon, sw.js, dll)
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
