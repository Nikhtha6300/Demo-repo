#!/usr/bin/env python3
"""
Demo script for AI Restaurant App
Shows how the API works with various order examples
"""

import requests
import json
import time

def test_api_endpoint(url, data=None, method='GET'):
    """Test an API endpoint and display results"""
    try:
        if method == 'POST':
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_order_result(result):
    """Pretty print order result"""
    print(f"Status: {result.get('status', 'unknown')}")
    print(f"Message: {result.get('message', 'No message')}")
    
    if result.get('items_found'):
        print("\n✅ Items Found:")
        for item in result['items_found']:
            print(f"  - {item['name']}: ${item['price']:.2f}")
        print(f"\n💰 Total: ${result.get('total_price', 0):.2f}")
    
    if result.get('suggestions'):
        print("\n💡 Suggestions:")
        for item in result['suggestions']:
            print(f"  - {item['name']}: ${item['price']:.2f} ({item.get('description', 'No description')})")

def main():
    """Run the demo"""
    base_url = "http://localhost:5000"
    
    print("🤖 AI Restaurant Demo")
    print("Testing the AI-powered food ordering system...")
    
    # Test health check
    print_section("Health Check")
    health = test_api_endpoint(f"{base_url}/health")
    print(f"Server Status: {health.get('status', 'unknown')}")
    
    # Test menu endpoint
    print_section("Restaurant Menu")
    menu = test_api_endpoint(f"{base_url}/menu")
    if 'error' not in menu:
        for category, items in menu.items():
            print(f"\n📋 {category.replace('_', ' ').title()}:")
            for item in items:
                status = "✅ Available" if item['available'] else "❌ Not Available"
                print(f"  - {item['name']}: ${item['price']:.2f} - {status}")
    else:
        print(f"Error loading menu: {menu['error']}")
    
    # Test various order scenarios
    test_orders = [
        {
            "description": "Available Item",
            "order": "I'd like a beef burger please"
        },
        {
            "description": "Multiple Available Items", 
            "order": "Can I get salmon and a coffee?"
        },
        {
            "description": "Unavailable Item",
            "order": "I want pizza please"
        },
        {
            "description": "Mixed Available/Unavailable",
            "order": "I'd like burger and wine"
        },
        {
            "description": "Natural Language Order",
            "order": "Hi! I'm really hungry, could I please have some wings and a coke? Thanks!"
        }
    ]
    
    for i, test_case in enumerate(test_orders, 1):
        print_section(f"Order Test {i}: {test_case['description']}")
        print(f"Customer Order: \"{test_case['order']}\"")
        print("\nAI Response:")
        
        result = test_api_endpoint(
            f"{base_url}/order", 
            {"order": test_case['order']}, 
            'POST'
        )
        
        if 'error' not in result:
            print_order_result(result)
        else:
            print(f"Error: {result['error']}")
        
        time.sleep(1)  # Small delay between requests
    
    print_section("Demo Complete!")
    print("🎉 The AI Restaurant app is working!")
    print("📱 Visit http://localhost:5000 to try the web interface")
    print("💡 Tip: Add your OpenAI API key to .env for full AI functionality")

if __name__ == "__main__":
    main()