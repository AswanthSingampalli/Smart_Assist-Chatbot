from flask import Flask, request, jsonify, render_template

from services.session_service import get_session
from services.translation_service import translate_to_english, translate_to_original
from services.sentiment_service import get_sentiment
from services.ai_service import generate_ai_response
from services.db_service import save_chat
from utils.helpers import format_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# --- E-Commerce Regular APIs ---

@app.route("/api/products", methods=["GET"])
def get_products():
    from services.db_service import products_col
    # Mock return if collection is empty
    return jsonify([
        {"id": "1", "name": "Silk green dress", "price": 79.90},
        {"id": "2", "name": "Flower pattern dress", "price": 80.00}
    ])

@app.route("/api/orders", methods=["POST"])
def api_place_order():
    from services.db_service import orders_col
    data = request.json
    order_id = str(data.get("order_id", "9999"))
    orders_col.insert_one({"_id": order_id, "product": "Custom App Order", "status": "Processing"})
    return jsonify({"success": True, "order_id": order_id})

# --- Support Chatbot API ---

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data["user_id"]
    message = data["message"]

    # Translate input
    translated_text, lang = translate_to_english(message)

    # Get session
    session = get_session(user_id)

    # Sentiment
    sentiment = get_sentiment(translated_text)

    # AI response
    response = generate_ai_response(translated_text, session)

    # Format response
    response = format_response(response, sentiment)

    # Translate back
    final_response = translate_to_original(response, lang)

    # Save chat
    save_chat(user_id, message, final_response, sentiment)

    return jsonify({"response": final_response})

if __name__ == "__main__":
    app.run(debug=True)