#!/usr/bin/env python3
"""
Manual database seeding script
Run this if automatic seeding doesn't work: python seed_manual.py
"""

import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("=" * 60)
        logger.info("MANUAL DATABASE SEEDING")
        logger.info("=" * 60)
        
        from app.database.seed_data import seed_database
        
        logger.info("Starting seed process...")
        seed_database()
        
        logger.info("=" * 60)
        logger.info("SEEDING COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        logger.info("")
        logger.info("Test accounts created:")
        logger.info("  Patient: patient@test.com / Test123!")
        logger.info("  Doctor:  doctor@test.com / Test123!")
        logger.info("  Admin:   admin@test.com / Test123!")
        logger.info("")
        
        return 0
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("SEEDING FAILED!")
        logger.error("=" * 60)
        logger.error(f"Error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())