import os
from typing import List

# Telegram API Configuration
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
API_TOKEN = os.getenv("API_TOKEN", "")

# Bot Configuration
BOT_NAME = os.getenv("BOT_NAME", "eBookFilterBot")

# Admin Configuration
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",") if x.strip()]

# Channel Configuration
INDEX_CHANNELS = [int(x) for x in os.getenv("INDEX_CHANNELS", "").split(",") if x.strip()]

# Database Configuration
FILES_DATABASE_URL = os.getenv("FILES_DATABASE_URL", "mongodb://localhost:27017/ebooks_db")

# Bot Settings
FORMATS = ["PDF", "EPUB", "MOBI", "AZW3", "TXT"]
GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Biography", "Technology", "Education"]
LANGUAGES = ["English", "Spanish", "French", "German", "Italian", "Portuguese"]

# Pagination Settings
RESULTS_PER_PAGE = 5
MAX_SEARCH_RESULTS = 50

# File Size Limits (in MB)
MAX_FILE_SIZE = 50

# Rate Limiting
RATE_LIMIT_MESSAGES = 20
RATE_LIMIT_WINDOW = 60  # seconds

# Validation
def validate_config():
    """Validate required configuration values"""
    errors = []
    
    if not API_ID or API_ID == 0:
        errors.append("API_ID is required")
    
    if not API_HASH:
        errors.append("API_HASH is required")
    
    if not API_TOKEN:
        errors.append("API_TOKEN is required")
    
    if not FILES_DATABASE_URL:
        errors.append("FILES_DATABASE_URL is required")
    
    if not ADMINS:
        errors.append("At least one ADMIN is required")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True
