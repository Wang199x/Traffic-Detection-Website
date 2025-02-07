// Assign event to the "Start" button
document.getElementById('startButton').addEventListener('click', () => {
  const username = '{{ username }}'; // Get the username value from the Flask template

  const currentURL = window.location.origin; // Get the base URL

  if (username) {
    // If logged in, redirect to /process
    window.location.href = `${currentURL}/process`;
  } else {
    // If not logged in, redirect to /login
    window.location.href = `${currentURL}/login`;
  }
});

// Other events (homeLink, signupLink, loginLink) remain the same
document.getElementById('homeLink').addEventListener('click', (e) => {
  e.preventDefault(); // Prevent default behavior
  window.scrollTo({ top: 0, behavior: 'smooth' }); // Smooth scroll to the top of the page
});

document.getElementById('signupLink').addEventListener('click', (e) => {
  e.preventDefault(); // Prevent default behavior
  const baseUrl = window.location.origin; // Get the base URL
  window.location.href = `${baseUrl}/signup`; // Redirect to /signup
});

document.getElementById('loginLink').addEventListener('click', (e) => {
  e.preventDefault(); // Prevent default behavior
  const baseUrl = window.location.origin; // Get the base URL
  window.location.href = `${baseUrl}/login`; // Redirect to /login
});

// Log out the user when the "Logout" button is clicked
document.getElementById('logoutButton').addEventListener('click', () => {
  sessionStorage.removeItem('username'); // Remove the username from sessionStorage
  window.location.href = window.location.origin; // Reload the homepage
});
