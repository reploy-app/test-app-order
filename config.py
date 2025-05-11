import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description="OrderService Microservice")
parser.add_argument(
    "--launch-mode",
    dest="launch_mode",
    type=str,
    help="Launch mode: api or worker"
)
args, _ = parser.parse_known_args()

# Launch Mode
LAUNCH_MODE = os.getenv("LAUNCH_MODE", "api")
launch_mode_arg = args.launch_mode
if launch_mode_arg:
    LAUNCH_MODE = launch_mode_arg

# HTTP Service Config
PORT = int(os.getenv("PORT", 8000))

# PostgreSQL Config
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "user_service_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# Redis Config
REDIS_HOST = os.getenv("REDIS_HOST", "redis-shared")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
