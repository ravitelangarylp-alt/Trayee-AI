import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("GOOGLE_API_KEY")

if api_key:
    print(f"✅ API Key found: {api_key[:5]}...{api_key[-4:]}", flush=True)
else:
    print("❌ ERROR: API Key NOT FOUND!", flush=True)

client = genai.Client(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        prompt = f"You are 'Trayee AI', an expert Sanskrit chatbot. You must reply to the user's query strictly in the Sanskrit language using the Devanagari script. User Query: {user_message}"
        
        print("👉 Sending prompt to Gemini...", flush=True)
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        
        print("✅ Received response from Gemini!", flush=True)
        return jsonify({"reply": response.text})
        
    except Exception as e:
        print(f"🔥 GEMINI API ERROR: {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
