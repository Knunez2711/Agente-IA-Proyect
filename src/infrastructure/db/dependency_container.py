"""
Infrastructure: DependencyContainer
Contenedor de inyección de dependencias (IoC Container).
Conecta los puertos del dominio con sus implementaciones de infraestructura.

Esto es lo que hace que la arquitectura hexagonal sea intercambiable:
para cambiar de Groq a OpenAI, solo cambia el adaptador aquí.
"""
from src.infrastructure.repositories.postgresql_repository import PostgreSQLRepository
from src.infrastructure.llm.groq_llm_adapter import GroqLLMAdapter
from src.application.use_cases.process_query_use_case import ProcessNaturalLanguageQueryUseCase
from src.application.use_cases.get_schema_use_case import GetDatabaseSchemaUseCase


class DependencyContainer:
    """Configura y provee las dependencias de la aplicación."""

    def __init__(self):
        # Infraestructura
        self._db_repository = PostgreSQLRepository()
        self._llm_adapter = GroqLLMAdapter()

        # Casos de uso (inyectando dependencias)
        self._process_query_use_case = ProcessNaturalLanguageQueryUseCase(
            sql_generator=self._llm_adapter,
            db_repository=self._db_repository,
        )
        self._get_schema_use_case = GetDatabaseSchemaUseCase(
            db_repository=self._db_repository,
        )

    @property
    def process_query_use_case(self) -> ProcessNaturalLanguageQueryUseCase:
        return self._process_query_use_case

    @property
    def get_schema_use_case(self) -> GetDatabaseSchemaUseCase:
        return self._get_schema_use_case


# Instancia global del contenedor
container = DependencyContainer()