import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
if ENVIRONMENT == "prod":
    dotenv_path = ".env.production"
else:
    dotenv_path = ".env.development"

load_dotenv(dotenv_path)

# Bot Configuration
TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

# Test Guild Configuration
test_guild_id = os.getenv("TEST_GUILD_ID")
if test_guild_id:
    try:
        test_guild_id = int(test_guild_id)
    except ValueError:
        test_guild_id = None
