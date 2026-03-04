import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Charles: Using your specific key directly in the code for the demo
API_KEY = "AIzaSyADjc-aJTsJuvWQGLsoXz3MwthOj-vyE68"

SYSTEM_CONTEXT = """
You are the Sales Lead for Mobile City Zambia. 
PRICES: 
- S25 Ultra: K19,999
- iPhone 16 Pro Max: K30,999
- iPhone 17 Pro Max: K32,349
LOCATIONS: Manda Hill & East Park. 
WARRANTY: 12 months.
Keep answers short, professional, and very helpful.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    # Using the stable March 2026 Gemini 3 Flash endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{SYSTEM_CONTEXT}\n\nCustomer: {user_input}"}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        
        if 'candidates' in data:
            reply = data['candidates'][0]['content']['parts'][0]['text']
        else:
            reply = "I'm checking our latest stock at Manda Hill. How can I help you today?"
            
    except Exception as e:
        reply = "Our connection is a bit slow. Are you looking for the S25 or iPhone 16 today?"
        
    return jsonify({"reply": reply})

if __name__ == "__main__":
    # CRITICAL: This is why the app fails to respond. 
    # Railway tells the app which port to use via the PORT variable.
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

