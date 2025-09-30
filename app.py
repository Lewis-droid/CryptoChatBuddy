from flask import Flask, render_template, request, jsonify
import difflib
import random

app = Flask(__name__)

# -------------------------
# Crypto Dataset
# -------------------------
crypto_db = {
    "Bitcoin": {"price_trend": "rising", "market_cap": "high", "energy_use": "high", "sustainability_score": 3/10},
    "Ethereum": {"price_trend": "stable", "market_cap": "high", "energy_use": "medium", "sustainability_score": 6/10},
    "Cardano": {"price_trend": "rising", "market_cap": "medium", "energy_use": "low", "sustainability_score": 8/10}
}

# -------------------------
# Memory for fallback learning
# -------------------------
learned_responses = {}  # e.g., {"keyword": "response"}

# -------------------------
# Simple AI Intent Detection
# -------------------------
def detect_intent(user_query):
    keywords = {
        "sustainable": ["sustainable", "eco", "green", "environment"],
        "profitable": ["profitable", "growth", "buy", "investment"],
        "trending": ["trending", "rising", "up", "popular"],
        "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "greetings"],
        "farewell": ["bye", "goodbye", "see you", "later", "farewell"],
        "thanks": ["thanks", "thank you", "thx"],
        "howareyou": ["how are you", "how's it going", "how are you doing"]
    }

    all_words = [w for group in keywords.values() for w in group]
    query_words = user_query.lower().split()

    # Match single-word keywords
    for qw in query_words:
        match = difflib.get_close_matches(qw, all_words, n=1, cutoff=0.7)
        if match:
            for intent, words in keywords.items():
                if match[0] in words:
                    return intent

    # Check multi-word phrases
    if "how are you" in user_query.lower() or "how's it going" in user_query.lower():
        return "howareyou"

    return None

# -------------------------
# Chatbot Response Logic
# -------------------------
def chatbot_response(user_query):
    intent = detect_intent(user_query)

    # Greetings
    if intent == "greeting":
        return random.choice([
            "Hello! 🤖 How can I help you with crypto today?",
            "Hi there! Ready to explore some coins? 🚀",
            "Hey! Want me to check trending or sustainable cryptos? 🌱"
        ])

    # Farewell
    elif intent == "farewell":
        return random.choice([
            "Goodbye! 👋 Stay safe and happy investing!",
            "See you later! Remember, always DYOR! 🙌",
            "Bye! CryptoBuddy signing off 🪙"
        ])

    # Thanks
    elif intent == "thanks":
        return random.choice([
            "You're welcome! 😊",
            "No problem! Glad I could help! 👍",
            "Anytime! Happy to assist! 🤖"
        ])

    # How are you
    elif intent == "howareyou":
        return random.choice([
            "I'm doing great! Ready to help with crypto 🚀",
            "All good here! How about your portfolio? 💰",
            "Feeling bullish today! 😎"
        ])

    # Sustainability
    elif intent == "sustainable":
        recommend = max(crypto_db, key=lambda x: crypto_db[x]["sustainability_score"])
        return f"{recommend} 🌱 is the most sustainable choice with a high eco-score!"

    # Profitability
    elif intent == "profitable":
        for coin, data in crypto_db.items():
            if data["price_trend"] == "rising" and data["market_cap"] in ["high", "medium"]:
                return f"{coin} 🚀 looks great for long-term growth!"

    # Trending
    elif intent == "trending":
        rising_coins = [c for c, d in crypto_db.items() if d["price_trend"] == "rising"]
        return f"These cryptos are trending up 📈: {', '.join(rising_coins)}"

    # Check learned responses
    for keyword, response in learned_responses.items():
        if keyword in user_query.lower():
            return response

    # Fallback: learn this query
    fallback_response = "Hmm 🤔 I don’t have an answer for that yet. Can you teach me what to say?"
    # Save keyword for next time (simple first word approach)
    first_word = user_query.lower().split()[0]
    learned_responses[first_word] = "Thanks for teaching me! I will remember this for next time."
    return fallback_response

# -------------------------
# Routes
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_msg = request.form["message"]
    bot_reply = chatbot_response(user_msg)
    return jsonify({"reply": bot_reply})

# -------------------------
# Run Flask
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
