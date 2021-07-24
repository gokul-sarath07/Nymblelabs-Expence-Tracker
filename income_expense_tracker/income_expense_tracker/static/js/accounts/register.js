const usernameField = document.querySelector('.register-form-username-input');
const usernameFeedbackArea = document.querySelector('.invalid-username-feedback');
const emailField = document.querySelector('.register-form-email-input');
const emailFeedbackArea = document.querySelector('.invalid-email-feedback');
const passwordField = document.querySelector('.register-form-password-input');
const passwordFeedbackArea = document.querySelector('.invalid-password-feedback');


// Username Validation
usernameField.addEventListener('keyup', (e) => {
  const usernameValue = e.target.value;

  usernameField.style.borderColor = "white"
  usernameFeedbackArea.style.display = "none"


  if (usernameValue.length > 0) {

    fetch('/accounts/validate-username', {
      body: JSON.stringify({
        username: usernameValue
      }),
      method: "POST"
    })
      .then(res => res.json())
      .then(data => {
        if (data.username_error) {
          usernameField.style.borderColor = "red"
          usernameFeedbackArea.style.display = "block";
          usernameFeedbackArea.innerText = `${ data.username_error }`;
        } else {
          usernameField.style.borderColor = "green";
        }
      })
  }
})

// Email Validation
emailField.addEventListener('keyup', (e) => {
  const emailValue = e.target.value;

  emailField.style.borderColor = "white"
  emailFeedbackArea.style.display = "none"


  if (emailValue.length > 0) {

    fetch('/accounts/validate-email', {
      body: JSON.stringify({
        email: emailValue
      }),
      method: "POST"
    })
      .then(res => res.json())
      .then(data => {
        if (data.email_error) {

          emailField.style.borderColor = "red"
          emailFeedbackArea.style.display = "block";
          emailFeedbackArea.innerText = `${ data.email_error }`;
        } else {
          emailField.style.borderColor = "green";
        }
      })
  }
})


// Password Validation
passwordField.addEventListener('keyup', (e) => {
  const passwordValue = e.target.value;

  passwordField.style.borderColor = "white";
  passwordFeedbackArea.style.display = "none";


  if (passwordValue.length >= 6) {
    passwordField.style.borderColor = "green";
  }

  if (passwordValue.length > 0 && passwordValue.length < 6) {
    fetch('/accounts/validate-password', {
      body: JSON.stringify({
        password: passwordValue
      }),
      method: "POST"
    })
      .then(res => res.json())
      .then(data => {
        if (data.password_error) {
          passwordField.style.borderColor = "red";
          passwordFeedbackArea.style.display = "block";
          passwordFeedbackArea.innerText = `${ data.password_error }`;
        }
      })
  }
})
