# ============================================================
# 📋 Git Commit Strategy — SQL Agent IA
# Kevin Núñez | github.com/Knunez2711
#
# Convención: Conventional Commits (estándar de la industria)
# Formato: <tipo>(<scope>): <descripción corta>
#
# Tipos usados:
#   feat     → nueva funcionalidad
#   fix      → corrección de bug
#   chore    → configuración, dependencias, scaffolding
#   test     → pruebas unitarias o de integración
#   docs     → documentación
#   refactor → mejora de código sin cambiar funcionalidad
#
# Ejecuta cada bloque EN ORDEN desde la raíz del proyecto.
# ============================================================


# ─────────────────────────────────────────────────────
# PASO 0 — Inicializar repositorio
# ─────────────────────────────────────────────────────

git init
git remote add origin https://github.com/Knunez2711/sql-agent-ia.git


# ─────────────────────────────────────────────────────
# COMMIT 1 — Scaffolding inicial
# ─────────────────────────────────────────────────────

git add .gitignore .env.example requirements.txt run.py
git commit -m "chore: initialize project with hexagonal architecture scaffold

[ADD] Project base structure following hexagonal architecture pattern
[ADD] .gitignore covering Python cache, venv, and sensitive env files
[ADD] requirements.txt with core dependencies:
      Flask, LangChain, Groq, SQLAlchemy, Pydantic, pytest
[ADD] .env.example as safe configuration template (no secrets)
[ADD] run.py as single application entry point"


# ─────────────────────────────────────────────────────
# COMMIT 2 — Capa de dominio
# ─────────────────────────────────────────────────────

git add src/domain/
git commit -m "feat(domain): implement core domain layer with pure business logic

[ADD] QueryResult entity — represents a complete agent query execution
[ADD] DatabaseSchema entity with Table and TableColumn value objects
[ADD] SQLGeneratorPort — abstract interface (port) for LLM adapters
[ADD] DatabaseRepositoryPort — abstract interface (port) for DB adapters
[ADD] Domain exceptions:
      · DangerousQueryException (blocked destructive SQL)
      · EmptyQuestionException (blank user input)
      · SQLGenerationException (LLM failure)
      · DatabaseQueryException (PostgreSQL error)

NOTE: This layer has zero external dependencies — pure Python only."


# ─────────────────────────────────────────────────────
# COMMIT 3 — Capa de aplicación
# ─────────────────────────────────────────────────────

git add src/application/
git commit -m "feat(application): add use cases and DTOs for query orchestration

[ADD] ProcessNaturalLanguageQueryUseCase — orchestrates full pipeline:
      validate → get schema → generate SQL → safety check →
      execute query → interpret results → return DTO
[ADD] GetDatabaseSchemaUseCase — retrieves and formats DB schema
[ADD] QueryRequestDTO — typed input object from interface layer
[ADD] QueryResponseDTO — typed output object with results + metadata
[ADD] SQL safety guard blocking: DROP, DELETE, TRUNCATE, ALTER, etc.
[ADD] Execution time tracking (milliseconds) per query"


# ─────────────────────────────────────────────────────
# COMMIT 4 — Adaptador PostgreSQL
# ─────────────────────────────────────────────────────

git add src/infrastructure/db/ src/infrastructure/repositories/
git commit -m "feat(infrastructure): implement PostgreSQL repository adapter

[ADD] PostgreSQLRepository implementing DatabaseRepositoryPort contract
[ADD] SQLAlchemy engine with QueuePool (pool_size=5, max_overflow=10)
[ADD] pool_pre_ping=True for automatic connection health checks
[ADD] get_schema() — maps DB introspection to domain entities
[ADD] execute_query() — safe read-only execution with error handling
[ADD] DependencyContainer (IoC) — wires ports to implementations,
      making adapters fully swappable without touching business logic"


# ─────────────────────────────────────────────────────
# COMMIT 5 — Adaptador LLM (Groq)
# ─────────────────────────────────────────────────────

git add src/infrastructure/llm/
git commit -m "feat(infrastructure): implement Groq LLM adapter with LangChain

[ADD] GroqLLMAdapter implementing SQLGeneratorPort contract
[ADD] LangChain ChatGroq integration with LLaMA-3.1-70b-versatile
[ADD] generate_sql() — schema-aware prompt engineering for SQL generation
[ADD] interpret_results() — natural language explanations in Spanish
[ADD] SQL extraction via regex (handles markdown blocks and raw SQL)
[SET] temperature=0 for deterministic, reproducible SQL generation

NOTE: Swapping to OpenAI/Gemini only requires a new adapter class."


# ─────────────────────────────────────────────────────
# COMMIT 6 — Capa de interfaces (API + Web)
# ─────────────────────────────────────────────────────

