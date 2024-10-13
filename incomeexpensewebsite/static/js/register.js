document.addEventListener('DOMContentLoaded', () => {
    // username verification
    const usernameField = document.querySelector("#usernameField");
    const feedbackArea = document.querySelector(".invalid-feedback");
    const usernameSuccess = document.querySelector(".usernameSuccess");

    // email verification
    const emailField = document.querySelector("#emailField");
    const emailfeedbackArea = document.querySelector(".emailfeedbackArea");
    const emailSuccess = document.querySelector(".emailSuccess");

    //submit button
    const submitBtn = document.querySelector(".submit-btn");
    

    // showPasswordToggle
    const passwordField = document.querySelector("#passwordField");
    const showPasswordToggle = document.querySelector(".showPasswordToggle");

    console.log('Password Field:', passwordField); // Should log the input field
    console.log('Toggle Button:', showPasswordToggle); 
    const handleToggleInput = () => {
        console.log('Toggle Button Clicked');  // Check if this logs when you click the toggle
        if (showPasswordToggle.textContent === "SHOW") {
            showPasswordToggle.textContent = "HIDE";
            passwordField.setAttribute("type", "text");
        } else {
            showPasswordToggle.textContent = "SHOW";
            passwordField.setAttribute("type", "password");
        }
    };

    showPasswordToggle.addEventListener("click", handleToggleInput);

    // username verification event
    usernameField.addEventListener("keyup", (e) => {
        const usernameVal = e.target.value;
        usernameSuccess.style.display = "block";
        usernameSuccess.textContent = `Checking ${usernameVal}`;
        usernameField.classList.remove("is-invalid");
        feedbackArea.style.display = "none";

        // API request for username validation
        if (usernameVal.length > 0) {
            fetch("/authentication/validate-username/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: usernameVal }),
            })
            .then((response) => response.json())
            .then((data) => {
                usernameSuccess.style.display = "none";
                if (data.username_error) {
                    submitBtn.setAttribute("disabled","disabled");
                    submitBtn.disabled=true;
                    usernameField.classList.add("is-invalid");
                    feedbackArea.style.display = "block";
                    feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                }else{
                    submitBtn.removeAttribute("disabled");
                }
            });
        }
    });

    // email verification event
    emailField.addEventListener("keyup", (e) => {
        const emailVal = e.target.value;
        emailSuccess.style.display = "block";
        emailSuccess.textContent = `Checking ${emailVal}`;
        emailField.classList.remove("is-invalid");
        emailfeedbackArea.style.display = "none";

        // API request for email validation
        if (emailVal.length > 0) {
            fetch("/authentication/validate-email/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email: emailVal }),
            })
            .then((response) => response.json())
            .then((data) => {
                emailSuccess.style.display = "none";
                if (data.email_error) {
                    submitBtn.setAttribute("disabled","disabled");
                    submitBtn.disabled=true;
                    emailField.classList.add("is-invalid");
                    emailfeedbackArea.style.display = "block";
                    emailfeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                }else{
                    submitBtn.removeAttribute("disabled");
                }
            });
        }
    });
});
