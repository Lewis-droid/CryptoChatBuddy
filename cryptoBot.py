# crypto_chatbot_ai.py
# --------------------------------
# CryptoBuddy 🤖 + Simple AI Layer
# --------------------------------

import difflib

# --- Dataset ---
crypto_db = {
    "Bitcoin": {
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3/10
    },
    "Ethereum": {
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6/10
    },
    "Cardano": {
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8/10
    }
}

# --- Simple AI Intent Detector ---
# It finds the closest matching "intent keyword"
def detect_intent(user_query):
    keywords = {
        "sustainable": ["sustainable", "eco", "green", "environment"],
        "profitable": ["profitable", "growth", "buy", "investment"],
        "trending": ["trending", "rising", "up", "popular"]
    }

    # Flatten all keywords
    all_words = [w for group in keywords.values() for w in group]
    query_words = user_query.lower().split()

    # Try fuzzy matching
    for qw in query_words:
        match = difflib.get_close_matches(qw, all_words, n=1, cutoff=0.7)
        if match:
            for intent, words in keywords.items():
                if match[0] in words:
                    return intent

    return None


# --- Chatbot Logic ---
def chatbot_response(user_query):
    intent = detect_intent(user_query)

    if intent == "sustainable":
        recommend = max(crypto_db, key=lambda x: crypto_db[x]["sustainability_score"])
        return f"{recommend} 🌱 is the most sustainable choice with a high eco-score!"

    elif intent == "profitable":
        for coin, data in crypto_db.items():
            if data["price_trend"] == "rising" and data["market_cap"] in ["high", "medium"]:
                return f"{coin} 🚀 looks great for long-term growth!"

    elif intent == "trending":
        rising_coins = [c for c, d in crypto_db.items() if d["price_trend"] == "rising"]
        return f"These cryptos are trending up 📈: {', '.join(rising_coins)}"

    else:
        return "Hmm 🤔 I couldn’t quite get that. Try asking about growth, sustainability, or trending cryptos!"


# --- Interactive Loop ---
print("Hey there! I’m CryptoBuddy 🤖. Ask me about crypto trends or sustainability!")
print("Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("CryptoBuddy: Take care! Always DYOR (Do Your Own Research) 🙌")
        break
    print("CryptoBuddy:", chatbot_response(user_input))
