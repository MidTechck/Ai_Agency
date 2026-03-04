import os, requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# CEO: Using your confirmed key
API_KEY = "AIzaSyADjc-aJTsJuvWQGLsoXz3MwthOj-vyE68"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    # MARCH 2026 FIX: Using the newest stable Gemini 3 Flash model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"You are the Sales Lead for Mobile City Zambia. S25 Ultra: K19,999. iPhone 16 Pro Max: K30,999. iPhone 17 Pro Max: K32,349. Locations: Manda Hill & East Park. 12 months warranty. Give short, professional answers.\n\nCustomer: {user_input}"}]
        }]
    }
    
    try:
        # Increased timeout to 15s for stability on 3G/4G
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        
        # Monitor this in Termux!
        print(f"RESPONSE: {data}")
        
        if 'candidates' in data:
            reply = data['candidates'][0]['content']['parts'][0]['text']
        elif 'error' in data and data['error']['code'] == 429:
            reply = "I'm just pulling up our latest inventory for you. One moment!"
        else:
            # If Gemini 3 is also not found, try the universal 'gemini-flash-latest' alias
            return try_fallback(user_input)
            
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"reply": "Connecting to our store inventory... what model are you looking for?"})

def try_fallback(user_input):
    # Emergency fallback to the universal 'latest' alias
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": user_input}]}]}
    res = requests.post(url, json=payload).json()
    reply = res['candidates'][0]['content']['parts'][0]['text'] if 'candidates' in res else "How can I help you with your purchase?"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

