// Function to open and prefill the global application form
function openForm(companyName, companyEmail) {
    document.getElementById("formCompanyName").value = companyName;
    document.getElementById("formCompanyEmail").value = companyEmail;
    var form = document.getElementById("globalApplyForm");
    
    // First, set display to block if it isn't already
    form.style.display = "block";
    
    // Force a reflow (optional) and then add the "show" class to trigger the transition
    setTimeout(function() {
      form.classList.add("show");
    }, 10);
  }
  

  function closeForm() {
    var form = document.getElementById("globalApplyForm");
    form.classList.remove("show");
    // Optionally, hide the form after the transition ends
    setTimeout(function() {
      form.style.display = "none";
    }, 500); // matches the transition duration
  }
  



document.getElementById("resume-upload").addEventListener("change", function(){
    var fileName = this.files[0] ? this.files[0].name : "No file chosen";
    document.getElementById("file-chosen").textContent = fileName;
});

