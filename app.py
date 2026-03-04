import os
from flask import Flask, request, jsonify
# Import your AI logic here (ensure your Gemini API key is set in Railway Variables)

app = Flask(__name__)

@app.route('/')
def home():
    return "Mobile City AI Enterprise Server is Online."

@app.route('/chat', methods=['POST'])
def chat():
    # Your chat logic goes here
    return jsonify({"status": "success", "message": "AI is responding"})

if __name__ == "__main__":
    # BULLETPROOF PORT LOGIC: This is the 'bridge' for Railway
    # It looks for the port Railway provides, defaulting to 5000 for local tests
    port = int(os.environ.get("PORT", 5000))
    # Using 0.0.0.0 allows the app to be reachable outside the container
    app.run(host='0.0.0.0', port=port)

