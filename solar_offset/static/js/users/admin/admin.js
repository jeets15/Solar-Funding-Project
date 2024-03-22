var suspendBtns = document.getElementsByClassName('suspend-btn');
var userIdInput = document.querySelector('#suspendModalBox input[name="user_id"]');

// Event listener for the suspend button click
for (var i = 0; i < suspendBtns.length; i++) {
    suspendBtns[i].addEventListener('click', function () {
        // Get the user id value
        var userId = this.getAttribute('data-userid');
        // Set the user id value to the hidden input tag in the modal form
        userIdInput.value = userId;
    });
}