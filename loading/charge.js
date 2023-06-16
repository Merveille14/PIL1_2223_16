const loader = document.querySelector('.loader');
window.addEventListener('load', () => {
  setTimeout(() => {
    loader.classList.add('fondu-out');
    window.location.href = 'accueils.html';

    // Créer un nouvel élément div
    const message = document.createElement('div');

    // Ajouter du texte à l'intérieur de l'élément
    message.textContent = 'Loading complete';

    // Ajouter des styles à l'élément
    message.style.backgroundColor = 'yellow';
    message.style.color = 'black';
    message.style.padding = '10px';

    // Ajouter l'élément au corps de la page (ou à un autre élément de votre choix)
    document.body.appendChild(message);

    // Supprimer l'élément après 1 seconde
    setTimeout(() => {
      message.remove();
    }, 1000); // 1000 millisecondes équivalent à 1 seconde
  }, 10000); // Attendre 10 secondes avant d'ajouter la classe 'fondu-out' et de rediriger
});