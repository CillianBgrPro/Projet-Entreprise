#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """
    Entry point for running administrative tasks.
    This function initializes the Django settings module, attempts to import Django's management commands,
    and executes those commands based on the command-line arguments provided.

    Raises:
        ImportError: If Django cannot be imported due to missing installation or incorrect PYTHONPATH.
    
    Returns:
        None
    """
    # Set the default value for the DJANGO_SETTINGS_MODULE environment variable.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
    
    try:
        # Import Django's execute_from_command_line function from django.core.management module.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an ImportError with a message indicating that Django is not installed or PYTHONPATH is incorrect.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the management commands passed as command-line arguments.
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()