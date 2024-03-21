import logging

EARLY_MILEAGE = 8000.00  # amount of miles car drives in a year
SATISFACTION_MULTIPLIER = 70  # will multiply satisfaction by it's value, used to make satisfaction affect car's list
MAX_SATISFACTION = 5

# Database configuration
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/database"

# JWT configuration
SECRET_KEY = "supersecretkey"
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_TIME = 180  # expiry time in minutes
GUEST_JWT_EXPIRY_TIME = 525_600_000  # 1000 years

# Logging configuration
LOGGING_LEVEL = logging.DEBUG
