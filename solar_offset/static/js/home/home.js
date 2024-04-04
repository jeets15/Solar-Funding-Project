// Message Section
setTimeout(function () {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'none';
    }
}, 5000);


// Map Section

// Call the drawMap function to display the map
drawMap(document.getElementById("canvas-1"));
drawMap(document.getElementById("canvas-2"));
drawMap(document.getElementById("canvas-3"));

// Helper Methods

// Function to draw map on canvas
function drawMap(canvas) {
    // Customize the dimensions of canvas
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const ctx = canvas.getContext("2d");

    // Create instance & load image
    const img = new Image();
    img.src = canvas.getAttribute("src");

    // Event Handler on image load
    img.onload = function () {
        // Draw the image on the canvas
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        // Remove any existing buttons
        const buttons = canvas.parentNode.querySelectorAll("button");
        buttons.forEach(button => button.remove());

        // Add the buttons again with updated positions and sizes
        addButtons(canvas);
    };
}

// Function to add buttons on the map
function addButtons(canvas) {
    // South Africa
    const south_africa = createButton("../../static/images/countries/south-africa.png", 55, 57, "{{ url_for('householder.country', country_code='za')}}");
    canvas.parentNode.appendChild(south_africa);

    // Argentina
    const argentina = createButton("../../static/images/countries/argentina.png", 32, 60, "{{ url_for('householder.country', country_code='ar')}}");
    canvas.parentNode.appendChild(argentina);

    // Australia
    const australia = createButton("../../static/images/countries/australia.png", 84, 55, "{{ url_for('householder.country', country_code='au')}}");
    canvas.parentNode.appendChild(australia);

    // Brazil
    const brazil = createButton("../../static/images/countries/brazil.png", 35, 50, "{{ url_for('householder.country', country_code='br')}}");
    canvas.parentNode.appendChild(brazil);

    // Canada
    const canada = createButton("../../static/images/countries/canada.png", 20, 17, "{{ url_for('householder.country', country_code='ca')}}");
    canvas.parentNode.appendChild(canada);

    // Iran
    const iran = createButton("../../static/images/countries/iran.png",63 , 29, "{{ url_for('householder.country', country_code='ir')}}");
    canvas.parentNode.appendChild(iran);

    // Saudi Arabia
    const saudi_arabia = createButton("../../static/images/countries/saudi-arabia.png", 60, 33, "{{ url_for('householder.country', country_code='sa')}}");
    canvas.parentNode.appendChild(saudi_arabia);

    // USA
    const usa = createButton("../../static/images/countries/united-states-of-america.png", 20, 25, "{{ url_for('householder.country', country_code='us')}}");
    canvas.parentNode.appendChild(usa);
}

// Function to create button on the map
function createButton(imageUrl, x, y, url) {
    const button = document.createElement("button");
    button.style.position = "absolute";
    button.style.top = y + "%";
    button.style.left = x + "%";
    button.style.width = "25px";
    button.style.height = "25px";
    button.style.border = "none";
    button.style.borderRadius = "50%";
    button.style.cursor = "pointer";
    button.style.backgroundImage = "url(" + imageUrl + ")";
    button.style.backgroundSize = "cover";
    button.addEventListener("click", function () {
        window.location.href = url;
    });
    return button;
}


// Add event listener for window resize
window.addEventListener("resize", function () {
    const canvases = document.querySelectorAll("#canvas-1, #canvas-2, #canvas-3");
    canvases.forEach(canvas => drawMap(canvas));
});





