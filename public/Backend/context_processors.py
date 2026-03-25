def template(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' # on verifie si la requete viens du router
    return {
        'base_template': 'partial.html' if is_ajax else 'index.html' # si la requete viens du router on renvoi partial.html sinon index.html
    }
