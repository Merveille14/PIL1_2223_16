// Récupérer les boutons de changement de langue
const langToggleButtons = document.querySelectorAll("#lang-toggle button");
// Écouter l'événement de clic sur les boutons de changement de langue
langToggleButtons.forEach(button => {
 button.addEventListener("click", toggleLanguage);
});
// Fonction pour basculer la langue
function toggleLanguage(event) {
 const lang = event.target.dataset.lang;
 // Modifier les variables CSS personnalisées en fonction de la langue sélectionnée
 if (lang === "fr") {
 document.documentElement.setAttribute("lang", "fr");
 } else if (lang === "en") {
 document.documentElement.setAttribute("lang", "en");
 }
}