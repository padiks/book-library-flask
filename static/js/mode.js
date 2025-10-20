// Dark/Light mode toggle
const modeToggle = document.getElementById('modeToggle');
const modeIcon = document.getElementById('modeIcon');
// Load saved theme
if (localStorage.getItem('theme') === 'dark') {
  document.body.classList.add('dark-mode');
  modeIcon.className = 'bi bi-moon-fill';
} else {
  document.body.classList.remove('dark-mode');
  modeIcon.className = 'bi bi-sun-fill';
}
// Toggle on click
modeToggle.addEventListener('click', (e) => {
  e.preventDefault();
  document.body.classList.toggle('dark-mode');
  if (document.body.classList.contains('dark-mode')) {
    modeIcon.className = 'bi bi-moon-fill';
    localStorage.setItem('theme', 'dark');
  } else {
    modeIcon.className = 'bi bi-sun-fill';
    localStorage.setItem('theme', 'light');
  }
});