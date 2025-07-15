import logging
from pymongo import MongoClient, errors
from pymongo.collection import Collection
from info import FILES_DATABASE_URL
from typing import Optional, Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.client: Optional[MongoClient] = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Establish database connection with error handling"""
        try:
            self.client = MongoClient(
                self.database_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client["ebooks_db"]
            self.create_indexes()
            logger.info("Database connected successfully")
        except errors.ServerSelectionTimeoutError:
            logger.error("Database connection timeout")
            raise
        except errors.ConnectionFailure:
            logger.error("Database connection failed")
            raise
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Create text index for search
            self.db.ebooks.create_index([
                ("title", "text"),
                ("author", "text"),
                ("genre", "text")
            ])
            
            # Create individual indexes
            self.db.ebooks.create_index("title")
            self.db.ebooks.create_index("author")
            self.db.ebooks.create_index("genre")
            self.db.ebooks.create_index("format")
            self.db.ebooks.create_index("file_id")
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    def get_collection(self, name: str) -> Collection:
        """Get collection with connection check"""
        if not self.client or not self.db:
            self.connect()
        return self.db[name]
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("Database connection closed")

# Initialize database manager
try:
    db_manager = DatabaseManager(FILES_DATABASE_URL)
    ebooks_collection = db_manager.get_collection("ebooks")
    bans_collection = db_manager.get_collection("bans")
    users_collection = db_manager.get_collection("users")
    stats_collection = db_manager.get_collection("stats")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")
    raise

# Database helper functions
def safe_insert_ebook(ebook_data: Dict[str, Any]) -> bool:
    """Safely insert ebook with validation"""
    try:
        # Validate required fields
        required_fields = ['title', 'file_id', 'format']
        for field in required_fields:
            if field not in ebook_data or not ebook_data[field]:
                logger.error(f"Missing required field: {field}")
                return False
        
        # Check for duplicates
        existing = ebooks_collection.find_one({
            "file_id": ebook_data["file_id"]
        })
        if existing:
            logger.info(f"Duplicate ebook found: {ebook_data['title']}")
            return False
        
        # Insert with default values
        ebook_data.setdefault("author", "Unknown")
        ebook_data.setdefault("genre", "Unknown")
        ebook_data.setdefault("language", "Unknown")
        ebook_data.setdefault("size", "Unknown")
        
        ebooks_collection.insert_one(ebook_data)
        logger.info(f"Ebook inserted: {ebook_data['title']}")
        return True
        
    except Exception as e:
        logger.error(f"Error inserting ebook: {e}")
        return False

def safe_search_ebooks(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Safely search ebooks with error handling"""
    try:
        results = ebooks_collection.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}},
                {"genre": {"$regex": query, "$options": "i"}}
            ]
        }).limit(limit)
        
        return list(results)
        
    except Exception as e:
        logger.error(f"Error searching ebooks: {e}")
        return []

def safe_get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Safely get user data"""
    try:
        return users_collection.find_one({"user_id": user_id})
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        return None

def safe_add_user(user_data: Dict[str, Any]) -> bool:
    """Safely add user"""
    try:
        existing = users_collection.find_one({"user_id": user_data["user_id"]})
        if not existing:
            users_collection.insert_one(user_data)
            return True
        return False
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        return False

def is_user_banned(user_id: int) -> bool:
    """Check if user is banned"""
    try:
        return bans_collection.find_one({"user_id": user_id}) is not None
    except Exception as e:
        logger.error(f"Error checking ban status: {e}")
        return False
