const searchButton = document.querySelector("#searchbutton")
const statsBox = document.querySelector(".results")

searchButton.addEventListener('click', () => {
  console.log('Button clicked!');
  statsBox.classList.add('active'); //show autocomplete box
});