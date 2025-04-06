from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import io
import csv

app = Flask(__name__)

# --- Placeholder Data Loading ---
FOOD_DATA = pd.read_csv('data/food_data.csv')
WORKOUT_DATA = pd.read_csv('data/workout_data.csv')

# --- Placeholder API Functions (Simulating API calls) ---
def fetch_food_data(query):
    """Simulates fetching food data from an API."""
    filtered_data = FOOD_DATA[FOOD_DATA['food_name'].str.contains(query, case=False)]
    return filtered_data.to_dict('records')

def fetch_workout_data(query):
    """Simulates fetching workout data from an API."""
    filtered_data = WORKOUT_DATA[WORKOUT_DATA['workout_name'].str.contains(query, case=False)]
    return filtered_data.to_dict('records')

# --- Helper Functions for Calculations ---
def calculate_food_calories(food_item, measure, quantity):
    """Calculates approximate calories and macros for a food item."""
    food_record = FOOD_DATA[FOOD_DATA['food_name'] == food_item].iloc[0] # Assuming exact match for simplicity
    calories_per_unit = food_record['calories_per_100g']
    protein_per_unit = food_record['protein_per_100g']
    carbs_per_unit = food_record['carbs_per_100g']
    fat_per_unit = food_record['fat_per_100g']

    if measure == 'grams':
        weight_grams = quantity
    elif measure == 'ml': # Assuming 1ml = 1g for simplicity for liquid foods, needs better handling in real app
        weight_grams = quantity
    elif measure == 'tablespoon': # Approximate tablespoon to grams, needs better handling
        weight_grams = quantity * 15
    elif measure == 'cup': # Approximate cup to grams, needs better handling
        weight_grams = quantity * 200

    calories = (calories_per_unit / 100) * weight_grams
    protein = (protein_per_unit / 100) * weight_grams
    carbs = (carbs_per_unit / 100) * weight_grams
    fat = (fat_per_unit / 100) * weight_grams

    return {
        'calories': round(calories, 2),
        'protein': round(protein, 2),
        'carbs': round(carbs, 2),
        'fat': round(fat, 2)
    }

def calculate_workout_calories(workout_item, sets, reps):
    """Calculates approximate calories burned for a workout."""
    workout_record = WORKOUT_DATA[WORKOUT_DATA['workout_name'] == workout_item].iloc[0] # Assuming exact match
    calories_per_rep = workout_record['calories_per_rep']
    total_calories_burned = calories_per_rep * sets * reps
    return round(total_calories_burned, 2)


# --- Flask Routes ---
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/food_tracker", methods=['GET', 'POST'])
def food_tracker():
    if request.method == 'POST':
        food_item = request.form['food_item']
        measure = request.form['measure']
        quantity = float(request.form['quantity'])
        calculation = calculate_food_calories(food_item, measure, quantity)
        return render_template('food_tracker.html', calculation=calculation, food_item=food_item, measure=measure, quantity=quantity)
    return render_template('food_tracker.html', calculation=None)

@app.route("/workout_tracker", methods=['GET', 'POST'])
def workout_tracker():
    if request.method == 'POST':
        workout_item = request.form['workout_item']
        sets = int(request.form['sets'])
        reps = int(request.form['reps'])
        calories_burned = calculate_workout_calories(workout_item, sets, reps)
        return render_template('workout_tracker.html', calories_burned=calories_burned, workout_item=workout_item, sets=sets, reps=reps)
    return render_template('workout_tracker.html', calories_burned=None)

@app.route('/download_csv/food', methods=['POST'])
def download_food_csv():
    calculation_data = request.form.to_dict() # Get the calculation data from the form
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Food Item', 'Measure', 'Quantity', 'Calories', 'Protein', 'Carbs', 'Fat']) # Header
    writer.writerow([calculation_data.get('food_item', ''), calculation_data.get('measure', ''), calculation_data.get('quantity', ''),
                     calculation_data.get('calories', ''), calculation_data.get('protein', ''), calculation_data.get('carbs', ''), calculation_data.get('fat', '')])

    csv_file = output.getvalue()
    return send_file(io.BytesIO(csv_file.encode('utf-8')),
                     mimetype='text/csv',
                     download_name='food_calculation.csv',
                     as_attachment=True)

@app.route('/download_csv/workout', methods=['POST'])
def download_workout_csv():
    calculation_data = request.form.to_dict() # Get the calculation data from the form
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Workout Item', 'Sets', 'Reps', 'Calories Burned']) # Header
    writer.writerow([calculation_data.get('workout_item', ''), calculation_data.get('sets', ''), calculation_data.get('reps', ''), calculation_data.get('calories_burned', '')])

    csv_file = output.getvalue()
    return send_file(io.BytesIO(csv_file.encode('utf-8')),
                     mimetype='text/csv',
                     download_name='workout_calculation.csv',
                     as_attachment=True)


@app.route('/autocomplete/food')
def autocomplete_food():
    query = request.args.get('term')
    food_suggestions = fetch_food_data(query) # Use placeholder API
    return jsonify(food_suggestions)

@app.route('/autocomplete/workout')
def autocomplete_workout():
    query = request.args.get('term')
    workout_suggestions = fetch_workout_data(query) # Use placeholder API
    return jsonify(workout_suggestions)

# --- New Routes for About and Contact ---
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)