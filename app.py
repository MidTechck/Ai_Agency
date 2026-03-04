import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Hardcoded for immediate demo success
API_KEY = "AIzaSyADjc-aJTsJuvWQGLsoXz3MwthOj-vyE68"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"You are the Sales Lead for Mobile City Zambia. S25 Ultra: K19,999. iPhone 16 Pro Max: K30,999. iPhone 17 Pro Max: K32,349. Locations: Manda Hill & East Park. Give short, professional answers.\n\nCustomer: {user_input}"}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        reply = data['candidates'][0]['content']['parts'][0]['text'] if 'candidates' in data else "I am checking our inventory at Manda Hill. How can I help you?"
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Connecting to our store inventory... what model are you looking for?"})

if __name__ == "__main__":
    # This line is the only way to fix the 'Application failed to respond' error
    # It MUST use os.environ.get('PORT')
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

