const goToStats = () => {
    window.location.href = "../html/stats.html";
} 
const goToAdoption = () => {
    window.location.href = "../html/adoption.html";
} 
const goToForm = () => {
    window.location.href = "../html/form.html";
} 



document.getElementById("adoption").addEventListener("click", goToAdoption);

document.getElementById("form").addEventListener("click", goToForm);

document.getElementById("stats").addEventListener("click", goToStats);

