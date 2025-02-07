document
  .getElementById('signupForm')
  .addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Validate username length
    if (username.length < 6 || username.length > 15) {
      document.getElementById('usernameError').textContent =
        'Username must be between 6 and 15 characters.';
      return;
    } else {
      document.getElementById('usernameError').textContent = '';
    }

    // Validate password length and strength
    if (password.length < 6 || password.length > 15) {
      document.getElementById('passwordError').textContent =
        'Password must be between 6 and 15 characters.';
      return;
    } else if (
      !/[A-Z]/.test(password) ||
      !/[a-z]/.test(password) ||
      !/\d/.test(password)
    ) {
      document.getElementById('passwordError').textContent =
        'Password must contain at least one uppercase letter, one lowercase letter, and one number.';
      return;
    } else {
      document.getElementById('passwordError').textContent = '';
    }

    // Validate confirm password
    if (password !== confirmPassword) {
      document.getElementById('confirmPasswordError').textContent =
        'Passwords do not match.';
      return; // Stop form submission
    } else {
      document.getElementById('confirmPasswordError').textContent = '';
    }

    // Proceed with form submission
    try {
      const response = await fetch('/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        window.location.href = result.redirect;
      } else {
        // Show server error message
        document.getElementById('usernameError').textContent = result.message;
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  });

document
  .getElementById('togglePassword')
  .addEventListener('click', function () {
    const passwordField = document.getElementById('password');
    const isPasswordHidden = passwordField.type === 'password';

    // Toggle the password field type
    passwordField.type = isPasswordHidden ? 'text' : 'password';

    // Change the image source
    this.src = isPasswordHidden
      ? 'static/images/eye_open.png' // If password is hidden, change to eye_open
      : 'static/images/eye_close.png'; // If password is visible, change to eye_close
  });
