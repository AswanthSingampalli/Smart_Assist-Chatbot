import random
import datetime
from services.db_service import orders_col

AGENTS = ["Alex (FedEx Pharma)", "Sarah (Priority Health)", "Mike (Local Pharmacy Driver)"]

KNOWN_DISEASES = {
    # Supported symptoms mapping directly to the 8 products
    "headache": "Paracetamol 500mg",
    "fever": "Paracetamol 500mg",
    "pain": "Ibuprofen 400mg",
    "muscle": "Ibuprofen 400mg",
    "inflammation": "Ibuprofen 400mg",
    "legs pain": "Ibuprofen 400mg",
    "leg pain": "Ibuprofen 400mg",
    "body ache": "Ibuprofen 400mg",
    "scurvy": "Vitamin C Complex",
    "cold": "Vitamin C Complex",
    "immune": "Vitamin C Complex",
    "injury": "Premium First Aid Kit",
    "cut": "Premium First Aid Kit",
    "allergy": "Allergy Relief",
    "allergies": "Allergy Relief",
    "sneezing": "Allergy Relief",
    "insomnia": "Melatonin Gummies",
    "sleep": "Melatonin Gummies",
    "temperature": "Digital Thermometer",
    "cough": "Cough Syrup",
    "cold and cough": "Cough Syrup",
    "congestion": "Cough Syrup",
    
    # Unsupported serious diseases / symptoms (Not in cart)
    "stomach pain": None,
    "stomach": None,
    "chest pain": None,
    "eyes pain": None,
    "eye pain": None,
    "digestion problem": None,
    "digestion": None,
    "skin care": None,
    "acne": None,
    "diabetes": None,
    "cancer": None,
    "flu": None,
    "asthma": None,
    "malaria": None,
    "covid": None,
    "infection": None,
    "hypertension": None,
    "blood pressure": None,
    "heart attack": None,
    "stroke": None,
    "depression": None,
    "anxiety": None,
    "rabies": None,
    "dengue": None
}

