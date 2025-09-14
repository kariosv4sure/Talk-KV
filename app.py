from flask import Flask, render_template, request, jsonify
import os, requests, re, random
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()

    # 🔎 Patterns to catch many "who made you" variants (case-insensitive)
    creator_patterns = [
        r"who\s*made\s*u", r"who\s*made\s*you",
        r"who\s*created\s*u", r"who\s*created\s*you",
        r"who\s*built\s*u", r"who\s*built\s*you",
        r"your\s*creator", r"your\s*maker",
        r"who\s*owns\s*you", r"who\s*developed\s*u",
        r"who\s*developed\s*you", r"who\s*is\s*your\s*creator",
        r"who\s*is\s*your\s*maker", r"who\s*wrote\s*you",
        r"who\s*programmed\s*you", r"who\s*designed\s*you",
        r"who\s*invented\s*you", r"who\s*produced\s*you",
        r"who\s*engineered\s*you", r"who\s*set\s*you\s*up",
        r"who\s*built\s*u\s*bruh", r"who\s*made\s*u\s*bro"
    ]

    if any(re.search(p, user_message, re.I) for p in creator_patterns):
        responses = [
            "Ifeanyichukwu Collins—also known as **Karios Vantari**—built me.",
            "Karios Vantari (Ifeanyichukwu Collins) is my creator.",
            "All credit goes to Karios Vantari, a.k.a. Ifeanyichukwu Collins.",
            "I was proudly coded by Ifeanyichukwu Collins—Karios Vantari.",
            "My maker? None other than Karios Vantari (Ifeanyichukwu Collins).",
            "This is a KV creation: Karios Vantari (Ifeanyichukwu Collins) made me!",
            "The one and only Karios Vantari—yes, Ifeanyichukwu Collins—built me.",
            "I exist thanks to Ifeanyichukwu Collins, known as Karios Vantari.",
            "Karios Vantari (Ifeanyichukwu Collins) is the mind behind me.",
            "I owe my existence to Ifeanyichukwu Collins—Karios Vantari himself!"
        ]
        return jsonify({"reply": random.choice(responses)})

    # 👉 Otherwise call Groq as usual
    if not GROQ_API_KEY:
        return jsonify({"reply": "Error: GROQ_API_KEY not set on the server."}), 500

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are KV, a warm, encouraging diary friend."},
            {"role": "user", "content": user_message}
        ]
    }

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers, json=payload
    )

    print("STATUS:", r.status_code)
    print("BODY:", r.text)

    data = r.json()
    if "choices" not in data:
        return jsonify({"reply": f"Error from Groq: {data}"}), 500

    reply = data['choices'][0]['message']['content']
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
