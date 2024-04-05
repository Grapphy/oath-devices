function displayAlert(type, message) {
    var alertContainer = document.getElementById("alertContainer");
    var alert = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">${message}</div>`;
    alertContainer.innerHTML = alert;
}


function generateBase32Secret(length) {
    const base32Charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
    const base32Length = length;
    let base32 = '';
    const randomBytes = new Uint8Array(base32Length);
    window.crypto.getRandomValues(randomBytes);
    for (let i = 0; i < base32Length; i++) {
      base32 += base32Charset[randomBytes[i] % base32Charset.length];
    }
    return base32
}


function generateOATH(issuer, label, secret) {
    return new OTPAuth.TOTP({
        issuer: issuer,
        label: label,
        algorithm: "SHA1",
        digits: 6,
        period: 30,
        secret: OTPAuth.Secret.fromBase32(secret)
    });
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


function registerOATHDevice(code, secret, password) {
    fetch("http://localhost:5050/api/v1/@me/mfa/totp/enable", {
        method: "POST",
        headers: {
            "X-Auth-Token": access_token
        },
        body: JSON.stringify({
            password: password,
            code: code,
            secret: secret
        })
    })
    .then(response => {
        if (!response.ok) {
            console.log("Failure");
        }
        return response.json();
    })
    .then(data => {
        console.log("backup_codes: " + data.backup_codes);
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


document.getElementById("profile-container").querySelector("#enable-mfa").addEventListener("click", function(event) {
    console.log("do somethiunig");

    document.getElementById("profile-container").hidden = true;
    document.getElementById("mfa-step-up-container").hidden = false;
    
    let secret = generateBase32Secret(32)
    let otpmfa = generateOATH("MyApp", "Robert", secret);
    
    const qr = new QRious({
        element: document.getElementById("mfa-step-up-container").querySelector('#qrcode'),
        value: otpmfa.toString(),
        size: 400
    });
})