def generate_ai_response(message, context):
    message_clean = message.lower()

    if "intent" not in context:
        context["intent"] = None

    # Handle placing an order directly (triggered via JS or text)
    if message_clean.startswith("buy ") or message_clean.startswith("order "):
        product_name = message_clean.replace("buy ", "").replace("order ", "").strip().title()
        
        # Prevent generic words from instantly generating a fake order
        if product_name.lower() in ["medicine", "medicines", "drugs", "pills", "something", ""]:
            # Fall back to asking what product they want or rendering a catalog!
            pass # Continues down to the other handlers
        else:
            order_id = str(random.randint(10000, 99999))
            
            # Varied mock data
            days_to_add = random.randint(1, 3) # Pharmacies deliver fast!
            del_date = (datetime.datetime.now() + datetime.timedelta(days=days_to_add)).strftime("%A, %B %d")
            mock_statuses = ["Packing at Pharmacy", "Out for Delivery", "Shipped"]
            assigned_status = random.choice(mock_statuses)
            
            # New Tracking Metadata
            shipment_id = f"RX-{random.randint(100000, 999999)}"
            agent = random.choice(AGENTS)
            
            # PUSH TO MONGODB
            orders_col.insert_one({
                "_id": order_id,
                "product": product_name,
                "status": assigned_status,
                "delivery_date": del_date,
                "price": f"${random.randint(5, 50)}.00",
                "shipment_id": shipment_id,
                "delivery_agent": agent,
                "tracking_url": f"https://track.smartpharmacy.local/shipment/{shipment_id}"
            })
            
            context["intent"] = None
            return f"💊 Success! Your order for <b>{product_name}</b> has been placed! Your Order ID is: <b>{order_id}</b>.<br><br>Fast delivery is guaranteed. Type 'track delivery' to see live status updates!"

    # ===============================================
    # EMERGENCY SYSTEM OVERRIDE
    # ===============================================
    if any(word in message_clean for word in ["chest", "emergency", "bleeding", "911", "hospital"]):
        return "🚨 <b>WARNING:</b> If you are experiencing a severe medical emergency, do not wait for an online delivery. Please dial 911 immediately or go to the nearest hospital."

    # ===============================================
    # INTELLIGENT DISEASE & SYMPTOM ENGINE
    # ===============================================
    found_disease = None
    # Use sorting by string length to ensure `stomach pain` matches before `pain`
    for disease in sorted(KNOWN_DISEASES.keys(), key=len, reverse=True):
        if disease in message_clean:
            found_disease = disease
            break
            
    if found_disease:
        medicine = KNOWN_DISEASES[found_disease]
        if medicine:
            # We HAVE the medicine in the cart!
            return f"""Based on your symptoms of <b>{found_disease}</b>, I highly recommend our <b>{medicine}</b> from our pharmacy catalog.<br><br>
            It is fast-acting and highly effective. Would you like to buy it right now?<br><br>
            <button class="quick-reply-btn" onclick="sendQuickReply('buy {medicine}')" style="background:#0077b6; color:white;">Order {medicine}</button>"""
        else:
            # We DON'T have the medicine for this serious disease.
            return f"I am very sorry, but we currently do not sell over-the-counter medicine for <b>{found_disease}</b> in our online pharmacy. 🩺 For chronic or serious conditions, please consult your primary care doctor right away."
            
    if "disease" in message_clean or "sick" in message_clean or "ill" in message_clean or "symptom" in message_clean:
        return """Please select the symptom you are experiencing from the list below, or type it out manually:
        <div class="quick-replies" style="margin-top: 10px;">
            <button class="quick-reply-btn" onclick="sendQuickReply('fever')">Fever</button>
            <button class="quick-reply-btn" onclick="sendQuickReply('headache')">Headache</button>
            <button class="quick-reply-btn" onclick="sendQuickReply('legs pain')">Legs Pain</button>
            <button class="quick-reply-btn" onclick="sendQuickReply('cold and cough')">Cold & Cough</button>
            <button class="quick-reply-btn" onclick="sendQuickReply('stomach pain')">Stomach Pain</button>
            <button class="quick-reply-btn" onclick="sendQuickReply('skin care')">Skin Issues</button>
            <button class="quick-reply-btn" onclick="sendQuickReply('eyes pain')">Eye Pain</button>
        </div>
        """
        
    if "medicine" in message_clean and not message_clean.startswith("wrong"):
        return "You can buy medicines by checking our homepage grid, or just tell me your symptoms directly (e.g. 'I have a headache') and I will prescribe the best medicine we have!"

    # ===============================================
    # CUSTOMER ISSUES / PHARMACY OPERATIONS
    # ===============================================
    if any(word in message_clean for word in ["damaged", "broken", "expired", "wrong", "defective", "missing"]):
        return "I am incredibly sorry that you received a damaged or incorrect medicine package! 🩺 Safety is our top priority. Please provide your 5-digit Order ID so I can instantly issue an emergency replacement or refund."
    
    if any(word in message_clean for word in ["address", "change destination", "wrong location", "move"]):
        return "Because medicine delivery vehicles are dispatched rapidly, we can only update your shipping address locally if the status is still 'Packing'. Please provide your 5-digit Order ID so I can check!"

    if any(word in message_clean for word in ["prescription", "doctor", "script", "rx", "upload"]):
        return "I can definitely help fill your prescription! Please log in to your account and upload a clear photo of your Doctor's Rx note. Our licensed pharmacists will verify it and dispatch your medicine within 2 hours."
        
    if any(word in message_clean for word in ["pharmacist", "human", "talk", "call", "agent", "someone", "person"]):
        return "Would you like to speak directly with one of our licensed pharmacists? You can call us toll-free 24/7 at <b>1-800-SMART-RX</b>, or type 'connect me' to start a live text chat."
        
    if any(word in message_clean for word in ["side effect", "side", "effect", "dosage", "how to", "safe", "pill amount"]):
        return "Before taking any new medicine, please refer to the printed label for exact dosage instructions and potential side effects. Assisting via AI cannot replace medical advice! If you are taking other medications, always consult a Doctor first."
        
    if any(word in message_clean for word in ["refill", "subscribe", "monthly", "autorefill", "recurring"]):
        return "Never run out of your essential medicines again! We offer an exclusive <b>Smart Auto-Refill</b> program. Subscribe to any medicine and receive 10% off plus automatic monthly shipping direct to your door."
        
    if any(word in message_clean for word in ["shipping", "cost", "fee", "how fast", "delivery", "hours", "open"]):
        # Don't trigger shipping cost if they just said "track delivery" (handled below)
        if "track" not in message_clean and "where" not in message_clean:
            return "Our online pharmacy dispatch operates 24/7! 🚚 Standard Delivery is absolutely <b>FREE</b> for all orders over $10.00 and usually arrives in 1-3 business days. Overnight emergency shipping is available for $4.99."

    # Refund / Cancel Intent
    if "refund" in message_clean or "cancel" in message_clean:
        context["intent"] = "refund_order"
        return "I can certainly process a cancellation or refund for you. Please provide your 5-digit order ID."

    # Order tracking intent
    if "order" in message_clean or "track" in message_clean or "delivery" in message_clean:
        context["intent"] = "order_tracking"
        return "Sure! Please provide your 5-digit delivery Order ID to track your medicine."

    # Handle order ID input for TRACKING
    if context.get("intent") == "order_tracking":
        if message_clean.isdigit():
            order_id = message_clean
            
            # PULL LIVE FROM MONGODB!
            order = orders_col.find_one({"_id": order_id})
            
            if order:
                product = order.get("product", "Unknown Medicine")
                status = order.get("status", "Packing at Pharmacy")
                delivery_date = order.get("delivery_date", "soon")
                
                # Fetch tracking details
                shipment_id = order.get("shipment_id", "Pending")
                agent = order.get("delivery_agent", "Assigning Driver...")
                tracking_url = order.get("tracking_url", "#")
                
                context["intent"] = None
                
                if "Shipped" in status or "Out for Delivery" in status:
                    return f"""🚚 <b>On its way!</b> Your {product} (Order #{order_id}) has left the pharmacy.<br><br>
                    <b>Status:</b> {status}<br>
                    <b>Estimated Arrival:</b> {delivery_date}<br>
                    <b>Delivery Driver:</b> {agent}<br>
                    <b>Tracking ID:</b> {shipment_id}<br><br>
                    👉 <a href='{tracking_url}' target='_blank' style='color:#0077b6; font-weight:600; text-decoration:none;'>Click here for the Live Driver Map</a>"""
                elif "Refunded" in status:
                    return f"💸 <b>Cancelled.</b> That order for {product} was cancelled and the refund was processed fully."
                else:
                    return f"🏥 <b>Packing:</b> The pharmacist is preparing your {product} right now! It will be handed to a driver soon. Estimated Arrival: <b>{delivery_date}</b>."
            else:
                return f"Hmm, I couldn't find delivery {order_id} in our pharmacy database. Are you sure that's correct?"

    # Handle order ID input for REFUND
    if context.get("intent") == "refund_order":
        if message_clean.isdigit():
            order_id = message_clean
            order = orders_col.find_one({"_id": order_id})
            
            if order:
                orders_col.update_one({"_id": order_id}, {"$set": {"status": "Refunded"}})
                product = order["product"]
                context["intent"] = None
                return f"💰 Successfully initiated a full refund for your <b>{product}</b> (Order {order_id}). It will appear in your bank account in 3-5 days."
            else:
                return f"Hmm, I couldn't find order {order_id} to cancel. Are you sure that's correct?"

    # Greeting
    if any(word in message_clean for word in ["hi", "hello", "hey"]):
        return "Hi there! 👋 I'm your SmartPharmacy Assistant.<br><br>Try telling me your symptoms, asking for <b>vitamins</b>, or ask me to <b>track your medicine delivery</b>."

    return "I am your Pharmacy Assistant. I can help you find medicines for your symptoms, track a delivery, or process a refund!"