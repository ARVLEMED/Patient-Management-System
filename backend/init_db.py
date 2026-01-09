#!/usr/bin/env python3
"""
Database initialization script
Creates tables and seeds initial data
"""

import sys
import time
import logging
from sqlalchemy import text, inspect

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_tables_exist(engine):
    """Check if tables already exist"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return len(tables) > 0

def main():
    logger.info("=" * 50)
    logger.info("DATABASE INITIALIZATION STARTING")
    logger.info("=" * 50)
    
    try:
        from app.core.database import engine, Base, SessionLocal
        from app.database.seed_data import seed_database
        
        # Test database connection
        logger.info("Testing database connection...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("✓ Database connection successful!")
        
        # Check if tables already exist
        tables_exist = check_tables_exist(engine)
        
        if tables_exist:
            logger.info("✓ Database tables already exist")
            
            # Check if data exists
            db = SessionLocal()
            try:
                from app.models.models import User
                user_count = db.query(User).count()
                
                if user_count > 0:
                    logger.info(f"✓ Database already seeded ({user_count} users found)")
                    logger.info("Skipping seed data...")
                else:
                    logger.info("Tables exist but no data found. Seeding database...")
                    seed_database()
                    logger.info("✓ Database seeded successfully!")
            finally:
                db.close()
        else:
            # Create tables
            logger.info("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("✓ Database tables created successfully!")
            
            # Seed database
            logger.info("Seeding database with initial data...")
            seed_database()
            logger.info("✓ Database seeded successfully!")
        
        logger.info("=" * 50)
        logger.info("DATABASE INITIALIZATION COMPLETED")
        logger.info("=" * 50)
        return 0
        
    except Exception as e:
        logger.error("=" * 50)
        logger.error("DATABASE INITIALIZATION FAILED")
        logger.error("=" * 50)
        logger.error(f"Error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())