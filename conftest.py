import os
import sys

# Garante que a raiz do projeto esteja no sys.path, para que
# "from app import app" funcione independentemente de como o
# pytest é chamado (localmente ou no CircleCI).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
