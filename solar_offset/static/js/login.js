var eyeicon = document.querySelector("#passwordfield i")
var password = document.getElementById("password")
var userid = document.getElementById("userid").value


eyeicon.addEventListener("click", () => {
    // Toggle the password input type between "password" and "text"
    password.type = password.type === "password" ? "text" : "password";
    // Update the eye icon class based on the password input type
    eyeicon.className = `fa-solid fa-eye${password.type === "password" ? "" : "-slash"}`;
});

setTimeout(function () {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'none';
    }
}, 5000);