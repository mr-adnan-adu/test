import logging
import sys
from pyrogram import Client
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid
from info import API_ID, API_HASH, API_TOKEN, BOT_NAME, validate_config
from utils import ensure_directory_exists

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class EBookBot:
    def __init__(self):
        self.app = None
        self.initialize()
    
    def initialize(self):
        """Initialize bot with error handling"""
        try:
            # Validate configuration
            validate_config()
            
            # Ensure required directories exist
            ensure_directory_exists('logs')
            ensure_directory_exists('data')
            
            # Initialize Pyrogram client
            self.app = Client(
                name="eBookFilterBot",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=API_TOKEN,
                plugins={"root": "plugins"},
                workdir="data"
            )
            
            logger.info(f"Bot initialized successfully: {BOT_NAME}")
            
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            sys.exit(1)
    
    def run(self):
        """Run the bot with error handling"""
        try:
            logger.info(f"Starting {BOT_NAME}...")
            self.app.run()
            
        except ApiIdInvalid:
            logger.error("Invalid API_ID. Please check your configuration.")
            sys.exit(1)
        except ApiIdPublishedFlood:
            logger.error("API_ID is flood limited. Please try again later.")
            sys.exit(1)
        except AccessTokenInvalid:
            logger.error("Invalid API_TOKEN. Please check your bot token.")
            sys.exit(1)
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Bot runtime error: {e}")
            sys.exit(1)
        finally:
            logger.info("Bot shutdown complete")

def main():
    """Main function"""
    try:
        bot = EBookBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
