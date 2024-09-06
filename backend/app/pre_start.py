""" This Python file merely tests whether the database is up. 
"""

from app.core.db import engine
from tenacity import retry, after_log, before_log, stop_after_attempt, wait_fixed
import logging

from sqlmodel import Session, select 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_TRIES   = 60 * 5    # every 5 minutes
RETRY       = 1         # wait a second then try again

@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(RETRY),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN)
)
def init_db(engine):
    try:
        with Session(engine) as session:
            # Run a command on the database to see if it is active.
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e

def main():
    logger.info("Initializing the database...")
    init_db(engine)
    logger.info("Completed initializing the database")

if __name__ == "__main__":
    main()