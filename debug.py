"""
Use this file with ipython for interactive shell django

Используй этот файл вместе с ipython для инетакивного взаимодействия с shell django

example:
ipython 
>>> import debug.py
>>> import mainapp.model
"""

import django
import os
project_name = 'geekshop'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
django.setup()

# Now this script or any imported module can use any part of Django it needs.
