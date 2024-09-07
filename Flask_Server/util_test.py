import json
import pickle
import numpy as np
from sklearn.decomposition import PCA

__ocean_prox = None
__data_cols = None
__model = None

def predict_house_price(longitude, latitude, housing_median_age, total_rooms, total_bedrooms, households, median_income, population, ocean_proximity):
    # Convert inputs to numpy arrays
    longitude = np.array(longitude)
    latitude = np.array(latitude)
    housing_median_age = np.array(housing_median_age)
    total_rooms = np.array(total_rooms)
    total_bedrooms = np.array(total_bedrooms)
    households = np.array(households)
    median_income = np.array(median_income)
    population = np.array(population)
    #ocean_proximity = np.array(ocean_proximity) error !
    ocean_proximity = np.array([ocean_proximity]) if isinstance(ocean_proximity, str) else np.array(ocean_proximity)
    # convert to a list then numpy aray if it is a string else directly a np array


    # Feature engineering
    roomsPerHousehold = total_rooms / households
    bedroomsPerHousehold = total_bedrooms / households
    populationPerHousehold = population / households

    # Log transformations
    total_rooms_log = np.log1p(total_rooms)
    total_bedrooms_log = np.log1p(total_bedrooms)
    population_log = np.log1p(population)
    households_log = np.log1p(households)
    median_income_log = np.log1p(median_income)
    population_per_household_log = np.log1p(populationPerHousehold)

    # Standardization
    features_dict = {
        'longitude': (longitude, np.float64(-119.57098639122775), np.float64(2.0036833619831143)),
        'latitude': (latitude, np.float64(35.633778147640484), np.float64(2.136260129990799)),
        'housing_median_age': (housing_median_age, np.float64(28.629723908361072), np.float64(12.589847902173602)),
        'rooms_per_household': (roomsPerHousehold, np.float64(5.4312888106655235), np.float64(2.4831272299642775)),
        'bedrooms_per_household': (bedroomsPerHousehold, np.float64(1.0969583762175268), np.float64(0.4760945712837238)),
        'households_log': (households_log, np.float64(5.984643026150241), np.float64(0.7268715736185464)),
        'median_income_log': (median_income_log, np.float64(1.5171689099889567), np.float64(0.3586639550804106)),
        'population_per_household_log': (population_per_household_log, np.float64(1.3515286144153444), np.float64(0.2078129719598193))
    }

    std_features = [(feature - mean) / std for feature, mean, std in features_dict.values()]

    # One-hot encoding for ocean proximity
    ocean_mapping = {
        'INLAND': [1, 0, 0],
        'NEAR OCEAN': [0, 0, 1],
        'NEAR BAY': [0, 1, 0],
        'ISLAND': [0, 0, 0]  # or any other default value
    }

    ocean_encoded = np.array([ocean_mapping[prox] for prox in ocean_proximity])

    # Combine longitude and latitude, then apply PCA
    long_lat_combined = np.vstack((std_features[0], std_features[1])).T
    pca = PCA(n_components=1)
    lat_long_Z_Score = pca.fit_transform(long_lat_combined).flatten()

    # Prepare final feature array
    final_features = np.column_stack(std_features[2:] + [ocean_encoded[:, 0], ocean_encoded[:, 1], ocean_encoded[:, 2], lat_long_Z_Score])

    # Load model and predict
    model = load_artifacts()
    predictions = model.predict(final_features)[0]
    return round(np.square(predictions),2)

def get_ocean_proximity():
    global __ocean_prox
    load_artifacts()
    __ocean_prox = __data_cols[6:9] # end indexing is excluded
    return __ocean_prox

def load_artifacts():
    global __data_cols
    global __model
    print("Loading saved artifacts ..... Start")

    with open('columns.json', 'r') as f:
        __data_cols = json.load(f)["data_cols"]

    with open('my_model.pickle', 'rb') as file:
        __model = pickle.load(file)

    print("Loading saved artifacts ..... Done")
    return __model

if __name__ == '__main__':
    longitude = [-121.09]
    latitude = [39.48]
    housing_median_age = [25.0]
    total_rooms = [1665.0]
    total_bedrooms = [374.0]
    households = [330.0]
    median_income = [1.5603]
    population = [845.0]
    ocean_proximity = ['INLAND']
    house_price = predict_house_price(longitude, latitude, housing_median_age, total_rooms, total_bedrooms, households, median_income, population, ocean_proximity)
    print(f"Predicted house price: {house_price}")
