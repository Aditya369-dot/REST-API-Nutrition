from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load data once to avoid reloading
df = pd.read_csv('pred_food.csv')
df['Food Name'] = df['Food Name'].str.lower()  # make food name case-insensitive

# Sample diet plans for each diet type
sample_diets = {
    "slowcarb": "Sample Slow Carb Diet: Breakfast - Eggs and vegetables. Lunch - Chicken salad. Dinner - Beef and spinach.",
    "keto": "Sample Keto Diet: Breakfast - Keto porridge. Lunch - Salmon with asparagus. Dinner - Cauliflower rice with beef curry.",
    "diabeticfriendly": "Sample Diabetic-Friendly Diet: Breakfast - Oatmeal with berries. Lunch - Quinoa salad with nuts. Dinner - Grilled chicken with mixed vegetables.",
    "paleo": "Sample Paleo Diet: Breakfast - Banana pancakes. Lunch - Avocado chicken salad. Dinner - Grilled salmon with broccoli.",
    "balanced": "Sample Balanced Diet: Breakfast - Greek yogurt with granola. Lunch - Turkey and avocado wrap. Dinner - Baked cod with sweet potato.",
    "suitableforbloodpressure": "Sample Diet for Blood Pressure: Breakfast - Oatmeal with sliced bananas. Lunch - Baked tilapia with kale salad. Dinner - Stir-fried tofu with vegetables.",
    "dash": "Sample DASH Diet: Breakfast - Whole grain cereal with milk. Lunch - Grilled chicken sandwich with side salad. Dinner - Baked salmon with brown rice and steamed spinach."
}

@app.route("/nutrition/<foodname>", methods=['GET'])
def get_nutrition(foodname):
    """Function to provide nutritional info for a specific food name."""
    foodname = foodname.lower()
    filtered_df = df[df['Food Name'] == foodname]

    if filtered_df.empty:
        return jsonify({"error": "Food not found"}), 404

    nutritional_info = filtered_df.drop(columns=["Food Name"]).to_dict(orient='records')[0]
    return jsonify(nutritional_info)

@app.route("/nutrition/", methods=['GET'])
def get_filtered_nutrition():
    diet = request.args.get('diet', '').lower()

    # Ensure filtered_df is defined here to include diet filtering logic
    # Example filtering logic (you need to adapt this based on your actual data and requirements)
    if diet in sample_diets:
        # Sample filtering logic, replace with actual conditions
        if diet == "keto":
            filtered_df = df[df['Fat'] > 15]
        else:
            filtered_df = pd.DataFrame()  # Replace with actual filtering for other diets

        if not filtered_df.empty:
            nutritional_info = filtered_df.drop(columns=["Food Name"]).to_dict(orient='records')
            return jsonify({"Diet Plan": sample_diets[diet], "Foods": nutritional_info})
        else:
            return jsonify({"error": "No foods match this dietary preference"}), 404
    else:
        return jsonify({"error": "Invalid or no diet specified"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)
