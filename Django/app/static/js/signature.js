
document.addEventListener('DOMContentLoaded', function() {
    
    var canvas = document.getElementById('signature');
    if (!canvas) {
        console.error('Canvas with id "signature" not found!');
        return;
    }
    
    // Prevent scaling by setting CSS size to match attributes

    canvas.style.width = canvas.width + 'px';
    canvas.style.height = canvas.height + 'px';
    
    var ctx = canvas.getContext("2d");
    var drawing = false;
    var prevX, prevY;
    var currX, currY;
    var signature = document.getElementsByName('signature')[0];
    if (!signature) {
        console.error('Hidden input with name "signature" not found!');
        return;
    }

    // Mouse events
    canvas.addEventListener("mousedown", start);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stop);
    canvas.addEventListener("mouseout", stop); // Stop drawing if mouse leaves canvas

    // Touch events for mobile
    canvas.addEventListener("touchstart", start);
    canvas.addEventListener("touchmove", draw);
    canvas.addEventListener("touchend", stop);

    function start(e) {
        e.preventDefault(); // Prevent scrolling on touch
        drawing = true;
    }

    function stop(e) {
        e.preventDefault();
        drawing = false;
        prevX = prevY = null;
        if (signature) {
            signature.value = canvas.toDataURL();
        }
    }

    function draw(e) {
        e.preventDefault(); // Prevent scrolling on touch
        if (!drawing) return;

        // Use offsetX/Y for mouse events (accounts for scaling)
        if (e.offsetX !== undefined) {
            currX = e.offsetX;
            currY = e.offsetY;
        } else {
            // For touch events, calculate scaled position
            var rect = canvas.getBoundingClientRect();
            currX = (e.touches[0].clientX - rect.left) * (canvas.width / rect.width);
            currY = (e.touches[0].clientY - rect.top) * (canvas.height / rect.height);
        }

        if (!prevX && !prevY) {
            prevX = currX;
            prevY = currY;
        }

        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
        ctx.lineTo(currX, currY);
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.closePath();

        prevX = currX;
        prevY = currY;
    }

    // Make clearCanvas function global so it can be called from HTML
    window.clearCanvas = function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        if (signature) {
            signature.value = ''; // Clear the hidden input too
        }
    };

});

function getCookie(name) {
  let cookieArr = document.cookie.split(";");
  for(let i = 0; i < cookieArr.length; i++) {
    let cookiePair = cookieArr[i].split("=");
    /* Removing whitespace from the beginning of the cookie name
    and compare it with the given string */
    if(name == cookiePair[0].trim()) {
      return decodeURIComponent(cookiePair[1]);
    }
  }
  return null;
}

function saveSignature()
{

let csrftoken;

const canvas = document.getElementById('signature');
const dataURL = canvas.toDataURL('image/png'); // Get base64 string
console.log(dataURL);
console.log(JSON.stringify({ image: dataURL }))

// Example sending via fetch

fetch("", 
    {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is included
    },
    body: JSON.stringify({image:dataURL})
})
};

document.getElementById('save_my_signature').addEventListener("click", saveSignature)