#!/bin/bash

cd /Users/aprendiz/Desktop/nova1/Save-Nova

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Levantando servidor Django..."
python manage.py runserver

