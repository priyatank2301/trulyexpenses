// console.log('Register Working')

const usernameField = document.querySelector('#usernameField');
const feedbackArea=document.querySelector('.invalid-feedback');
const usernameSuccess=document.querySelector('.usernameSuccess');
const emailField=document.querySelector('#emailField');
const emailfeedbackArea=document.querySelector('.emailfeedbackArea');
const emailSuccess=document.querySelector('.emailSuccess');
usernameField.addEventListener("keyup", (e) => {
    console.log('777', 777);

    const usernameVal = e.target.value;
    // console.log(usernameVal);
    usernameSuccess.style.display = 'block';
    usernameSuccess.textContent=`Checking ${usernameVal}`;

    usernameField.classList.remove('is-invalid');
                feedbackArea.style.display='none';
                

    //for api request
    if (usernameVal.length > 0) {
        fetch('/authentication/validate-username/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: usernameVal })
        })
        .then(response => response.json())
        .then(data => {
            console.log("data", data);
            usernameSuccess.style.display = 'none';
            if(data.username_error){
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display='block';
                feedbackArea.innerHTML=`<p>${data.username_error}</p>`;
            }
        });
    }
});


emailField.addEventListener("keyup", (e) => {
    console.log('777', 777);

    const emailVal = e.target.value;
    // console.log(usernameVal);

    emailSuccess.style.display = 'block';
    emailSuccess.textContent=`Checking ${emailVal}`;

    emailField.classList.remove('is-invalid');
                emailfeedbackArea.style.display='none';
                

    //for api request
    if (emailVal.length > 0) {
        fetch('/authentication/validate-email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: emailVal })
        })
        .then(response => response.json())
        .then(data => {
            console.log("data", data);
            emailSuccess.style.display = 'none';
            if(data.email_error){
                emailField.classList.add('is-invalid');
                emailfeedbackArea.style.display='block';
                emailfeedbackArea.innerHTML=`<p>${data.email_error}</p>`;
            }
        });
    }
});
