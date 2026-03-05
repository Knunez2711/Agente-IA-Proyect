<div align="center">

# 🤖 SQL Agent IA

### Consulta tu Base de Datos en Lenguaje Natural

*Convierte preguntas en español a consultas SQL automáticamente usando Inteligencia Artificial*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.1-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)

</div>

---

## 🚀 ¿Qué hace este proyecto?

**SQL Agent IA** es una aplicación web que permite consultar una base de datos PostgreSQL usando **lenguaje natural en español**, sin necesidad de saber SQL. El agente usa **LLaMA 3.1 70B** (vía Groq) y **LangChain** para entender la pregunta, generar la query correcta, ejecutarla y explicar los resultados de forma conversacional.

El usuario escribe una pregunta como:

> *"¿Cuál fue el mes con mayor facturación en 2024?"*

Y el agente automáticamente:

1. 🧠 **Analiza** la pregunta y el esquema de la base de datos  
2. ⚙️ **Genera el SQL** correcto usando LLaMA 3.1 70B (vía Groq)  
3. 🐘 **Ejecuta la consulta** directamente en PostgreSQL  
4. 💬 **Interpreta los resultados** y los explica en español  
5. 📊 **Muestra la tabla** de datos de forma visual y organizada  

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                     USUARIO                             │
│         "¿Cuál es el empleado con más ventas?"          │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  FLASK API                              │
│              POST /api/query                            │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│            LANGCHAIN AGENT + GROQ                       │
│   1. Lee el esquema de la BD                            │
│   2. LLaMA 3.1 70B genera el SQL                        │
└──────────────┬────────────────────────┬─────────────────┘
               │                        │
               ▼                        ▼
┌──────────────────────┐   ┌────────────────────────────┐
│     POSTGRESQL       │   │    GROQ (LLaMA 3.1)        │
│  Ejecuta la query    │──▶│  Interpreta resultados     │
└──────────────────────┘   └────────────────────────────┘
                                        │
                                        ▼
                        ┌─────────────────────────────────┐
                        │     FRONTEND BOOTSTRAP 5        │
                        │  Tabla + SQL + Interpretación   │
                        └─────────────────────────────────┘
```

---

## 📦 Stack Tecnológico

| Tecnología | Versión | Rol en el proyecto |
|-----------|---------|-------------------|
| **Python** | 3.11+ | Lenguaje base del backend |
| **Flask** | 3.0 | API REST + servidor web |
| **LangChain** | 0.2 | Framework de orquestación LLM |
| **Groq API** | — | Inferencia ultrarrápida con LLaMA 3.1 70B |
| **PostgreSQL** | 16 | Base de datos relacional |
| **SQLAlchemy** | 2.0 | ORM y gestión de conexiones |
| **Bootstrap** | 5.3 | Frontend responsive con tema oscuro |
| **Vanilla JS** | ES6+ | Interactividad y consumo de API |

---

## 🎯 Ejemplos de consultas

```
💼 ¿Cuántas ventas hubo en total en el año 2024?
🏆 ¿Cuál es el empleado con más ventas?
📅 ¿Cuánto es el total de ventas por mes en 2024?
📦 ¿Cuáles son los 5 productos más vendidos?
💰 ¿Cuál es el salario promedio por departamento?
👥 ¿Cuántos empleados hay en cada departamento?
📈 ¿Cuál fue el mes con mayor facturación?
⚠️  ¿Qué productos tienen stock menor a 20 unidades?
```

---

## ⚙️ Instalación y configuración

### Prerrequisitos

- Python 3.11+
- PostgreSQL instalado y corriendo
- Cuenta gratuita en [console.groq.com](https://console.groq.com)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Knunez2711/sql-agent.git
cd sql-agent
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate        # Mac / Linux
# venv\Scripts\activate         # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
GROQ_API_KEY=tu_api_key_de_groq       # Obtener en console.groq.com (gratis)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=empresa_db
DB_USER=postgres
DB_PASSWORD=tu_password_de_postgres
FLASK_SECRET_KEY=una_clave_secreta_random
FLASK_DEBUG=True
```

### 5. Crear la base de datos

```bash
psql -U postgres -f database/seed.sql
```

Esto crea la base de datos `empresa_db` con tablas de empleados, productos, departamentos y ventas, más datos de ejemplo listos para consultar.

### 6. Ejecutar el proyecto

```bash
python run.py
```

Abre tu navegador en **[http://localhost:5000](http://localhost:5000)** 🎉

---

## 📁 Estructura del proyecto

```
sql-agent/
├── src/
│   ├── __init__.py
│   ├── main.py          # Flask app + rutas de la API
│   ├── agent.py         # Agente LangChain + Groq (núcleo del proyecto)
│   └── database.py      # Conexión PostgreSQL + extracción de esquema
├── database/
│   └── seed.sql         # Script SQL con datos de ejemplo
├── static/
│   ├── css/
│   │   └── style.css    # Tema oscuro personalizado
│   └── js/
│       └── app.js       # Lógica del frontend
├── templates/
│   └── index.html       # UI con Bootstrap 5
├── .env.example         # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
├── run.py               # Punto de entrada
└── README.md
```

---

## 🔧 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| `GET` | `/` | Interfaz web principal |
| `POST` | `/api/query` | Recibe pregunta → retorna SQL + resultados + interpretación |
| `GET` | `/api/schema` | Devuelve el esquema completo de la base de datos |
| `GET` | `/api/suggestions` | Lista de preguntas de ejemplo |
| `POST` | `/api/execute` | Ejecuta SQL directamente |

**Ejemplo de request a `/api/query`:**

```json
POST /api/query
{
  "question": "¿Cuál es el empleado con más ventas?"
}
```

**Ejemplo de response:**

```json
{
  "success": true,
  "sql": "SELECT e.nombre, e.apellido, SUM(v.total) AS total_ventas ...",
  "data": {
    "columns": ["nombre", "apellido", "total_ventas"],
    "rows": [["Ana", "García", 29700000]],
    "total_rows": 3
  },
  "interpretation": "Ana García es la vendedora con mayor facturación..."
}
```

---

## 🔒 Seguridad implementada

- ✅ Solo se permiten queries `SELECT` — ninguna operación de escritura
- ✅ Detección y bloqueo de queries destructivas (`DROP`, `DELETE`, `TRUNCATE`, etc.)
- ✅ Credenciales protegidas con variables de entorno (nunca en el código)
- ✅ CORS configurado correctamente

---

## 📈 Roadmap — Próximas mejoras

- [ ] Historial de consultas persistente con Redis
- [ ] Visualizaciones automáticas con Chart.js según el tipo de dato
- [ ] Soporte para múltiples bases de datos simultáneas
- [ ] Autenticación de usuarios con JWT
- [ ] Export de resultados a CSV y Excel
- [ ] Dockerización con Docker Compose
- [ ] Deploy en Railway o Render

---

## 👤 Autor

<div align="center">

**Kevin Núñez**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Kevin%20Núñez-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/knunez97/)
[![GitHub](https://img.shields.io/badge/GitHub-Knunez2711-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Knunez2711)

</div>

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT** — siéntete libre de usarlo, modificarlo y distribuirlo.

---

<div align="center">

*Hecho con ❤️ y mucho ☕ por Kevin Núñez*

</div>