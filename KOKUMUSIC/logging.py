import logging
from pymongo import MongoClient
import time
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from logging.handlers import RotatingFileHandler
from config import LOG_FILE_NAME
import config 

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

# Set the logging level for specific libraries to ERROR
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

# Main logger for the application
LOGGERR = logging.getLogger(__name__)

# MongoDB setup
boot = time.time()
mongodb = MongoCli(config.MONGO_DB_URI)
db = mongodb.Anonymous
mongo = MongoClient(config.MONGO_DB_URI)

# App configuration
OWNER = config.OWNER_ID

# Function to get additional loggers
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

