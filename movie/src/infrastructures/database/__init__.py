# flake8: noqa
from urllib.parse import urlparse

from movie.src.core.config import settings

DATABASE_TYPE, _, _ = urlparse(settings.DATABASE_URL).scheme.partition('+')
if DATABASE_TYPE == 'sqlite':
    from .sqlite import AsyncSQLiteEngine as AsyncRelationalDBEngine
    from .sqlite import AsyncSQLiteScopedSession as AsyncScopedSession
    from .sqlite import get_async_sqlite_session as get_async_session
    from .sqlite import initialize_sqlite_db as initialize_db

    IS_RELATIONAL_DB = True

elif DATABASE_TYPE == 'postgresql':
    from .postgres import AsyncPostgreSQLEngine as AsyncRelationalDBEngine
    from .postgres import AsyncPostgreSQLScopedSession as AsyncScopedSession
    from .postgres import get_async_postgresql_session as get_async_session
    from .postgres import initialize_postgres_db as initialize_db

    IS_RELATIONAL_DB = True

else:
    raise RuntimeError(
        f'Invalid database type \'{DATABASE_TYPE}\' provided in DATABASE_URL: {settings.DATABASE_URL}'
    )
