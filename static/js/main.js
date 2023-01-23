const form = document.getElementById("scraper-form");
const loadingAnimation = document.getElementById("loading-animation");
const stopForm = document.getElementById("stop-form");
stopForm.addEventListener("submit", (event) => {
    event.preventDefault();
    fetch("/stop", { method: "POST" })
      .then(response => response.json())
      .then(data => {
        if (data.status === "stopped") {
          alert("Scraping process stopped");
        }
      });
  });

form.addEventListener("submit", (event) => {
    event.preventDefault();
    loadingAnimation.style.display = "block";
    checkStatus();
});
// function to check the status of the scraping process
function checkStatus() {
    // send a GET request to the status endpoint
    fetch("/status")
      .then(response => response.json())
      .then(data => {
        // check the status of the scraping process
        if (data.status === "scraping") {
          // if the scraping is not done, call the checkStatus function again after 1 second
          setTimeout(checkStatus, 1000);
        } else {
          // if the scraping is done, hide the loading animation and show a success message
          loadingAnimation.style.display = "none";
          alert("Scraping process is finished!");

        }
      });
  }
  
  // call the checkStatus function when the form is submitted
  document.getElementById("scraper-form").onsubmit = function() {
    document.getElementById("loading").style.display = "block";
    checkStatus();
  };
  