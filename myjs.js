// Function to update the clock every second
function updateClock() {
  const clockElement = document.getElementById("clock");
  const currentTime = new Date().toLocaleTimeString();
  clockElement.textContent = currentTime;
}

// Set an initial timeout to start the clock
setTimeout(updateClock, 1000);

// Set an interval to update the clock every second
setInterval(updateClock, 1000);
