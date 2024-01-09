function updateClock() {
    const timeDisplay = document.getElementById("time-display");
    const selectedTimezone = document.getElementById("text-input").value;

    const now = new Date();
    const options = { timeZone: selectedTimezone };
    const formattedTime = now.toLocaleTimeString("en-US", options);
    timeDisplay.textContent = formattedTime;
}

setInterval(updateClock, 1000); // Update clock every second
