#!/usr/bin/env python3
"""
Database initialization script
Creates tables and seeds initial data
"""

import sys
import time
import logging
from sqlalchemy import text

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Wait for database to be ready
logger.info("Waiting for database to be ready...")
time.sleep(5)

try:
    from app.core.database import engine, Base
    from app.database.seed_data import seed_database
    
    logger.info("Testing database connection...")
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    logger.info("Database connection successful!")
    
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")
    
    logger.info("Seeding database with initial data...")
    seed_database()
    logger.info("Database initialization completed successfully!")
    
except Exception as e:
    logger.error(f"Database initialization failed: {e}")
    sys.exit(1)