#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.normal')
    
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        version = os.environ.get('APP_VERSION', 'normal')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'shop.settings.{version}')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


