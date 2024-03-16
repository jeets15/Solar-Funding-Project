var password = document.getElementById("password")
var confirmpassword = document.getElementById("confirmpassword")

function validateFields() {
    if (password.value !== confirmpassword.value) {
        alert("Passwords do not match")
        return false;
    } else {
        return true;
    }
}
