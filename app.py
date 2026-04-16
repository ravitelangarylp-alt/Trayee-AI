import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("GROQ_API_KEY")
if api_key:
    print(f"✅ Groq API Key found!", flush=True)
else:
    print("❌ ERROR: Groq API Key NOT FOUND!", flush=True)

client = Groq(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        prompt = f"You are 'Trayee AI', an expert Sanskrit chatbot. Reply strictly in Sanskrit using Devanagari script. User Query: {user_message}"
        
        print("👉 Sending prompt to Groq...", flush=True)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        
        print("✅ Received response!", flush=True)
        return jsonify({"reply": response.choices[0].message.content})
        
    except Exception as e:
        print(f"🔥 ERROR: {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
