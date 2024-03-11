setTimeout(function () {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'none';
    }
}, 5000);

.table-container{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    overflow: auto;
}