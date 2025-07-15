import os
import logging
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

# Rate limiting storage
user_message_count = defaultdict(list)

def format_result(result: Dict[str, Any]) -> str:
    """Format search result for display"""
    if not result:
        return "No result found."
    
    title = result.get('title', 'Unknown Title')
    author = result.get('author', 'Unknown Author')
    genre = result.get('genre', 'Unknown Genre')
    format_type = result.get('format', 'Unknown Format')
    size = result.get('size', 'Unknown Size')
    language = result.get('language', 'Unknown Language')
    file_link = result.get('file_link', '#')
    
    # Clean up title and author
    title = clean_text(title)
    author = clean_text(author)
    
    return (
        f"📚 **{title}**\n"
        f"👤 **Author**: {author}\n"
        f"🏷️ **Genre**: {genre}\n"
        f"📄 **Format**: {format_type}\n"
        f"📊 **Size**: {size}\n"
        f"🌐 **Language**: {language}\n"
        f"🔗 [Download]({file_link})"
    )

def clean_text(text: str) -> str:
    """Clean and validate text input"""
    if not text or not isinstance(text, str):
        return "Unknown"
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\-.,!?()[\]{}]', '', text)
    
    # Limit length
    if len(text) > 100:
        text = text[:97] + "..."
    
    return text if text else "Unknown"

def validate_query(query: str) -> bool:
    """Validate search query"""
    if not query or not isinstance(query, str):
        return False
    
    # Remove whitespace
    query = query.strip()
    
    # Check length
    if len(query) < 2 or len(query) > 100:
        return False
    
    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9\s\-.,!?()[\]{}]+$', query):
        return False
    
    return True

def is_rate_limited(user_id: int, limit: int = 20, window: int = 60) -> bool:
    """Check if user is rate limited"""
    try:
        now = datetime.now()
        cutoff = now - timedelta(seconds=window)
        
        # Clean old messages
        user_message_count[user_id] = [
            msg_time for msg_time in user_message_count[user_id] 
            if msg_time > cutoff
        ]
        
        # Check if over limit
        if len(user_message_count[user_id]) >= limit:
            return True
        
        # Add current message
        user_message_count[user_id].append(now)
        return False
        
    except Exception as e:
        logger.error(f"Error checking rate limit: {e}")
        return False

def extract_file_info(document) -> Dict[str, Any]:
    """Extract file information from Telegram document"""
    try:
        if not document:
            return {}
        
        # Get file extension and format
        file_name = document.file_name or "unknown"
        file_size = document.file_size or 0
        mime_type = document.mime_type or ""
        
        # Determine format
        format_map = {
            "application/pdf": "PDF",
            "application/epub+zip": "EPUB",
            "application/x-mobipocket-ebook": "MOBI",
            "application/vnd.amazon.ebook": "AZW3",
            "text/plain": "TXT"
        }
        
        format_type = format_map.get(mime_type, "UNKNOWN")
        
        # Format file size
        if file_size > 0:
            size_mb = file_size / (1024 * 1024)
            size_str = f"{size_mb:.2f} MB"
        else:
            size_str = "Unknown"
        
        return {
            "file_name": file_name,
            "file_size": file_size,
            "format": format_type,
            "size": size_str,
            "mime_type": mime_type
        }
        
    except Exception as e:
        logger.error(f"Error extracting file info: {e}")
        return {}

def parse_title_author(text: str) -> tuple:
    """Parse title and author from text"""
    if not text:
        return "Unknown", "Unknown"
    
    # Common patterns for "Title by Author" or "Author - Title"
    patterns = [
        r'^(.+?)\s+by\s+(.+?)$',  # Title by Author
        r'^(.+?)\s+-\s+(.+?)$',   # Author - Title
        r'^(.+?)\s+\|\s+(.+?)$',  # Title | Author
    ]
    
    for pattern in patterns:
        match = re.match(pattern, text.strip(), re.IGNORECASE)
        if match:
            return clean_text(match.group(1)), clean_text(match.group(2))
    
    return clean_text(text), "Unknown"

def ensure_directory_exists(path: str) -> bool:
    """Ensure directory exists"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {path}: {e}")
        return False

def safe_int_conversion(value: str, default: int = 0) -> int:
    """Safely convert string to int"""
    try:
        return int(value) if value else default
    except (ValueError, TypeError):
        return default

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    if not filename:
        return "unknown_file"
    
    # Remove dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext
    
    return filename

def format_stats(stats: Dict[str, Any]) -> str:
    """Format statistics for display"""
    total_books = stats.get('total_books', 0)
    total_users = stats.get('total_users', 0)
    total_searches = stats.get('total_searches', 0)
    
    formats = stats.get('formats', {})
    genres = stats.get('genres', {})
    
    text = f"📊 **Bot Statistics**\n\n"
    text += f"📚 Total Books: {total_books}\n"
    text += f"👥 Total Users: {total_users}\n"
    text += f"🔍 Total Searches: {total_searches}\n\n"
    
    if formats:
        text += "**Formats:**\n"
        for format_type, count in sorted(formats.items()):
            text += f"• {format_type}: {count}\n"
        text += "\n"
    
    if genres:
        text += "**Genres:**\n"
        for genre, count in sorted(genres.items()):
            text += f"• {genre}: {count}\n"
    
    return text

def validate_file_type(mime_type: str) -> bool:
    """Validate if file type is supported"""
    supported_types = [
        "application/pdf",
        "application/epub+zip",
        "application/x-mobipocket-ebook",
        "application/vnd.amazon.ebook",
        "text/plain"
    ]
    
    return mime_type in supported_types

def get_file_icon(format_type: str) -> str:
    """Get emoji icon for file format"""
    icons = {
        "PDF": "📄",
        "EPUB": "📖",
        "MOBI": "📱",
        "AZW3": "📚",
        "TXT": "📝"
    }
    
    return icons.get(format_type, "📄")
