from flask import Flask, request, jsonify, render_template
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

model = genai.GenerativeModel("models/gemini-2.5-flash")

# Flask app
app = Flask(__name__)

# ======================================================
# ✅ Enable CORS for your Vercel frontend
# ======================================================
CORS(app, resources={
    r"/*": {
        "origins": ["https://strat-bot-ai-chatbot.vercel.app"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


# ======================================================
# ROUTES
# ======================================================

@app.route("/")
def index():
    return "Backend Running Successfully!"


# ======================================================
# CHAT ROUTE WITH OPTIONS SUPPORT
# ======================================================
@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    # ---- preflight request ----
    if request.method == "OPTIONS":
        return "", 200

    # ---- POST request ----
    data = request.get_json()
    user_input = data.get("message")

    print("User input:", user_input)

    if not user_input:
        return jsonify({"error": "No input provided."}), 400

    try:
        prompt = f"""
You are StratBot — a Game Strategy Advisor bot.

Rules:
1. If user greets: reply casually & politely.
2. If user asks 'who made you', answer:
   "I was built using Google's AI models, but optimized and shaped into a strategist bot by Sanchit Sharma."
3. If topic is gaming → provide strategies.
4. If topic is physical sports → provide performance advice.
5. If topic is unrelated → reply:
   "I'm all about gaming strategies! For other topics, a general assistant might help you better."

User message:
{user_input}
"""

        # Generate response
        response = model.generate_content(prompt)

        # Clean markdown symbols
        clean_text = response.text.replace("**",**_
