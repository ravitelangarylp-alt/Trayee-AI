import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # ಮುಖಪುಟದಿಂದ ಬರುವ ಮನವಿಗಳಿಗೆ (Requests) ಅನುಮತಿ ನೀಡಲು

# Render ನ Environment Variables ನಿಂದ ನೇರವಾಗಿ API Key ಪಡೆಯುವುದು
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Gemini 1.5 Flash ಮಾಡೆಲ್ ಆಯ್ಕೆ (ಇದು ವೇಗವಾಗಿ ಉತ್ತರಿಸುತ್ತದೆ)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # ಸಿಸ್ಟಮ್ ಪ್ರಾಂಪ್ಟ್: ತ್ರಯೀ AI ಸಂಸ್ಕೃತದಲ್ಲಿಯೇ ಉತ್ತರಿಸುವಂತೆ ಕಟ್ಟುನಿಟ್ಟಿನ ನಿರ್ದೇಶನ
        prompt = f"You are 'Trayee AI', an expert Sanskrit chatbot. You must reply to the user's query strictly in the Sanskrit language using the Devanagari script. User Query: {user_message}"
        
        response = model.generate_content(prompt)
        
        return jsonify({"reply": response.text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # ಸರ್ವರ್ ಅನ್ನು ಪೋರ್ಟ್ 5000 ನಲ್ಲಿ ರನ್ ಮಾಡುವುದು (ನಿಮ್ಮ ಕಂಪ್ಯೂಟರ್‌ನಲ್ಲಿ ಟೆಸ್ಟ್ ಮಾಡುವಾಗ ಇದು ಬೇಕಾಗುತ್ತದೆ)
    app.run(debug=True, port=5000)
