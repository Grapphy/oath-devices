function displayAlert(type, message) {
    var alertContainer = document.getElementById("alertContainer");
    var alert = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">${message}</div>`;
    alertContainer.innerHTML = alert;
}


function displayProfile(access_token) {
    document.getElementById("login-container").hidden = true;
    
    fetch("http://localhost:5050/api/v1/@me", {
        method: "GET",
        headers: {
            "X-Auth-Token": access_token
        }
    })
    .then(response => {
        if (!response.ok) {
            console.log("Failure");
        }
        return response.json();
    })
    .then(data => {
        var profileContainer = document.getElementById("profile-container");
        profileContainer.hidden = false;
        profileContainer.querySelector("#userId").textContent = data.id;
        profileContainer.querySelector("#username").textContent = data.name;
        profileContainer.querySelector("#mfa-status").textContent = (data.mfa_enabled) ? "Enabled" : "Disabled";
    })
    .catch(error => {
        console.log(error);
    });
}


document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the values from the form
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Construct the request body
    var requestBody = JSON.stringify({
        username: username,
        password: password
    });

    // Make a POST request to the API endpoint
    fetch("http://localhost:5050/api/v1/auth", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: requestBody
    })
    .then(response => {
        if (!response.ok) {
            displayAlert("danger", "Login failed.");
        }
        return response.json();
    })
    .then(data => {
        displayProfile(data.access_token);
    })
    .catch(error => {
        displayAlert("danger", "Error:", error);
    });
});
