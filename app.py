import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
GEMINI_KEY = 'AIzaSyDeS7h05h4axgwzZuOQPKNgR_u2hMUflDo' 

# Your Ndola Shop Identity
STOCK_CONTEXT = """
You are the AI Sales Assistant for Apex Electronics Ndola. 
Location: Near Misundu. 
Products: 
- iPhone 15 (K18,500)
- Samsung S24 (K21,000)
- HP Laptop Core i5 (K7,500)
- MacBook Air M2 (K24,000)
Delivery: K50 in Ndola.
Instructions: Answer briefly, use Kwacha (K), and be very polite.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    
    # 2026 STABLE ENDPOINT
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{STOCK_CONTEXT}\nUser: {user_msg}"}]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        if 'candidates' in data:
            bot_reply = data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": bot_reply})
        else:
            # If 2.5 is still in rollout, fallback to 2.0
            print("Trying fallback model...")
            url_fallback = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
            response = requests.post(url_fallback, json=payload, timeout=10)
            data = response.json()
            bot_reply = data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"reply": "System is refreshing for the new day. Try again!"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

