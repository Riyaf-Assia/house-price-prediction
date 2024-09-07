from flask import Flask, request, jsonify
import util_test

app = Flask(__name__) # creating the flask application

@app.route('/hello')
def hello():
    return "Hello"

@app.route('/get_ocean_prox')
def get_ocean_prox():
    response = jsonify({
        'prox': util_test.get_ocean_proximity()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_house_price', methods=['POST'])
def predict_house_price():
    # Use form data from request.form
    longitude = float(request.form['longitude'])
    latitude = float(request.form['latitude'])
    housing_median_age = float(request.form['housing_median_age'])
    total_rooms = int(request.form['total_rooms'])
    total_bedrooms = int(request.form['total_bedrooms'])
    households = int(request.form['households'])
    median_income = float(request.form['median_income'])
    population = float(request.form['population'])
    ocean_proximity = request.form['ocean_proximity']

    # Call util_test's prediction function
    predicted_price = util_test.predict_house_price(
        longitude, latitude, housing_median_age, total_rooms,
        total_bedrooms, households, median_income, population, ocean_proximity
    )

    response = jsonify({
        'price': predicted_price
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Flask Server For Home Price Prediction ...")
    app.run(debug=True)
