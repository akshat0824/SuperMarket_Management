// script.js

// Function to validate numeric input fields.
function validateNumberInput(event) {
     const inputValue=parseFloat(event.target.value);

     // Check if the input is a valid positive number.
     if(isNaN(inputValue) || inputValue <=0) {
         alert("Please enter a valid positive number.");
         event.target.value ="";
         event.target.focus();
         return false; // Prevent form submission.
     }
}

// Attach event listeners to numeric fields.
document.addEventListener("DOMContentLoaded", function() {
     const numericInputs=document.querySelectorAll("input[type='number']");

     numericInputs.forEach(input => {
         input.addEventListener("blur", validateNumberInput);
         input.addEventListener("keydown", function(e) {
             if (e.key === 'Enter') {
                 validateNumberInput({ target: input });
             }
         });
     });
});

// Example function to handle form submission via AJAX (optional).
function handleFormSubmission(event) {
     event.preventDefault(); // Prevent default form submission.

     const formData=new FormData(event.target);

     fetch(event.target.action, {
         method:'POST',
         body:formData,
         headers:{
             'X-Requested-With':'XMLHttpRequest' // Indicate AJAX request.
         }
     })
     .then(response => response.json())
     .then(data => {
         // Handle success response.
         console.log(data);
         alert("Form submitted successfully!");

         // Optionally redirect or update the UI here.
         window.location.reload(); // Reload page to see updated data.
     })
     .catch(error => {
         console.error("Error:", error);
         alert("There was an error submitting the form.");
     });
}

// Attach event listeners for forms (optional).
const forms=document.querySelectorAll("form");
forms.forEach(form => {
     form.addEventListener("submit", handleFormSubmission);
});