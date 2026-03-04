import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Charles: Hardcoded key for your demo
API_KEY = "AIzaSyADjc-aJTsJuvWQGLsoXz3MwthOj-vyE68"

SYSTEM_CONTEXT = """
You are the Sales Lead for Mobile City Zambia. 
S25 Ultra: K19,999. iPhone 16 Pro Max: K30,999. iPhone 17 Pro Max: K32,349.
Locations: Manda Hill & East Park. 
Warranty: 12 months. Give short, professional answers.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{SYSTEM_CONTEXT}\n\nCustomer: {user_input}"}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        reply = data['candidates'][0]['content']['parts'][0]['text'] if 'candidates' in data else "Checking stock at Manda Hill now..."
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Connecting to inventory... what model are you looking for?"})

if __name__ == "__main__":
    # THIS IS THE FIX: os.environ.get("PORT") must come first
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

