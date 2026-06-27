import os

# Database configurations
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "smartassist")

# OpenAI API config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

# Session timeout in seconds
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", 3600))
