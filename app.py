from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env (biar aman dari public repo)
load_dotenv()

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

# Masukin API key dari environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Inisialisasi model Gemini
model = genai.GenerativeModel("gemini-pro")

# Route utama
@app.route("/")
def index():
    return render_template("index.html")

# Route chat
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
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

# Untuk file statis (ikon, sw.js, dll)
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
