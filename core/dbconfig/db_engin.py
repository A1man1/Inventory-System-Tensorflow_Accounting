from databases import Database
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from core.settings import Settings
from starlette.requests import Request


def get_database(request: Request) -> Database:
        """Get current database from app state.

        Args:
            request (Request): HTTP Request object through API.

        Returns:
            Database: Apps database.
        """
        return request.app.state._db


def get_db() -> Database:
        """Configure database for the application.

        Returns:
            Database: Current DB for the application.
        """
        options = {
            "min_size": Settings().db_pool_min_size,
            "max_size": Settings().db_pool_max_size,
            "force_rollback": Settings().db_force_roll_back,
        }
        return Database(Settings().database_url, **options)

URL_DB=str(Settings().database_url)
db: Database = get_db()
metadata = sqlalchemy.MetaData()
