"""
Infrastructure: GroqLLMAdapter
Implementación concreta del SQLGeneratorPort usando Groq + LangChain.
"""
import os
import re
import logging
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from src.domain.ports.sql_generator_port import SQLGeneratorPort
from src.domain.entities.database_schema import DatabaseSchema
from src.domain.exceptions.domain_exceptions import SQLGenerationException

logger = logging.getLogger(__name__)

MODEL_NAME = "llama-3.1-70b-versatile"


class GroqLLMAdapter(SQLGeneratorPort):
    """
    Adaptador de infraestructura: Groq API con LangChain.
    Implementa el contrato SQLGeneratorPort.
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY no está configurada en las variables de entorno.")

        self._llm = ChatGroq(
            api_key=api_key,
            model_name=MODEL_NAME,
            temperature=0,
        )
        logger.info(f"GroqLLMAdapter inicializado con modelo: {MODEL_NAME}")

    def generate_sql(self, question: str, schema: DatabaseSchema) -> str:
        """Genera SQL a partir de una pregunta usando LLaMA 3.1 vía Groq."""
        system_prompt = f"""Eres un experto en SQL y análisis de datos. Tu única tarea es generar queries SQL correctas para PostgreSQL.

REGLAS ESTRICTAS:
- Responde SOLO con la query SQL dentro de bloques ```sql ```
- Solo genera queries SELECT o WITH (nunca INSERT, UPDATE, DELETE, DROP, etc.)
- Usa aliases descriptivos en las columnas para que sean legibles
- Limita con LIMIT 10 por defecto si la pregunta pide "top" o "más"
- Usa ILIKE para búsquedas de texto (case-insensitive)
- Los montos están en pesos colombianos
- No expliques nada, solo retorna el SQL

ESQUEMA DE LA BASE DE DATOS:
{schema.to_prompt_text()}"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=question),
            ]
            response = self._llm.invoke(messages)
            sql = self._extract_sql(response.content)

            if not sql:
                raise SQLGenerationException("El modelo no retornó SQL válido.")

            logger.debug(f"SQL generado: {sql}")
            return sql

        except SQLGenerationException:
            raise
        except Exception as e:
            logger.error(f"Error en Groq al generar SQL: {e}")
            raise SQLGenerationException(str(e))

    def interpret_results(
        self,
        question: str,
        sql: str,
        columns: list[str],
        rows: list[list],
    ) -> str:
        """Interpreta los resultados de la query en lenguaje natural."""
        system_prompt = (
            "Eres un analista de datos experto. Interpreta los resultados de "
            "consultas SQL de forma clara y conversacional en español. "
            "Sé conciso, directo y destaca los datos más relevantes. "
            "Formatea valores monetarios con $ y separadores de miles."
        )

        user_prompt = f"""El usuario preguntó: "{question}"

Query ejecutada:
```sql
{sql}
```

Resultados ({len(rows)} filas):
Columnas: {columns}
Datos: {rows}

Proporciona una interpretación clara y útil en 2-4 oraciones."""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
            response = self._llm.invoke(messages)
            return response.content

        except Exception as e:
            logger.error(f"Error interpretando resultados: {e}")
            return "Los resultados fueron obtenidos exitosamente. Revisa la tabla para ver los datos."

    @staticmethod
    def _extract_sql(text: str) -> str:
        """Extrae el SQL limpio del texto generado por el LLM."""
        # Intentar extraer de bloque de código
        pattern = r"```(?:sql)?\s*([\s\S]*?)```"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Buscar SELECT/WITH directamente
        sql_pattern = r"((?:SELECT|WITH)\s[\s\S]+?;)"
        match = re.search(sql_pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return text.strip()