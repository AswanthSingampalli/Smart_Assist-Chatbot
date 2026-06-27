<<<<<<< HEAD
# 💊 SmartPharmacy + Context-Aware Medical Chatbot

**SmartPharmacy** is a full-stack E-Pharmacy application containing a deeply integrated, intelligent Medical Chatbot. The backend acts as an Artificial Intelligence Pharmacist capable of mapping sophisticated conversational symptoms directly to inventory, managing customer delivery protocols, mitigating life-threatening warnings, and persisting multi-turn conversation memory contexts across operations.

## ✨ Core Features
*   **Intelligent Symptom Triage**: Employs an advanced Natural Language dictionary engine that dynamically maps user symptom phrasing (e.g. *"I have a headache", "My legs hurt"*) straight to relevant medicines in the checkout cart.
*   **Emergency Safety Override**: Strict algorithmic intercept block that catches hazardous keywords like *"chest pain"*, *"bleeding"*, or *"911"* and restricts e-commerce features, forcing the user to consult emergency services.
*   **Context Memory Handling**: The backend remembers complex states. If you ask to *track an order*, the bot will preserve your positional state (via a Flask-Session wrapper) and await your 5-digit Order ID specifically.
*   **Interactive Chat UI**: Replaces brute-force text replies with beautiful HTML-injection Buttons (Carousel Medicine display, Sub-symptom clickable lists) generated natively by Python.
*   **Full Real-Time Database Integration**: Connecting securely to **MongoDB**, the architecture can place live orders, generate randomized pharmacy delivery metrics, issue instant mock-refunds, and track shipment IDs.

## 🛠️ Tech Stack
*   **Backend:** Python 3.10+, Flask, PyMongo (NoSQL)
*   **Frontend:** Vanilla JS, HTML5, CSS3 (Medical Teal & Blue Theme)
*   **AI Engine logic:** Pattern/Substring heuristics integrated inside `ai_service.py` 

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have Python installed and a running instance of **MongoDB** (either MongoDB Compass locally or MongoDB Atlas).

### 2. Installation
Clone the repository to your desktop and navigate into it:
```bash
git clone https://github.com/Chandu2226/Smart_Assist-Chatbot.git
cd Smart_Assist-Chatbot
```

Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

pip install flask pymongo
```

### 3. Configuration
Inside `config.py`, you will need to map your Database URI and insert your API keys. 
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
```

### 4. Boot the Server
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser and try talking to the Pharmacy Assistant! 

---
*Disclaimer: This codebase is designed to emulate advanced technical NLP features inside e-commerce for educational engineering purposes. Do not replace live human medical diagnosis with this AI.*
=======
# Smart_Assist-Chatbot
SmartPharmacy is a full-stack AI-powered e-pharmacy platform featuring an intelligent medical chatbot that analyzes symptoms, recommends medicines from inventory, provides safety warnings, manages deliveries, and maintains multi-turn conversation context for personalized healthcare assistance.
>>>>>>> e0720042a6f2f162ad0e468ca76e1aa09eb54771
