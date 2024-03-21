var makes = document.getElementById('dropdownMake');
makes.innerHTML = '';

// Fetch data from API endpoint
fetch('/cars/makes')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse response as JSON
    })
    .then(data => {
        // Extract the list of options from the data
        var options = data; // Adjust this according to the actual structure of your API response

        // Now you have the list of options, you can use it to populate your dropdown
        // For example:
        options.forEach(function (optionText) {
            makes.innerHTML += `<input type=\"checkbox\" id=\"${optionText}\" name=\"${optionText}\" value=\"${optionText}\">`;
            makes.innerHTML += `<label for=\"${optionText}\">${optionText}</label>`;
            makes.innerHTML += `<br>`;
            // var option = document.createElement("option");
            // option.value = optionText.toLowerCase().replace(/\s/g, ''); // Set value to lowercase without spaces
            // option.text = optionText;
            // dropdown.appendChild(option); // Append option to select element
        });
    })
    .catch(error => console.error('Error fetching data:', error));


fetch('/cars/recommended', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem("token")
    },
})
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse response as JSON
    })
    .then(data => {
        // Extract the list of options from the data
        ads_div = document.getElementById('ads');
        ads_div.innerHTML = `<h1>We recommend!</h1><br><br><h2>${data['CarModel']['make']} ${data['CarModel']['model']} ${data['CarModel']['year']}</h2><br><br><h1>Only ${data['CarModel']['price']}$!</h1><br><h4>${parseInt(data['five_years_price'])}$ for 5 years</h4>`;
        // Now you have the list of options, you can use it to populate your dropdown
        // For example:
    })
    .catch(error => console.error('Error fetching data:', error));

// --------

function toggleMake() {
    var dropdownContent = document.getElementById('dropdownMake');
    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
    } else {
        dropdownContent.style.display = 'block';
    }
}

function toggleYear() {
    var dropdownContent = document.getElementById('dropdownYear');
    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
    } else {
        dropdownContent.style.display = 'block';
    }
}

function toggleRange() {
    var dropdownContent = document.getElementById('dropdownRange');
    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
    } else {
        dropdownContent.style.display = 'block';
    }
}

function toggleMileage() {
    var dropdownContent = document.getElementById('dropdownMileage');
    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
    } else {
        dropdownContent.style.display = 'block';
    }
}

function createCheckboxes2() {
    var checkboxDictionary = {};

    var checkedCheckboxIDs = [];
    var dropdownMake = document.getElementById('dropdownMake');
    var checkboxes = dropdownMake.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            checkedCheckboxIDs.push(checkbox.id);
        }
    });

    var minYearInput = document.getElementById('minYear');
    var minYearValue = minYearInput.value;
    var maxYearInput = document.getElementById('maxYear');
    var maxYearValue = maxYearInput.value;

    var minPriceInput = document.getElementById('minPrice');
    var minPriceValue = minPriceInput.value;
    var maxPriceInput = document.getElementById('maxPrice');
    var maxPriceValue = maxPriceInput.value;

    var maxMileageInput = document.getElementById('maxMileage');
    var maxMileageValue = maxMileageInput.value;

    // console.log(checkedCheckboxIDs);
    // console.log(minYearValue);
    // console.log(maxYearValue);
    // console.log(minPriceValue);
    // console.log(maxPriceValue);

    checkboxDictionary['make'] = checkedCheckboxIDs;

    checkboxDictionary['year_min'] = parseInt(minYearValue);
    checkboxDictionary['year_max'] = parseInt(maxYearValue);

    checkboxDictionary['min_price'] = parseInt(minPriceValue);
    checkboxDictionary['max_price'] = parseInt(maxPriceValue);

    checkboxDictionary['max_mileage'] = parseInt(maxMileageValue);

    // console.log(checkboxDictionary['make']);
    // console.log(checkboxDictionary['min_year']);
    // console.log(checkboxDictionary['max_year']);
    // console.log(checkboxDictionary['min_price']);
    // console.log(checkboxDictionary['max_price']);
    // console.log(checkboxDictionary['max_mileage']);

    // URL to which the request will be sent
    var url = '/cars/find';

    // Options for the fetch request
    var options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem("token")
        },
        body: JSON.stringify(checkboxDictionary),
    };

    // Sending the fetch request
    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            var responses = document.getElementById('responseField');
            // responses.innerHTML = data;
            console.log('Response:', data);
            responses.innerHTML = '';
            // engine_size: 1.6;
            // fuel_type: 'diesel';
            // id: 83364;
            // make: 'vauxhall';
            // mileage: 59000;
            // model: 'insignia';
            // mpg: 74.3;
            // price: 7750;
            // satisfaction: 3.9;
            // tax: 0;
            // transmission: 'manual';
            // year: 2016;

            // data.forEach(function (optionText) {
            //   makes.innerHTML += `<div class="record-line">
            data.forEach(function (data) {
                responses.innerHTML += `<div class="record-line">
  <div class="record-column">
    <h3>Make</h3>
    <p>${data.CarModel.make}</p>
  </div>
  <div class="record-column">
    <h3>Model</h3>
    <p>${data.CarModel.model}</p>
  </div>
  <div class="record-column">
    <h3>Year</h3>
    <p>${data.CarModel.year}</p>
  </div>
  <div class="record-column">
    <h3>Transmission</h3>
    <p>${data.CarModel.transmission}</p>
  </div>
  <div class="record-column">
    <h3>Fuel Type</h3>
    <p>${data.CarModel.fuel_type}</p>
  </div>
  <div class="record-column">
    <h3>MPG</h3>
    <p>${data.CarModel.mpg}</p>
  </div>
  <div class="record-column">
    <h3>Mileage</h3>
    <p>${data.CarModel.mileage}</p>
  </div>
  <div class="record-column">
    <h3>Engine Size</h3>
    <p>${data.CarModel.engine_size}</p>
  </div>
  <div class="record-column">
    <h3>Tax</h3>
    <p>${data.CarModel.tax}</p>
  </div>
  <div class="record-column">
    <h3>Price</h3>
    <p>${data.CarModel.price}</p>
  </div>
    <div class="record-column">
    <h3>Five Years Price</h3>
    <p>${data.five_years_price}</p>
  </div>
</div>
`;
            });
            responses.innerHTML = responseHTML;
        })
        .catch(error => {
            console.error('Error:', error);
        });



fetch('/cars/recommended', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem("token")
    },
})
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse response as JSON
    })
    .then(data => {
        // Extract the list of options from the data
        ads_div = document.getElementById('ads');
        ads_div.innerHTML = `<h1>We recommend!</h1><br><br><h2>${data['CarModel']['make']} ${data['CarModel']['model']} ${data['CarModel']['year']}</h2><br><br><h1>Only ${data['CarModel']['price']}$!</h1><br><h4>${parseInt(data['five_years_price'])}$ for 5 years</h4>`;
        // Now you have the list of options, you can use it to populate your dropdown
        // For example:
    })
    .catch(error => console.error('Error fetching data:', error));


}

