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
        # ಫ್ರಂಟ್‌ಎಂಡ್‌ನಿಂದ ಬರುವ ಮೆಸೇಜ್ ಮತ್ತು ಫೈಲ್ ಪಡೆಯುವುದು
        user_message = request.form.get("message", "")
        uploaded_file = request.files.get("file")
        
        file_content = ""
        # ಬಳಕೆದಾರರು ವೆಬ್‌ಸೈಟ್ ಮೂಲಕ ಏನಾದರೂ ಸಣ್ಣ ಫೈಲ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ್ದರೆ ಮಾತ್ರ ಓದುವುದು
        if uploaded_file:
            file_content = uploaded_file.read().decode('utf-8')

        if not user_message and not file_content:
            return jsonify({"error": "No message or file provided"}), 400

        # Trayee AI ಗಾಗಿ ಚಿಕ್ಕದಾದ ಮತ್ತು ಸ್ಪಷ್ಟವಾದ System Prompt (ಟೋಕನ್ ಉಳಿತಾಯಕ್ಕಾಗಿ)
        system_instructions = (
            "You are 'Trayee AI', an expert Sanskrit chatbot specializing in computational linguistics and Pāṇinian grammar. "
            "Reply strictly in Sanskrit using Devanagari script."
        )

        # ಬಳಕೆದಾರರ ಪ್ರಾಂಪ್ಟ್ ರಚನೆ
        user_prompt = user_message
        if file_content:
            user_prompt += f"\n\n[User attached file content]:\n{file_content}"

        print("👉 Sending prompt to Claude...", flush=True)

        # Anthropic API Call (Sonnet 4.6)
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=system_instructions,
            messages=[{"role": "user", "content": user_prompt}]
        )

        print("✅ Received response!", flush=True)
        return jsonify({"reply": message.content[0].text})

    except Exception as e:
        print(f"🔥 ERROR: {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
