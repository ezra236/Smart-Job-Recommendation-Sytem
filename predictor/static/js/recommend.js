function openGlobalForm(companyName, companyEmail) {
    // Pre-fill the form fields with company info
    document.getElementById('formCompanyName').value = companyName;
    document.getElementById('formCompanyEmail').value = companyEmail;

    var formElement = document.getElementById('globalApplyForm');
    // Set display to block so it becomes visible in the layout
    formElement.style.display = 'block';
    // Force a reflow so that the transition works (this is optional in most cases)
    void formElement.offsetWidth;
    // Add the 'show' class to trigger the transition
    formElement.classList.add('show');
  }

  function closeForm() {
    var formElement = document.getElementById('globalApplyForm');
    // Remove the 'show' class to trigger the reverse transition
    formElement.classList.remove('show');
    // After the transition completes (0.5s), hide the element again
    setTimeout(function() {
      formElement.style.display = 'none';
    }, 500);
  }




  document.getElementById("resume-upload").addEventListener("change", function(){
    var fileName = this.files[0] ? this.files[0].name : "No file chosen";
    document.getElementById("file-chosen").textContent = fileName;
});

