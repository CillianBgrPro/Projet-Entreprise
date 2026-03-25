document.addEventListener('click', (e) => { // verifi que les cliques sur la page entiere concerne des liens ou non
    const link = e.target.closest('a');
    if (link && link.href && link.origin === location.origin) { // verifi que c'est un lien et qu'il ne renvoie pas sur un autre site (nom de domaine) + si contient un href
        e.preventDefault(); // empeche de chager simplement que la page html du href
        loadPage(link.href); // charge selon notre méthode pour utiliser simplement comme un template
    }
});

window.addEventListener('popstate', () => { // bouton retour ou avancer de la souris
    loadPage(location.href, false);
});

async function loadPage(url, pushState = true) { // charge la page
    try {
        const response = await fetch(url, { // appel context_processors.py pour renvoyer les templates
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        const htmlFragment = await response.text(); // recupere le template
        
        document.querySelector('#app-content').innerHTML = htmlFragment; // remplace le contenu de la page
        
        if (pushState) {
            history.pushState(null, '', url); // ajoute l url dans l historique pour le boutton avant et arriere
        }
    } catch (err) {
        window.location.href = url; // si une erreuir intervien recharge la page normalement
    }
}