git add src/interfaces/
git commit -m "feat(interfaces): add Flask REST API and web interface layer

[ADD] Flask Application Factory pattern (create_app function)
[ADD] API Blueprint with REST endpoints:
      · POST /api/query      — natural language to SQL pipeline
      · GET  /api/schema     — live database schema inspection
      · GET  /api/suggestions — curated example questions
      · GET  /api/health     — service health check endpoint
[ADD] Pydantic v2 request validation schemas with custom validators
[ADD] Web Blueprint serving Bootstrap 5 frontend via Jinja2
[ADD] Global error handlers for 404 and 500 responses
[SET] CORS enabled for cross-origin requests"


# ─────────────────────────────────────────────────────
# COMMIT 7 — Base de datos de ejemplo
# ─────────────────────────────────────────────────────

git add database/
git commit -m "feat(database): add PostgreSQL sample database with realistic seed data

[ADD] empresa_db schema with 4 relational tables:
      · departamentos — 5 departments with budgets
      · empleados     — 10 employees with salaries (Colombian pesos)
      · productos     — 10 products with stock and pricing
      · ventas        — 25 sales records across 2024
[ADD] Foreign key relationships and NOT NULL constraints
[ADD] Realistic Colombian business data for meaningful AI queries"


# ─────────────────────────────────────────────────────
# COMMIT 8 — Frontend Bootstrap 5
# ─────────────────────────────────────────────────────

git add templates/ static/
git commit -m "feat(frontend): add responsive Bootstrap 5 UI with dark theme

[ADD] Single-page app with professional dark theme (CSS custom props)
[ADD] Natural language input with Ctrl+Enter keyboard shortcut
[ADD] Generated SQL display with syntax highlighting + copy button
[ADD] Dynamic results table with smart value formatting:
      · Currency formatting for large numbers (Colombian pesos)
      · Date localization (es-CO locale)
      · Boolean badges (Sí/No)
[ADD] AI interpretation panel with accent border
[ADD] Loading animation (bouncing dots) during processing
[ADD] Schema viewer modal for database exploration
[ADD] Clickable example questions sidebar
[ADD] Responsive layout with Bootstrap grid (mobile-friendly)"


# ─────────────────────────────────────────────────────
# COMMIT 9 — Tests unitarios
# ─────────────────────────────────────────────────────

git add tests/
git commit -m "test: add unit test suite for domain and application layers

[ADD] ProcessNaturalLanguageQueryUseCase tests:
      · Successful query returns correct results
      · Empty question raises EmptyQuestionException
      · Dangerous SQL (DROP, DELETE) is blocked
      · Execution time is recorded per query
      · Whitespace-only input is rejected
[ADD] Domain entity tests:
      · QueryResult.has_results / is_empty properties
      · QueryResult.to_dict() serialization
      · DatabaseSchema.to_prompt_text() formatting
      · DatabaseSchema.table_names listing
[SET] pytest + unittest.mock — zero external dependencies to run tests"


# ─────────────────────────────────────────────────────
# COMMIT 10 — Documentación
# ─────────────────────────────────────────────────────

git add README.md docs/
git commit -m "docs: add comprehensive README and project documentation

[ADD] README with professional badges (Python, LangChain, Groq, etc.)
[ADD] ASCII architecture diagram showing hexagonal layer structure
[ADD] Full installation guide (venv, pip, PostgreSQL, env config)
[ADD] REST API documentation with request/response JSON examples
[ADD] Tech stack table describing each technology's role
[ADD] Security considerations (read-only queries, env vars, CORS)
[ADD] Roadmap with planned improvements (Redis, Docker, Chart.js)
[ADD] GIT_COMMITS.sh — reproducible commit history guide"


# ─────────────────────────────────────────────────────
# PUSH FINAL
# ─────────────────────────────────────────────────────

git push -u origin main


# ─────────────────────────────────────────────────────
# RESUMEN DE COMMITS
# ─────────────────────────────────────────────────────
#
# 1.  chore: initialize project with hexagonal architecture scaffold
# 2.  feat(domain): implement core domain layer with pure business logic
# 3.  feat(application): add use cases and DTOs for query orchestration
# 4.  feat(infrastructure): implement PostgreSQL repository adapter
# 5.  feat(infrastructure): implement Groq LLM adapter with LangChain
# 6.  feat(interfaces): add Flask REST API and web interface layer
# 7.  feat(database): add PostgreSQL sample database with realistic seed data
# 8.  feat(frontend): add responsive Bootstrap 5 UI with dark theme
# 9.  test: add unit test suite for domain and application layers
# 10. docs: add comprehensive README and project documentation
#
# Convención: Conventional Commits — https://www.conventionalcommits.org