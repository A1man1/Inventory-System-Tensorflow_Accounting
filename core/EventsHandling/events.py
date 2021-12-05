from typing import Callable

import pymongo
import sqlalchemy
from core.config import log
from core.dbconfig import db_engin
from core.settings import Settings
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker


async def connect_to_db(app: FastAPI) -> None:
        """Function to create a database connection for current app.

        Args:
            app (FastAPI App)

        Raises:
            Exception: DB CONNECTION ERROR.

        Returns:
            None (Opens DB Connection)
        """
        try:
            log.info("connecting to a database")
            await db_engin.db.connect()
            app.state._db = db_engin.db

            engine = sqlalchemy.create_engine(db_engin.URL_DB)
            db_engin.metadata.create_all(engine)


            client = pymongo.MongoClient(Settings().mongo_db_url)
            client.server_info()
            log.info("Connected to MongoDB Database")

            log.info("Database connection - successful")
        except Exception as e:
            log.warn("--- DB CONNECTION ERROR ---")
            log.warn(e)
            log.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
        """Function to close a database connection for current app.

        Args:
            app (FastAPI App)

        Raises:
            Exception: DB DISCONNECT ERROR.

        Returns:
            None (Close DB Connection)
        """

        try:
            log.info("Closing connection to database")
            await app.state._db.disconnect()
            log.info("Database connection - closed")
        except Exception as e:
            log.warn("--- DB DISCONNECT ERROR ---")
            log.warn(e)
            log.warn("--- DB DISCONNECT ERROR ---")


def create_start_app_handler(app: FastAPI) -> Callable:
    """Decorator to handle app startup event along with DB connection.

    Args:
        app (FastAPI App)

    Returns:
        start_app (DB connected App Object)
    """
    
    async def start_app() -> None:
        await connect_to_db(app)
    return start_app

    
def create_stop_app_handler(app: FastAPI) -> Callable:
    """Decorator to handle app shutdown event after closed DB connection.

    Args:
        app (FastAPI App)

    Returns:
        stop_app (DB disconnect App Object)
    """
    
    async def stop_app() -> None:
        await close_db_connection(app)
    return stop_app
