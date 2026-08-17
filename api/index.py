import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

os.chdir(BACKEND_DIR)
sys.path.insert(0, BACKEND_DIR)

from app import app