"""
Infrastructure: PostgreSQLRepository
Implementación concreta del DatabaseRepositoryPort usando PostgreSQL + SQLAlchemy.
"""
import logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.domain.ports.database_repository_port import DatabaseRepositoryPort
from src.domain.entities.database_schema import DatabaseSchema, Table, TableColumn
from src.domain.exceptions.domain_exceptions import DatabaseQueryException
from src.infrastructure.db.database_config import create_db_engine

logger = logging.getLogger(__name__)


class PostgreSQLRepository(DatabaseRepositoryPort):
    """
    Adaptador de infraestructura: PostgreSQL.
    Implementa el contrato DatabaseRepositoryPort.
    """

    def __init__(self):
        self._engine = create_db_engine()

    def get_schema(self) -> DatabaseSchema:
        """Extrae el esquema de la base de datos y lo mapea a entidades del dominio."""
        query = """
            SELECT
                t.table_name,
                c.column_name,
                c.data_type,
                c.is_nullable,
                tc.constraint_type
            FROM information_schema.tables t
            JOIN information_schema.columns c
                ON t.table_name = c.table_name AND t.table_schema = c.table_schema
            LEFT JOIN information_schema.key_column_usage kcu
                ON c.column_name = kcu.column_name AND c.table_name = kcu.table_name
            LEFT JOIN information_schema.table_constraints tc
                ON kcu.constraint_name = tc.constraint_name
            WHERE t.table_schema = 'public'
                AND t.table_type = 'BASE TABLE'
            ORDER BY t.table_name, c.ordinal_position;
        """
        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(query))
                rows = result.fetchall()

            # Agrupar columnas por tabla
            tables_map: dict[str, list[TableColumn]] = {}
            for row in rows:
                table_name = row[0]
                if table_name not in tables_map:
                    tables_map[table_name] = []
                tables_map[table_name].append(
                    TableColumn(
                        name=row[1],
                        data_type=row[2],
                        is_nullable=row[3] == "YES",
                        constraint=row[4] or "",
                    )
                )

            tables = [Table(name=name, columns=cols) for name, cols in tables_map.items()]
            return DatabaseSchema(tables=tables)

        except SQLAlchemyError as e:
            logger.error(f"Error obteniendo esquema: {e}")
            raise DatabaseQueryException(str(e))

    def execute_query(self, sql: str) -> dict:
        """Ejecuta una query SQL de solo lectura y retorna columnas + filas."""
        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(sql))
                columns = list(result.keys())
                rows = [list(row) for row in result.fetchall()]

            logger.info(f"Query ejecutada exitosamente — {len(rows)} filas retornadas")
            return {"columns": columns, "rows": rows}

        except SQLAlchemyError as e:
            logger.error(f"Error ejecutando query: {e}")
            raise DatabaseQueryException(str(e))