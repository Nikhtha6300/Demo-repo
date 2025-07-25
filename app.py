from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI (you can also use other LLM providers)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Sample restaurant menu - in a real app, this would be in a database
RESTAURANT_MENU = {
    "appetizers": [
        {"name": "Caesar Salad", "price": 12.99, "available": True, "description": "Fresh romaine lettuce with caesar dressing"},
        {"name": "Buffalo Wings", "price": 14.99, "available": True, "description": "Spicy chicken wings with ranch dip"},
        {"name": "Mozzarella Sticks", "price": 9.99, "available": False, "description": "Crispy mozzarella with marinara sauce"}
    ],
    "main_courses": [
        {"name": "Grilled Salmon", "price": 24.99, "available": True, "description": "Atlantic salmon with herbs"},
        {"name": "Chicken Parmesan", "price": 19.99, "available": True, "description": "Breaded chicken with marinara and cheese"},
        {"name": "Beef Burger", "price": 16.99, "available": True, "description": "Angus beef with lettuce, tomato, and fries"},
        {"name": "Vegetarian Pizza", "price": 18.99, "available": False, "description": "Fresh vegetables on thin crust"},
        {"name": "Pasta Carbonara", "price": 17.99, "available": True, "description": "Creamy pasta with bacon and parmesan"}
    ],
    "desserts": [
        {"name": "Chocolate Cake", "price": 8.99, "available": True, "description": "Rich chocolate layer cake"},
        {"name": "Ice Cream Sundae", "price": 6.99, "available": True, "description": "Vanilla ice cream with toppings"},
        {"name": "Tiramisu", "price": 9.99, "available": False, "description": "Classic Italian dessert"}
    ],
    "beverages": [
        {"name": "Coca Cola", "price": 3.99, "available": True, "description": "Classic cola drink"},
        {"name": "Fresh Orange Juice", "price": 4.99, "available": True, "description": "Freshly squeezed orange juice"},
        {"name": "Coffee", "price": 2.99, "available": True, "description": "Freshly brewed coffee"},
        {"name": "Wine", "price": 8.99, "available": False, "description": "House red wine"}
    ]
}

def get_menu_items():
    """Get all menu items in a flat list"""
    items = []
    for category, item_list in RESTAURANT_MENU.items():
        for item in item_list:
            items.append({
                "category": category,
                "name": item["name"],
                "price": item["price"],
                "available": item["available"],
                "description": item["description"]
            })
    return items

def check_item_availability_with_ai(order_text):
    """Use AI to parse the order and check availability"""
    menu_items = get_menu_items()
    
    # Create a context for the AI
    menu_context = "\n".join([
        f"- {item['name']}: ${item['price']} ({'Available' if item['available'] else 'NOT AVAILABLE'}) - {item['description']}"
        for item in menu_items
    ])
    
    prompt = f"""
You are an AI assistant for a restaurant. A customer wants to order: "{order_text}"

Here is our current menu with availability:
{menu_context}

Please respond in a friendly, helpful manner. If the items are available, confirm the order and provide the total price. If any items are not available, suggest similar alternatives from the available menu items.

Format your response as a JSON object with:
- "status": "available" or "partially_available" or "unavailable"
- "message": friendly response to the customer
- "items_found": list of items that match the order
- "total_price": total price if items are available
- "suggestions": list of alternative items if some are unavailable

Be conversational and helpful!
"""

    try:
        # Use OpenAI API (you can replace this with any other LLM)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful restaurant assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Parse the AI response
        ai_response = response.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback response if JSON parsing fails
                return {
                    "status": "available",
                    "message": ai_response,
                    "items_found": [],
                    "total_price": 0,
                    "suggestions": []
                }
        except json.JSONDecodeError:
            return {
                "status": "available",
                "message": ai_response,
                "items_found": [],
                "total_price": 0,
                "suggestions": []
            }
            
    except Exception as e:
        # Fallback to simple keyword matching if AI fails
        return fallback_order_processing(order_text)

def fallback_order_processing(order_text):
    """Fallback method if AI is not available"""
    order_lower = order_text.lower()
    found_items = []
    total_price = 0
    unavailable_items = []
    
    menu_items = get_menu_items()
    
    for item in menu_items:
        if item['name'].lower() in order_lower:
            if item['available']:
                found_items.append(item)
                total_price += item['price']
            else:
                unavailable_items.append(item)
    
    if found_items and not unavailable_items:
        return {
            "status": "available",
            "message": f"Great! I found your items. Total: ${total_price:.2f}",
            "items_found": found_items,
            "total_price": total_price,
            "suggestions": []
        }
    elif found_items and unavailable_items:
        suggestions = [item for item in menu_items if item['available'] and item['category'] == unavailable_items[0]['category']][:2]
        return {
            "status": "partially_available",
            "message": f"Some items are available (${total_price:.2f}), but some are not. Here are some alternatives:",
            "items_found": found_items,
            "total_price": total_price,
            "suggestions": suggestions
        }
    else:
        suggestions = [item for item in menu_items if item['available']][:3]
        return {
            "status": "unavailable",
            "message": "Sorry, those items aren't available right now. Here are some alternatives:",
            "items_found": [],
            "total_price": 0,
            "suggestions": suggestions
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return jsonify(RESTAURANT_MENU)

@app.route('/order', methods=['POST'])
def process_order():
    data = request.get_json()
    order_text = data.get('order', '')
    
    if not order_text:
        return jsonify({'error': 'Please provide an order'}), 400
    
    # Process order with AI
    result = check_item_availability_with_ai(order_text)
    
    return jsonify(result)

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)