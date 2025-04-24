// script.js - Frontend logic for Car Price Predictor

// Initialize form with data from the server
function initializeForm(formData) {
  const categories = formData.categories;
  const numericRanges = formData.numeric_ranges;

  // Populate brand dropdown
  const brandSelect = document.getElementById("brand");
  categories.brand.sort().forEach((brand) => {
    const option = document.createElement("option");
    option.value = brand;
    option.textContent = brand;
    brandSelect.appendChild(option);
  });

  // Populate model years dropdown
  const yearSelect = document.getElementById("model_year");
  categories.model_year
    .sort((a, b) => b - a)
    .forEach((year) => {
      const option = document.createElement("option");
      option.value = year;
      option.textContent = year;
      yearSelect.appendChild(option);
    });

  // Populate fuel type dropdown
  const fuelSelect = document.getElementById("fuel_type");
  categories.fuel_type.sort().forEach((fuel) => {
    const option = document.createElement("option");
    option.value = fuel;
    option.textContent = fuel === "no_entry" ? "Not Specified" : fuel;
    fuelSelect.appendChild(option);
  });

  // Populate accident dropdown
  const accidentSelect = document.getElementById("accident");
  categories.accident.sort().forEach((accident) => {
    const option = document.createElement("option");
    option.value = accident;
    option.textContent = accident === "no_entry" ? "Not Specified" : accident;
    accidentSelect.appendChild(option);
  });

  // Set numeric range hints
  document.getElementById(
    "milage_range"
  ).textContent = `Range: ${numericRanges.milage.min} - ${numericRanges.milage.max}`;
  document.getElementById(
    "horsepower_range"
  ).textContent = `Range: ${numericRanges.horsepower.min} - ${numericRanges.horsepower.max}`;
  document.getElementById(
    "engine_L_range"
  ).textContent = `Range: ${numericRanges.engine_L.min} - ${numericRanges.engine_L.max}`;

  // Add event listener for brand selection to populate models
  brandSelect.addEventListener("change", function () {
    populateModels(this.value, categories.models_by_brand);
  });

  // Add event listener for form submission
  document
    .getElementById("predictionForm")
    .addEventListener("submit", function (e) {
      e.preventDefault();
      predictPrice();
    });
}

// Populate models based on selected brand
function populateModels(brand, modelsByBrand) {
  const modelSelect = document.getElementById("model");

  // Clear previous options
  modelSelect.innerHTML = '<option value="">Select a model</option>';

  // Disable if no brand selected
  if (!brand) {
    modelSelect.disabled = true;
    return;
  }

  // Enable and populate models
  modelSelect.disabled = false;

  if (modelsByBrand[brand]) {
    modelsByBrand[brand].sort().forEach((model) => {
      const option = document.createElement("option");
      option.value = model;
      option.textContent = model === "no_entry" ? "Not Specified" : model;
      modelSelect.appendChild(option);
    });
  }
}

// Make prediction API call
async function predictPrice() {
  // Hide previous results
  document.getElementById("resultContainer").style.display = "none";
  document.getElementById("errorContainer").style.display = "none";

  // Get form data
  const formData = {
    brand: document.getElementById("brand").value,
    model: document.getElementById("model").value,
    model_year: parseInt(document.getElementById("model_year").value),
    milage: parseInt(document.getElementById("milage").value),
    fuel_type: document.getElementById("fuel_type").value,
    accident: document.getElementById("accident").value,
    clean_title: parseInt(document.getElementById("clean_title").value),
  };

  // Add optional numeric fields if they're filled
  const horsepower = document.getElementById("horsepower").value;
  if (horsepower) {
    formData.horsepower = parseFloat(horsepower);
  }

  const engineL = document.getElementById("engine_L").value;
  if (engineL) {
    formData.engine_L = parseFloat(engineL);
  }

  try {
    // Submit prediction request
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const result = await response.json();

    if (result.error) {
      showError(result.error);
    } else {
      showResult(result.formatted_price);
    }
  } catch (error) {
    showError("Network error. Please try again.");
  }
}

// Display prediction result
function showResult(price) {
  document.getElementById("predictedPrice").textContent = price;
  document.getElementById("resultContainer").style.display = "block";
}

// Display error message
function showError(message) {
  document.getElementById("errorMessage").textContent = message;
  document.getElementById("errorContainer").style.display = "block";
}
