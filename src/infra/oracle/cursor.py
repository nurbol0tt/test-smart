import logging
from typing import List, Tuple, Union

import cx_Oracle
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import scoped_session

from src.core.settings import settings


class OracleCursor:
    @classmethod
    def oracle_sync_session(cls, url: str) -> scoped_session:
        engine = create_engine(
            url, pool_pre_ping=True, future=True,
            max_overflow=50, pool_size=25, pool_timeout=45
        )
        factory = orm.sessionmaker(
            engine, autoflush=False, expire_on_commit=False,
        )
        return scoped_session(factory)

    @classmethod
    def call_oracle_function(cls, func_name: str) -> Union[List[Tuple], None]:
        session = cls.oracle_sync_session(url=settings.NEW_ORACLE_URI)
        result_cursor = None
        cursor = None

        try:
            # Get the raw connection from the session
            connection = session.connection().connection

            # Create a cursor
            cursor = connection.cursor()

            # Prepare the SQL statement to call the function
            result_cursor = connection.cursor()
            cursor.execute(
                f"BEGIN :result := {func_name}(); END;",
                           result=result_cursor
            )

            # Fetch the result from the result cursor
            rows = result_cursor.fetchall()

            # Get column names from the result cursor description
            columns = [col[0] for col in result_cursor.description]

            results_as_dicts = []
            for row in rows:
                result_dict = dict(zip(columns, row))
                results_as_dicts.append(result_dict)

            return results_as_dicts

        except Exception as e:
            logging.error(
                "Failed to execute Oracle function: %s",
                str(e)
            )
            raise

        finally:
            # Close the cursors if they are initialized
            if result_cursor:
                result_cursor.close()
            if cursor:
                cursor.close()

            # Remove the session
            session.remove()

    @staticmethod
    def check_oracle_connection() -> bool:
        try:
            connection = cx_Oracle.connect(settings.NEW_ORACLE_URI)

            if connection.ping():
                logging.info("Successfully connected to Oracle database.")
                return True
            else:
                logging.error("Failed to ping Oracle database.")
                return False

        except cx_Oracle.Error as error:
            logging.error("Error connecting to Oracle database: %s", error)
            return False
