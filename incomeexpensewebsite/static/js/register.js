// console.log('Register Working')

const usernameField = document.querySelector('#usernameField');
const feedbackArea=document.querySelector('.invalid-feedback');
usernameField.addEventListener("keyup", (e) => {
    console.log('777', 777);

    const usernameVal = e.target.value;
    // console.log(usernameVal);

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
            if(data.username_error){
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display='block';
                feedbackArea.innerHTML=`<p>${data.username_error}</p>`;
            }
        });
    }
});
