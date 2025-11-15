"""
Smart Meal Planner Agent - Main Application
Built with Google's Agent Development Kit (ADK) and Gemini 2.5 Flash
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=GOOGLE_API_KEY)


# Custom Tool 1: Search Recipes
def search_recipes(dietary_preference: str, num_meals: int = 7) -> dict:
    """
    Search for meal recommendations based on dietary preferences.
    
    Args:
        dietary_preference: "vegetarian", "vegan", or "gluten-free"
        num_meals: Number of meals to generate (default: 7 for weekly)
    
    Returns:
        Dictionary with meal recommendations
    """
    meals_database = {
        "vegetarian": [
            {"name": "Chickpea Curry", "calories": 450, "time": 30},
            {"name": "Paneer Tikka", "calories": 320, "time": 25},
            {"name": "Vegetable Biryani", "calories": 520, "time": 45},
            {"name": "Lentil Soup", "calories": 280, "time": 20},
            {"name": "Mushroom Risotto", "calories": 480, "time": 35},
            {"name": "Caprese Salad", "calories": 200, "time": 10},
            {"name": "Vegetable Stir Fry", "calories": 380, "time": 25},
        ],
        "vegan": [
            {"name": "Buddha Bowl", "calories": 420, "time": 25},
            {"name": "Chickpea Stew", "calories": 380, "time": 30},
            {"name": "Tofu Scramble", "calories": 300, "time": 15},
            {"name": "Lentil Pasta", "calories": 450, "time": 25},
            {"name": "Quinoa Salad", "calories": 350, "time": 20},
            {"name": "Bean Chili", "calories": 410, "time": 35},
            {"name": "Vegetable Curry", "calories": 400, "time": 30},
        ],
        "gluten-free": [
            {"name": "Rice Bowl with Vegetables", "calories": 480, "time": 25},
            {"name": "Grilled Salmon", "calories": 520, "time": 30},
            {"name": "Corn Tacos", "calories": 450, "time": 20},
            {"name": "Quinoa Bowl", "calories": 420, "time": 25},
            {"name": "Potato Salad", "calories": 380, "time": 20},
            {"name": "Grilled Chicken", "calories": 500, "time": 25},
            {"name": "Vegetable Soup", "calories": 320, "time": 30},
        ],
    }
    
    meals = meals_database.get(dietary_preference.lower(), meals_database["vegetarian"])
    return {
        "dietary_preference": dietary_preference,
        "meals": meals[:num_meals],
        "total_meals": len(meals[:num_meals])
    }


# Custom Tool 2: Calculate Nutrition
def calculate_nutrition(meal_name: str) -> dict:
    """
    Calculate nutritional information for a meal.
    
    Args:
        meal_name: Name of the meal
    
    Returns:
        Dictionary with nutritional information
    """
    nutrition_db = {
        "chickpea curry": {"calories": 450, "protein": 18, "carbs": 55, "fat": 12},
        "buddha bowl": {"calories": 420, "protein": 16, "carbs": 52, "fat": 14},
        "tofu scramble": {"calories": 300, "protein": 20, "carbs": 25, "fat": 10},
        "grilled salmon": {"calories": 520, "protein": 45, "carbs": 0, "fat": 38},
        "vegetable stir fry": {"calories": 380, "protein": 12, "carbs": 45, "fat": 15},
    }
    
    nutrition = nutrition_db.get(meal_name.lower(), 
                                 {"calories": 400, "protein": 15, "carbs": 50, "fat": 12})
    return {
        "meal": meal_name,
        "nutrition": nutrition
    }


# Custom Tool 3: Get Grocery Items
def get_grocery_items(meals: list) -> dict:
    """
    Generate grocery list from meals.
    
    Args:
        meals: List of meal names
    
    Returns:
        Dictionary with grocery items
    """
    grocery_db = {
        "chickpea curry": ["Chickpeas", "Onion", "Tomato", "Ginger", "Garlic", "Coconut Milk"],
        "buddha bowl": ["Quinoa", "Chickpeas", "Spinach", "Bell Pepper", "Carrot"],
        "tofu scramble": ["Tofu", "Turmeric", "Kale", "Tomato", "Nutritional Yeast"],
        "grilled salmon": ["Salmon", "Lemon", "Olive Oil", "Herbs"],
        "vegetable stir fry": ["Broccoli", "Carrot", "Soy Sauce", "Ginger", "Garlic"],
    }
    
    items = set()
    for meal in meals:
        items.update(grocery_db.get(meal.lower(), ["Generic Ingredients"]))
    
    return {
        "meals": meals,
        "grocery_items": sorted(list(items))
    }


def main():
    """Main application loop for the Meal Planner Agent."""
    print("=" * 60)
    print("🍽️  Welcome to the Smart Meal Planner Agent!")
    print("=" * 60)
    print("\nPowered by Google Gemini 2.5 Flash")
    print("\nCommands:")
    print("  - 'vegetarian' - Get vegetarian meal plans")
    print("  - 'vegan' - Get vegan meal plans")
    print("  - 'gluten-free' - Get gluten-free meal plans")
    print("  - 'nutrition [meal]' - Get nutrition info")
    print("  - 'quit' - Exit the program")
    print("-" * 60)
    
    conversation_history = []
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        while True:
            user_input = input("\n🧑 You: ").strip()
            
            if user_input.lower() == "quit":
                print("\n👋 Thank you for using Meal Planner Agent!")
                break
            
            if not user_input:
                continue
            
            # Add user message to history
            conversation_history.append({"role": "user", "content": user_input})
            
            # Process different commands
            if "vegetarian" in user_input.lower():
                meals_data = search_recipes("vegetarian")
                context = f"Here's a personalized vegetarian meal plan:\n{meals_data}"
            elif "vegan" in user_input.lower():
                meals_data = search_recipes("vegan")
                context = f"Here's a personalized vegan meal plan:\n{meals_data}"
            elif "gluten" in user_input.lower():
                meals_data = search_recipes("gluten-free")
                context = f"Here's a personalized gluten-free meal plan:\n{meals_data}"
            elif "nutrition" in user_input.lower():
                meal = user_input.replace("nutrition", "").strip()
                nutrition_data = calculate_nutrition(meal)
                context = f"Nutritional information: {nutrition_data}"
            else:
                context = ""
            
            # Prepare messages for API
            messages = []
            for msg in conversation_history:
                messages.append(types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(msg["content"])]
                ))
            
            # Add context if available
            if context:
                system_prompt = f"""You are a helpful meal planning assistant. 
                {context}
                
                Provide personalized meal recommendations considering dietary preferences, 
                nutritional value, and cooking time. Be friendly and helpful."""
            else:
                system_prompt = """You are a helpful meal planning assistant. 
                Help users create personalized meal plans based on their dietary preferences.
                Provide nutritional information and shopping lists."""
            
            # Call Gemini API
            response = model.generate_content(
                contents=messages,
                system_instruction=system_prompt,
                generation_config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                ),
            )
            
            assistant_message = response.text
            conversation_history.append({"role": "assistant", "content": assistant_message})
            
            print(f"\n🤖 Assistant: {assistant_message}")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure your GOOGLE_API_KEY is set in .env file")


if __name__ == "__main__":
    main()
