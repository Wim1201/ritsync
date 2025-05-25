# check_env.py
import os
from dotenv import load_dotenv

load_dotenv()
print("ORS API KEY:", os.getenv("ORS_API_KEY"))
