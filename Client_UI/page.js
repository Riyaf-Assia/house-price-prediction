function estimatePrice(event) {
    // Prevent the form from refreshing the page
    event.preventDefault();

    // Collect form data
    var formData = {
        longitude: $('#longitude').val(),
        latitude: $('#latitude').val(),
        housing_median_age: $('#housing-median-age').val(),
        total_rooms: $('#total-rooms').val(),
        total_bedrooms: $('#total-bedrooms').val(),
        households: $('#households').val(),
        median_income: $('#median-income').val(),
        population: $('#population').val(),
        ocean_proximity: $('#ocean-proximity').val()
    };

    // Print form data to console (optional)
    console.log("Longitude:", formData.longitude);
    console.log("Latitude:", formData.latitude);
    console.log("Housing Median Age:", formData.housing_median_age);
    console.log("Total Rooms:", formData.total_rooms);
    console.log("Total Bedrooms:", formData.total_bedrooms);
    console.log("Households:", formData.households);
    console.log("Median Income:", formData.median_income);
    console.log("Population:", formData.population);
    console.log("Ocean Proximity:", formData.ocean_proximity);

    // Send the data to the backend using AJAX
    $.ajax({
        url: 'http://127.0.0.1:5000/predict_house_price',  // The URL to send data to (your Flask route)
        type: 'POST',
        data: formData,  // Send form data
        success: function(response) {
            // Display the result in the <p id="price"> element
            $('#price').text('$' + response.price.toFixed(2));
        },
        error: function() {
            $('#price').text('Error in predicting price. Please try again.');
        }
    });
}
