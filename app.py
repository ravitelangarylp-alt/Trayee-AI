import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("CLAUDE_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        prompt = f"You are 'Trayee AI', an expert Sanskrit chatbot. Reply strictly in Sanskrit using Devanagari script. User Query: {user_message}"

        print("👉 Sending prompt to Claude...", flush=True)

        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        print("✅ Received response!", flush=True)
        return jsonify({"reply": message.content[0].text})

    except Exception as e:
        print(f"🔥 ERROR: {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
