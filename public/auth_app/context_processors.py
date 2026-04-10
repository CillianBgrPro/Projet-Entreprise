import json
import os
from django.conf import settings

def translations(request):
    # Retrieve the current language from session, defaulting to 'fr' if not set.
    lang = request.session.get('lang', 'fr')

    # Construct the file path for the translation JSON file based on the current language.
    file_path = os.path.join(settings.BASE_DIR.parent, 'assets', 'translate', f'{lang}.json')
    
    # Initialize an empty dictionary to store translations data.
    translations_data = {}
    
    # Check if the translation file exists.
    if os.path.exists(file_path):
            # Open and read the translation JSON file.
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                translations_data = json.load(f)
            except Exception:
            # Handle any exceptions that occur during file reading or JSON parsing.
                translations_data = {}
                
    # Return a dictionary containing the translations data and the current language code.
    return {
        't': translations_data,
        'CURRENT_LANG': lang
    }