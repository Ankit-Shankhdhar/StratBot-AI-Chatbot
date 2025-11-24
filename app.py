from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Loaded API Key:", GEMINI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# Choose model
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Create Flask app
app = Flask(__name__)

# Enable CORS for your Vercel frontend
CORS(app, resources={
    r"/chat": {
        "origins": ["https://strat-bot-ai-chatbot.vercel.app"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    # Handle preflight request
    if request.method == "OPTIONS":
        return "", 200

    # Handle POST request
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    user_input = data.get("message")
    print("User input:", user_input)

    if not user_input:
        return jsonify({"error": "No input provided."}), 400

    try:
        prompt = f"""
You are StratBot — a Game Strategy Advisor bot.

Your behavior must strictly follow these rules:

1. If the user says greetings or polite conversation like "Hello", "Hi", "How are you", "Thank you", "Bye", etc., then reply casually and politely like a friendly bot.  
2. If the user asks who made you or who created you, reply:  
   "I was built using Google's AI models, but optimized and shaped into a strategist bot by Sanchit Sharma."  
3. If the question is related to any type of gaming (board games, video games, offline, online, mobile, etc.), then give proper game strategies, tips, tricks, or support.  
4. If the question is related to physical sports performance or player improvement (e.g., "How can Ronaldo play better in the next game?"), then provide strategies or advice for improving performance.  
5. If the question is NOT related to gaming, physical sports, and NOT a greeting, then reply:  
   "I'm all about gaming strategies! For other topics, a general assistant might help you better."

User message:
{user_input}
"""

        response = model.generate_content(prompt)
        clean_text = response.text.replace("**", "")
        return jsonify({"response": clean_text})

    except Exception as e:
        print("Gemini Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use 0.0.0.0 and port 10000 for Render compatibility
    app.run(host="0.0.0.0", port=10000)
