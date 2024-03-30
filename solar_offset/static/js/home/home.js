// Message Section
setTimeout(function () {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'none';
    }
}, 5000);


// Map Section

// Fetching all the canvas
const canvas1 = document.getElementById("canvas-1");

const canvas2 = document.getElementById("canvas-2");

const canvas3 = document.getElementById("canvas-3");


// Draw the map
function drawMap(canvas) {

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const ctx = canvas.getContext("2d");

    // Load the map image
    const img = new Image();
    img.src = canvas.getAttribute("src");

    img.onload = function () {
        // Draw the image on the canvas
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        // Add interactivity (e.g., highlight regions on click)
        canvas.addEventListener("click", function (e) {
            var rect = canvas.getBoundingClientRect();
            var x = e.clientX - rect.left;
            var y = e.clientY - rect.top;

            // Check if the click is within a specific region
            if (x >= 100 && x <= 200 && y >= 100 && y <= 200) {
                // Highlight the region
                ctx.beginPath();
                ctx.rect(100, 100, 100, 100);
                ctx.strokeStyle = "red";
                ctx.stroke();
            }
        });
    };
}

// Call the drawMap function to display the map
drawMap(canvas1);
drawMap(canvas2);
drawMap(canvas3);

