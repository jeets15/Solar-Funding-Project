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

        // South Africa
        const south_africa = createButton("../../static/images/countries/south-africa.png", 520, 290, "https://www.google.com/");
        canvas.parentNode.appendChild(south_africa);

        // Argentina
        const argentina = createButton("../../static/images/countries/argentina.png", 300, 300, "https://www.google.com/");
        canvas.parentNode.appendChild(argentina);

        // Australia
        const australia = createButton("../../static/images/countries/australia.png", 775, 280, "https://www.google.com/");
        canvas.parentNode.appendChild(australia);

        // Brazil
        const brazil = createButton("../../static/images/countries/brazil.png", 330, 250, "https://www.google.com/");
        canvas.parentNode.appendChild(brazil);

        // Canada
        const canada = createButton("../../static/images/countries/canada.png", 200, 85, "https://www.google.com/");
        canvas.parentNode.appendChild(canada);

        // Iran
        const iran = createButton("../../static/images/countries/iran.png", 590, 150, "https://www.google.com/");
        canvas.parentNode.appendChild(iran);

        // Saudi Arabia
        const saudi_arabia = createButton("../../static/images/countries/saudi-arabia.png", 570, 170, "https://www.google.com/");
        canvas.parentNode.appendChild(saudi_arabia);

        // USA
        const usa = createButton("../../static/images/countries/united-states-of-america.png", 200, 130, "https://www.google.com/");
        canvas.parentNode.appendChild(usa);

    };
}

// Function to create button on the map
function createButton(imageUrl, x, y, url) {
    const button = document.createElement("button");
    button.style.position = "absolute";
    button.style.top = y + "px";
    button.style.left = x + "px";
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




