import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("CLAUDE_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

# 1. 5 ಟೆಕ್ಸ್ಟ್ ಫೈಲ್‌ಗಳನ್ನು ಓದುವ ಫಂಕ್ಷನ್
def load_grammar_context():
    context = ""
    # ನೀವು ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಫೈಲ್ ಹೆಸರುಗಳು
    files = ['balamanorama.txt', 'kaumudi.txt', 'sutrartha_english.txt', 'vasu_english.txt', 'vasu_english_summary.txt']
    for file_name in files:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                context += f"\n--- {file_name} ---\n{f.read()}\n"
        else:
            print(f"⚠️ Warning: {file_name} not found in the directory.")
    return context

# ಸರ್ವರ್ ಸ್ಟಾರ್ಟ್ ಆದಾಗ ಒಮ್ಮೆ ಮಾತ್ರ ಫೈಲ್‌ಗಳನ್ನು ಲೋಡ್ ಮಾಡಿಕೊಳ್ಳುತ್ತದೆ
grammar_context = load_grammar_context()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # 2. JSON ಬದಲಿಗೆ ಫಾರ್ಮ್ ಡೇಟಾ (Form Data) ಮತ್ತು ಫೈಲ್ ಪಡೆಯುವುದು
        user_message = request.form.get("message", "")
        uploaded_file = request.files.get("file")
        
        file_content = ""
        if uploaded_file:
            # ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಫೈಲ್‌ನಿಂದ ಪಠ್ಯವನ್ನು ಓದುವುದು
            file_content = uploaded_file.read().decode('utf-8')

        if not user_message and not file_content:
            return jsonify({"error": "No message or file provided"}), 400

        # 3. Claude ಗೆ System Prompt ರಚನೆ (ನಿಮ್ಮ 5 ಫೈಲ್‌ಗಳನ್ನು ಇಲ್ಲಿ ಸೇರಿಸಲಾಗಿದೆ)
        system_instructions = (
            "You are 'Trayee AI', an expert Sanskrit chatbot specializing in computational linguistics and Pāṇinian grammar. "
            "Reply strictly in Sanskrit using Devanagari script. "
            f"Use the following classical texts as reference context to answer the user:\n{grammar_context}"
        )

        # 4. ಬಳಕೆದಾರರ ಪ್ರಾಂಪ್ಟ್ (ಮೆಸೇಜ್ + ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಫೈಲ್‌ನ ಡೇಟಾ)
        user_prompt = user_message
        if file_content:
            user_prompt += f"\n\nHere is the content of the uploaded file from the user:\n{file_content}"

        print("👉 Sending prompt to Claude...", flush=True)

        # 5. Anthropic API Call (System parameter ಬಳಸಿ)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022", # Claude ನ ಲೇಟೆಸ್ಟ್ ಮಾಡೆಲ್ ಹೆಸರು
            max_tokens=1024,
            system=system_instructions, # ಸಿಸ್ಟಮ್ ಪ್ರಾಂಪ್ಟ್ ಅನ್ನು ಪ್ರತ್ಯೇಕವಾಗಿ ಕಳುಹಿಸುವುದು ಉತ್ತಮ
            messages=[{"role": "user", "content": user_prompt}]
        )

        print("✅ Received response!", flush=True)
        return jsonify({"reply": message.content[0].text})

    except Exception as e:
        print(f"🔥 ERROR: {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
