var eyeicon = document.querySelector("#passwordfield i")
var eyeiconconfirmpassword = document.querySelector("#confirmpasswordfield i")
var password = document.getElementById("password")
var confirmpassword = document.getElementById("confirmpassword")
const requirementList = document.querySelectorAll(".requirement-list li");
const requirements = [
    {regex: /.{8,}/, index: 0}, // Minimum of 8 characters
    {regex: /[0-9]/, index: 1}, // At least one number
    {regex: /[a-z]/, index: 2}, // At least one lowercase letter
    {regex: /[^A-Za-z0-9]/, index: 3}, // At least one special character
    {regex: /[A-Z]/, index: 4}, // At least one uppercase letter
]

function validateFields() {
    if (password.value != confirmpassword.value) {
        alert("Passwords do not match")
        return false;
    } else {
        return true;
    }
}

eyeicon.addEventListener("click", () => {
    // Toggle the password input type between "password" and "text"
    password.type = password.type === "password" ? "text" : "password";
    // Update the eye icon class based on the password input type
    eyeicon.className = `fa-solid fa-eye${password.type === "password" ? "" : "-slash"}`;
});

password.addEventListener("keyup", (e) => {
    requirements.forEach(item => {
        // Check if the password matches the requirement regex
        const isValid = item.regex.test(e.target.value);
        const requirementItem = requirementList[item.index];
        // Updating class and icon of requirement item if requirement matched or not
        if (isValid) {
            requirementItem.classList.add("valid");
            requirementItem.firstElementChild.className = "fa-solid fa-check";
        } else {
            requirementItem.classList.remove("valid");
            requirementItem.firstElementChild.className = "fa-solid fa-circle";
        }
    });
});

eyeiconconfirmpassword.addEventListener("click", () => {
    // Toggle the password input type between "password" and "text"
    confirmpassword.type = confirmpassword.type === "password" ? "text" : "password";
    // Update the eye icon class based on the password input type
    eyeiconconfirmpassword.className = `fa-solid fa-eye${confirmpassword.type === "password" ? "" : "-slash"}`;
});