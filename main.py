from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open("data/food_data.json") as f:
    FOOD_DATA = json.load(f)

with open("data/workout_data.json") as f:
    WORKOUT_DATA = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/food-tracker", methods=["GET", "POST"])
def food_tracker():
    result = None
    if request.method == "POST":
        food_name = request.form["food_name"].lower()
        quantity = float(request.form["quantity"])
        unit = request.form["unit"]

        food_item = next((item for item in FOOD_DATA if food_name in item["name"].lower()), None)
        if food_item and unit in food_item["units"]:
            factor = food_item["units"][unit]
            result = {
                "calories": round(food_item["calories"] * factor * quantity, 2),
                "protein": round(food_item["protein"] * factor * quantity, 2),
                "carbs": round(food_item["carbs"] * factor * quantity, 2),
                "fat": round(food_item["fat"] * factor * quantity, 2),
            }
    return render_template("food_tracker.html", result=result)

@app.route("/workout-tracker", methods=["GET", "POST"])
def workout_tracker():
    result = None
    if request.method == "POST":
        workout_name = request.form["workout_name"].lower()
        reps = int(request.form["reps"])
        sets = int(request.form["sets"])

        workout = next((w for w in WORKOUT_DATA if workout_name in w["name"].lower()), None)
        if workout:
            calories = workout["calories_per_set"] * sets
            result = round(calories, 2)

    return render_template("workout_tracker.html", result=result)

@app.route("/autocomplete/food")
def autocomplete_food():
    query = request.args.get("q", "").lower()
    suggestions = [f["name"] for f in FOOD_DATA if query in f["name"].lower()]
    return jsonify(suggestions[:10])

@app.route("/autocomplete/workout")
def autocomplete_workout():
    query = request.args.get("q", "").lower()
    suggestions = [w["name"] for w in WORKOUT_DATA if query in w["name"].lower()]
    return jsonify(suggestions[:10])

if __name__ == "__main__":
    app.run(debug=True)
