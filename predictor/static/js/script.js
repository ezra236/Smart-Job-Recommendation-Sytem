// script.js
document.getElementById('signIn').addEventListener('click', function() {
    const signInForm = document.getElementById('signInForm');
    signInForm.classList.toggle('active'); // Toggle the form's visibility and scale
});

// Optional: Close the form when clicking outside of it
document.addEventListener('click', function(event) {
    const signInForm = document.getElementById('signInForm');
    const isClickInsideForm = signInForm.contains(event.target);
    const isSignInButton = event.target === document.getElementById('signIn');

    if (!isClickInsideForm && !isSignInButton && signInForm.classList.contains('active')) {
        signInForm.classList.remove('active'); // Hide the form
    }
});


// script.js
document.getElementById('signIn1').addEventListener('click', function() {
    const signInForm = document.getElementById('signInForm1');
    signInForm.classList.toggle('active'); // Toggle the form's visibility and scale
});

// Optional: Close the form when clicking outside of it
document.addEventListener('click', function(event) {
    const signInForm = document.getElementById('signInForm1');
    const isClickInsideForm = signInForm.contains(event.target);
    const isSignInButton = event.target === document.getElementById('signIn1');

    if (!isClickInsideForm && !isSignInButton && signInForm.classList.contains('active')) {
        signInForm.classList.remove('active'); // Hide the form
    }
});



document.addEventListener("DOMContentLoaded", function () {
    const postJobBtn = document.getElementById("post");

    postJobBtn.addEventListener("click", function () {
        const postUrl = postJobBtn.getAttribute("data-url"); // Get the Django URL
        window.open(postUrl, "_blank");
    });
});




document.addEventListener("DOMContentLoaded", function () {
    const postJobBtn = document.getElementById("postq");

    postJobBtn.addEventListener("click", function () {
        window.open("postT.html", "_blank");
    });
});




document.querySelector('.btn1').addEventListener('click', function(e) {
    e.preventDefault();
    
    // Hide the welcome section.
    var welcomeSection = document.querySelector('.welcome-section1');
    if (welcomeSection) {
      welcomeSection.style.display = 'none';
    }
    
    // Hide the original sign-in form block.
    var form1 = document.querySelector('.signin-form1');
    if (form1) {
      form1.style.display = 'none';
    }
    
    // Show the new form with a transition.
    var form2 = document.getElementById('signInForm2');
    if (form2) {
      form2.style.display = 'block';
      // Force a reflow (optional, to ensure transition happens)
      void form2.offsetWidth;
      // Add the active class to trigger the transition
      form2.classList.add('active');
    }
});
