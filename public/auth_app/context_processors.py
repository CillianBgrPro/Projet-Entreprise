import json
import os
from django.conf import settings

def translations(request):
    lang = request.session.get('lang', 'fr')

    file_path = os.path.join('assets/translate', f'{lang}.json')
    
    translations_data = {}
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                translations_data = json.load(f)
            except Exception:
                translations_data = {}
                
    return {
        't': translations_data,
        'CURRENT_LANG': lang
    }