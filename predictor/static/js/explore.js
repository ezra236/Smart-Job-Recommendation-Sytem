document.getElementById('predictionForm').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent default form submission

    const form = e.target;
    const formData = new FormData(form);

    fetch("", {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      // Update the page with the returned prediction
      const resultDiv = document.getElementById('prediction-result');
      resultDiv.innerHTML = `<div class="prediction"><h3>Predicted Job Title: ${data.prediction}</h3></div>`;
    })
    .catch(error => console.error('Error:', error));
  });




document.addEventListener("DOMContentLoaded", function () {
    let roles = [];

    // Fetch role categories from JSON
    fetch("/static/json/unique_roles.json")
        .then(response => response.json())
        .then(data => {
            roles = data.map(item => item["Role Category"]); // Extract only role names
        })
        .catch(error => console.error("Error loading role categories:", error));

    const roleInput = document.getElementById("Role");
    // Use the existing suggestion box
    const suggestionBox = document.getElementById("suggestions");

    roleInput.addEventListener("input", function () {
        let input = this.value.toLowerCase();
        suggestionBox.innerHTML = "";

        if (input.length > 0) {
            let filteredRoles = roles.filter(role => role.toLowerCase().startsWith(input));
            
            filteredRoles.slice(0, 50).forEach(role => { // Show up to 10 suggestions
                let item = document.createElement("li");
                item.textContent = role;
                item.addEventListener("click", function () {
                    roleInput.value = role;
                    suggestionBox.innerHTML = ""; // Clear suggestions after selection
                });
                suggestionBox.appendChild(item);
            });
        }
    });

    document.addEventListener("click", function (e) {
        if (!roleInput.contains(e.target) && !suggestionBox.contains(e.target)) {
            suggestionBox.innerHTML = ""; // Hide suggestions when clicking outside
        }
    });
});





document.addEventListener("DOMContentLoaded", function () {
    let roles = [];

    // Fetch role categories from JSON
    fetch("/static/json/unique_area.json")
        .then(response => response.json())
        .then(data => {
            roles = data.map(item => item["Functional Area"]); // Extract only role names
        })
        .catch(error => console.error("Error loading role categories:", error));

    const roleInput = document.getElementById("function");
    // Use the existing suggestion box
    const suggestionBox = document.getElementById("suggestions1");

    roleInput.addEventListener("input", function () {
        let input = this.value.toLowerCase();
        suggestionBox.innerHTML = "";

        if (input.length > 0) {
            let filteredRoles = roles.filter(role => role.toLowerCase().startsWith(input));
            
            filteredRoles.slice(0, 50).forEach(role => { // Show up to 10 suggestions
                let item = document.createElement("li");
                item.textContent = role;
                item.addEventListener("click", function () {
                    roleInput.value = role;
                    suggestionBox.innerHTML = ""; // Clear suggestions after selection
                });
                suggestionBox.appendChild(item);
            });
        }
    });

    document.addEventListener("click", function (e) {
        if (!roleInput.contains(e.target) && !suggestionBox.contains(e.target)) {
            suggestionBox.innerHTML = ""; // Hide suggestions when clicking outside
        }
    });
});





document.addEventListener("DOMContentLoaded", function () {
    let roles = [];

    // Fetch role categories from JSON
    fetch("/static/json/unique_industry.json")
        .then(response => response.json())
        .then(data => {
            roles = data.map(item => item["Industry"]); // Extract only role names
        })
        .catch(error => console.error("Error loading Industry categories:", error));

    const roleInput = document.getElementById("Industry");
    // Use the existing suggestion box
    const suggestionBox = document.getElementById("suggestions2");

    roleInput.addEventListener("input", function () {
        let input = this.value.toLowerCase();
        suggestionBox.innerHTML = "";

        if (input.length > 0) {
            let filteredRoles = roles.filter(role => role.toLowerCase().startsWith(input));
            
            filteredRoles.slice(0, 50).forEach(role => { // Show up to 10 suggestions
                let item = document.createElement("li");
                item.textContent = role;
                item.addEventListener("click", function () {
                    roleInput.value = role;
                    suggestionBox.innerHTML = ""; // Clear suggestions after selection
                });
                suggestionBox.appendChild(item);
            });
        }
    });

    document.addEventListener("click", function (e) {
        if (!roleInput.contains(e.target) && !suggestionBox.contains(e.target)) {
            suggestionBox.innerHTML = ""; // Hide suggestions when clicking outside
        }
    });
});

