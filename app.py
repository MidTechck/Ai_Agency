import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Charles: Hardcoded key for the demo
API_KEY = "AIzaSyADjc-aJTsJuvWQGLsoXz3MwthOj-vyE68"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"Mobile City Zambia Sales Lead. S25 Ultra: K19,999. iPhone 16 Pro Max: K30,999. Locations: Manda Hill & East Park. Short answers.\n\nCustomer: {user_input}"}]}]
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        reply = data['candidates'][0]['content']['parts'][0]['text'] if 'candidates' in data else "Checking stock..."
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Connecting to inventory..."})

if __name__ == "__main__":
    # This is the most important line for Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

