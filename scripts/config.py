import os
import sys
from dotenv import load_dotenv

# Get path to the project root (one level up from /scripts)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# Load .env from root
dotenv_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path)

# Grab the key
FRED_API_KEY = os.getenv("FRED_API_KEY")

# Safety check
if not FRED_API_KEY:
    sys.exit(
        "❌ Missing FRED_API_KEY! Please create a `.env` file in the project root.\n"
        "Example:\nFRED_API_KEY=your_actual_key_here"
    )
